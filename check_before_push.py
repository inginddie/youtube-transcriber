#!/usr/bin/env python3
"""
Script de verificación antes de subir a GitHub.
Verifica que no haya archivos sensibles o problemas comunes.
"""

import os
import sys
from pathlib import Path

# Colores para terminal
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"


def print_header(text):
    """Imprime un encabezado"""
    print(f"\n{BOLD}{'=' * 70}{RESET}")
    print(f"{BOLD}{text}{RESET}")
    print(f"{BOLD}{'=' * 70}{RESET}\n")


def print_success(text):
    """Imprime mensaje de éxito"""
    print(f"{GREEN}✓ {text}{RESET}")


def print_error(text):
    """Imprime mensaje de error"""
    print(f"{RED}✗ {text}{RESET}")


def print_warning(text):
    """Imprime mensaje de advertencia"""
    print(f"{YELLOW}⚠ {text}{RESET}")


def check_env_file():
    """Verifica que .env no esté en el repo"""
    print_header("🔒 Verificando archivos sensibles")
    
    if Path(".env").exists():
        # Verificar si está en .gitignore
        with open(".gitignore", "r") as f:
            if ".env" in f.read():
                print_success(".env existe pero está en .gitignore")
                return True
            else:
                print_error(".env existe pero NO está en .gitignore!")
                return False
    else:
        print_warning(".env no existe (asegúrate de tener .env.example)")
        return True


def check_api_keys():
    """Verifica que no haya API keys hardcodeadas"""
    print_header("🔑 Buscando API keys hardcodeadas")
    
    patterns = [
        "sk-proj-",
        "OPENAI_API_KEY = \"sk-",
        "api_key = \"sk-",
    ]
    
    found_issues = False
    
    for py_file in Path(".").rglob("*.py"):
        # Ignorar directorios y archivos específicos
        if any(x in str(py_file) for x in ["venv", "__pycache__", "check_before_push.py"]):
            continue
            
        with open(py_file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            for pattern in patterns:
                if pattern in content:
                    print_error(f"Posible API key en {py_file}")
                    found_issues = True
    
    if not found_issues:
        print_success("No se encontraron API keys hardcodeadas")
    
    return not found_issues


def check_large_files():
    """Verifica archivos grandes"""
    print_header("📦 Verificando archivos grandes")
    
    max_size_mb = 10
    large_files = []
    
    for file in Path(".").rglob("*"):
        if file.is_file():
            # Ignorar directorios comunes
            if any(x in str(file) for x in ["venv", ".git", "__pycache__", "node_modules"]):
                continue
                
            size_mb = file.stat().st_size / (1024 * 1024)
            if size_mb > max_size_mb:
                large_files.append((file, size_mb))
    
    if large_files:
        print_warning(f"Archivos mayores a {max_size_mb}MB encontrados:")
        for file, size in large_files:
            print(f"  - {file}: {size:.2f}MB")
        print_warning("Considera usar Git LFS para archivos grandes")
        return False
    else:
        print_success(f"No hay archivos mayores a {max_size_mb}MB")
        return True


def check_gitignore():
    """Verifica que .gitignore esté configurado"""
    print_header("📝 Verificando .gitignore")
    
    required_entries = [
        ".env",
        "venv/",
        "__pycache__/",
        "*.pyc",
        "vector_db/",
        "temp_audio/",
    ]
    
    if not Path(".gitignore").exists():
        print_error(".gitignore no existe!")
        return False
    
    with open(".gitignore", "r") as f:
        gitignore_content = f.read()
    
    missing = []
    for entry in required_entries:
        if entry not in gitignore_content:
            missing.append(entry)
    
    if missing:
        print_warning("Entradas faltantes en .gitignore:")
        for entry in missing:
            print(f"  - {entry}")
        return False
    else:
        print_success(".gitignore está correctamente configurado")
        return True


def check_readme():
    """Verifica que README.md exista y tenga contenido"""
    print_header("📖 Verificando README.md")
    
    if not Path("README.md").exists():
        print_error("README.md no existe!")
        return False
    
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()
    
    if len(content) < 100:
        print_error("README.md está muy vacío")
        return False
    
    # Verificar secciones importantes
    sections = ["Features", "Installation", "Usage", "License"]
    missing_sections = [s for s in sections if s not in content]
    
    if missing_sections:
        print_warning("Secciones faltantes en README:")
        for section in missing_sections:
            print(f"  - {section}")
    
    print_success("README.md existe y tiene contenido")
    return True


def check_license():
    """Verifica que LICENSE exista"""
    print_header("⚖️  Verificando LICENSE")
    
    if Path("LICENSE").exists():
        print_success("LICENSE existe")
        return True
    else:
        print_warning("LICENSE no existe (considera agregar uno)")
        return True  # No es crítico


def check_requirements():
    """Verifica requirements.txt"""
    print_header("📦 Verificando requirements.txt")
    
    if not Path("requirements.txt").exists():
        print_error("requirements.txt no existe!")
        return False
    
    with open("requirements.txt", "r") as f:
        content = f.read()
    
    if len(content) < 10:
        print_error("requirements.txt está vacío")
        return False
    
    print_success("requirements.txt existe y tiene contenido")
    return True


def check_structure():
    """Verifica estructura básica del proyecto"""
    print_header("📁 Verificando estructura del proyecto")
    
    required_dirs = ["src", "docs"]
    required_files = ["README.md", "requirements.txt", ".gitignore"]
    
    all_good = True
    
    for dir_name in required_dirs:
        if Path(dir_name).exists():
            print_success(f"Directorio {dir_name}/ existe")
        else:
            print_error(f"Directorio {dir_name}/ no existe")
            all_good = False
    
    for file_name in required_files:
        if Path(file_name).exists():
            print_success(f"Archivo {file_name} existe")
        else:
            print_error(f"Archivo {file_name} no existe")
            all_good = False
    
    return all_good


def main():
    """Función principal"""
    print(f"\n{BOLD}🚀 Verificación Pre-Push a GitHub{RESET}")
    
    checks = [
        ("Estructura del proyecto", check_structure),
        ("Archivos sensibles", check_env_file),
        ("API keys hardcodeadas", check_api_keys),
        (".gitignore", check_gitignore),
        ("README.md", check_readme),
        ("LICENSE", check_license),
        ("requirements.txt", check_requirements),
        ("Archivos grandes", check_large_files),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print_error(f"Error en {name}: {e}")
            results.append((name, False))
    
    # Resumen
    print_header("📊 RESUMEN")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        if result:
            print_success(f"{name}")
        else:
            print_error(f"{name}")
    
    print(f"\n{BOLD}Resultado: {passed}/{total} verificaciones pasadas{RESET}\n")
    
    if passed == total:
        print(f"{GREEN}{BOLD}✓ ¡Todo listo para subir a GitHub!{RESET}\n")
        return 0
    else:
        print(f"{RED}{BOLD}✗ Hay problemas que debes resolver antes de subir{RESET}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
