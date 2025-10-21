"""
Sistema de seguridad para producción
Incluye: Rate limiting, autenticación, protección contra bots
"""
import os
import time
import hashlib
import secrets
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
import threading


class RateLimiter:
    """Rate limiter para prevenir abuso"""
    
    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = defaultdict(list)
        self.lock = threading.Lock()
    
    def is_allowed(self, identifier: str) -> Tuple[bool, Optional[int]]:
        """
        Verifica si una request está permitida
        
        Args:
            identifier: IP o user ID
            
        Returns:
            (allowed, seconds_until_reset)
        """
        with self.lock:
            now = time.time()
            
            # Limpiar requests antiguas
            self.requests[identifier] = [
                req_time for req_time in self.requests[identifier]
                if now - req_time < self.window_seconds
            ]
            
            # Verificar límite
            if len(self.requests[identifier]) >= self.max_requests:
                oldest_request = min(self.requests[identifier])
                seconds_until_reset = int(self.window_seconds - (now - oldest_request))
                return False, seconds_until_reset
            
            # Agregar nueva request
            self.requests[identifier].append(now)
            return True, None
    
    def get_remaining(self, identifier: str) -> int:
        """Obtiene requests restantes"""
        with self.lock:
            now = time.time()
            self.requests[identifier] = [
                req_time for req_time in self.requests[identifier]
                if now - req_time < self.window_seconds
            ]
            return max(0, self.max_requests - len(self.requests[identifier]))


class AuthManager:
    """Gestor de autenticación simple"""
    
    def __init__(self):
        self.access_code = os.getenv("ACCESS_CODE", "")
        self.require_auth = os.getenv("REQUIRE_AUTH", "false").lower() == "true"
        self.sessions: Dict[str, datetime] = {}
        self.session_duration = timedelta(hours=24)
        self.lock = threading.Lock()
    
    def verify_access_code(self, code: str) -> bool:
        """Verifica código de acceso"""
        if not self.require_auth:
            return True
        return secrets.compare_digest(code, self.access_code)
    
    def create_session(self, identifier: str) -> str:
        """Crea una sesión autenticada"""
        with self.lock:
            session_id = secrets.token_urlsafe(32)
            self.sessions[session_id] = datetime.now()
            return session_id
    
    def verify_session(self, session_id: str) -> bool:
        """Verifica si una sesión es válida"""
        if not self.require_auth:
            return True
            
        with self.lock:
            if session_id not in self.sessions:
                return False
            
            session_time = self.sessions[session_id]
            if datetime.now() - session_time > self.session_duration:
                del self.sessions[session_id]
                return False
            
            return True
    
    def cleanup_expired_sessions(self):
        """Limpia sesiones expiradas"""
        with self.lock:
            now = datetime.now()
            expired = [
                sid for sid, stime in self.sessions.items()
                if now - stime > self.session_duration
            ]
            for sid in expired:
                del self.sessions[sid]


class SecurityManager:
    """Gestor principal de seguridad"""
    
    def __init__(self):
        # Rate limiters por tipo de operación
        self.transcription_limiter = RateLimiter(
            max_requests=int(os.getenv("MAX_TRANSCRIPTIONS_PER_HOUR", "5")),
            window_seconds=3600
        )
        self.search_limiter = RateLimiter(
            max_requests=int(os.getenv("MAX_SEARCHES_PER_MINUTE", "20")),
            window_seconds=60
        )
        self.chat_limiter = RateLimiter(
            max_requests=int(os.getenv("MAX_CHATS_PER_MINUTE", "10")),
            window_seconds=60
        )
        
        # Auth manager
        self.auth = AuthManager()
        
        # Blacklist de IPs
        self.blacklist: set = set()
        self.blacklist_lock = threading.Lock()
        
        # Contador de intentos fallidos
        self.failed_attempts: Dict[str, int] = defaultdict(int)
        self.max_failed_attempts = 5
    
    def get_client_id(self, request) -> str:
        """Obtiene identificador del cliente"""
        # En producción, usar IP real del cliente
        if hasattr(request, 'client'):
            return request.client.host
        return "unknown"
    
    def is_blacklisted(self, identifier: str) -> bool:
        """Verifica si un cliente está en blacklist"""
        with self.blacklist_lock:
            return identifier in self.blacklist
    
    def add_to_blacklist(self, identifier: str):
        """Agrega un cliente a la blacklist"""
        with self.blacklist_lock:
            self.blacklist.add(identifier)
            print(f"⚠️  Cliente {identifier} agregado a blacklist")
    
    def record_failed_attempt(self, identifier: str):
        """Registra un intento fallido"""
        self.failed_attempts[identifier] += 1
        if self.failed_attempts[identifier] >= self.max_failed_attempts:
            self.add_to_blacklist(identifier)
    
    def check_rate_limit(self, identifier: str, operation: str) -> Tuple[bool, Optional[str]]:
        """
        Verifica rate limit para una operación
        
        Returns:
            (allowed, error_message)
        """
        if self.is_blacklisted(identifier):
            return False, "Access denied. Contact administrator."
        
        limiter_map = {
            "transcription": self.transcription_limiter,
            "search": self.search_limiter,
            "chat": self.chat_limiter
        }
        
        limiter = limiter_map.get(operation)
        if not limiter:
            return True, None
        
        allowed, wait_time = limiter.is_allowed(identifier)
        
        if not allowed:
            remaining = limiter.get_remaining(identifier)
            error_msg = (
                f"Rate limit exceeded for {operation}. "
                f"Please wait {wait_time} seconds. "
                f"Remaining requests: {remaining}"
            )
            return False, error_msg
        
        return True, None


# Instancia global
security_manager = SecurityManager()


def require_rate_limit(operation: str):
    """Decorador para aplicar rate limiting"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Obtener identificador del cliente
            identifier = "default"  # En producción, obtener IP real
            
            # Verificar rate limit
            allowed, error_msg = security_manager.check_rate_limit(identifier, operation)
            
            if not allowed:
                return None, error_msg
            
            # Ejecutar función
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


def get_security_headers() -> Dict[str, str]:
    """Headers de seguridad para producción"""
    return {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline';",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
