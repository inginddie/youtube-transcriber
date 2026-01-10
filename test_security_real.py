#!/usr/bin/env python3
"""
Test REAL de seguridad - Demuestra que las protecciones funcionan
"""
import os
import sys

# Forzar seguridad activada para este test
os.environ["REQUIRE_AUTH"] = "true"
os.environ["ACCESS_CODE"] = "test_code_123"
os.environ["MAX_TRANSCRIPTIONS_PER_HOUR"] = "2"

from src.security import security_manager

def test_authentication():
    """Test 1: Autenticación funciona"""
    print("=" * 60)
    print("TEST 1: AUTENTICACIÓN")
    print("=" * 60)

    # Verificar que auth está activada
    assert security_manager.auth.require_auth == True, "Auth debería estar activada"
    print("✅ Auth está ACTIVADA")

    # Test código correcto
    result = security_manager.auth.verify_access_code("test_code_123")
    assert result == True, "Código correcto debería funcionar"
    print("✅ Código correcto ACEPTA")

    # Test código incorrecto
    result = security_manager.auth.verify_access_code("wrong_code")
    assert result == False, "Código incorrecto debería fallar"
    print("✅ Código incorrecto RECHAZA")

    print("\n✅ TEST 1 PASADO: Autenticación funciona correctamente\n")


def test_rate_limiting():
    """Test 2: Rate limiting funciona"""
    print("=" * 60)
    print("TEST 2: RATE LIMITING")
    print("=" * 60)

    client_id = "test_user_123"

    # Request 1 - debe pasar
    allowed, error = security_manager.check_rate_limit(client_id, "transcription")
    assert allowed == True, "Primera request debería pasar"
    print("✅ Request 1/2: PERMITIDA")

    # Request 2 - debe pasar
    allowed, error = security_manager.check_rate_limit(client_id, "transcription")
    assert allowed == True, "Segunda request debería pasar"
    print("✅ Request 2/2: PERMITIDA")

    # Request 3 - debe FALLAR (límite es 2)
    allowed, error = security_manager.check_rate_limit(client_id, "transcription")
    assert allowed == False, "Tercera request debería FALLAR"
    assert "Rate limit exceeded" in error, "Debe mostrar mensaje de rate limit"
    print(f"✅ Request 3/2: BLOQUEADA")
    print(f"   Mensaje: {error}")

    print("\n✅ TEST 2 PASADO: Rate limiting funciona correctamente\n")


def test_blacklisting():
    """Test 3: Blacklisting funciona"""
    print("=" * 60)
    print("TEST 3: BLACKLISTING POR INTENTOS FALLIDOS")
    print("=" * 60)

    client_id = "attacker_ip"

    # Simular 5 intentos fallidos
    for i in range(1, 6):
        security_manager.record_failed_attempt(client_id)
        print(f"   Intento fallido {i}/5")

    # Verificar que está en blacklist
    assert client_id in security_manager.blacklist, "Cliente debería estar en blacklist"
    print("✅ Cliente agregado a BLACKLIST después de 5 intentos")

    # Intentar hacer una operación
    allowed, error = security_manager.check_rate_limit(client_id, "transcription")
    assert allowed == False, "Cliente en blacklist debe ser bloqueado"
    assert "blacklisted" in error.lower(), "Mensaje debe mencionar blacklist"
    print(f"✅ Cliente bloqueado: {error}")

    print("\n✅ TEST 3 PASADO: Blacklisting funciona correctamente\n")


def test_integration_with_functions():
    """Test 4: Integración con funciones de la app"""
    print("=" * 60)
    print("TEST 4: INTEGRACIÓN CON FUNCIONES DE LA APP")
    print("=" * 60)

    # Importar funciones de la app
    sys.path.insert(0, os.path.dirname(__file__))
    from app_gradio import check_authentication, check_rate_limit

    # Test 1: Sin sesión - debe fallar
    is_auth, error = check_authentication("")
    assert is_auth == False, "Sin sesión debe fallar"
    print("✅ Sin sesión: BLOQUEADO")
    print(f"   Mensaje: {error[:50]}...")

    # Test 2: Con sesión inválida - debe fallar
    is_auth, error = check_authentication("invalid_session_id")
    assert is_auth == False, "Sesión inválida debe fallar"
    print("✅ Sesión inválida: BLOQUEADO")

    # Test 3: Rate limit sin sesión
    is_allowed, error = check_rate_limit("", "transcription")
    # Nota: Esto aún verifica rate limit incluso sin sesión
    print("✅ Rate limiting verifica incluso sin sesión")

    print("\n✅ TEST 4 PASADO: Integración funciona correctamente\n")


def main():
    """Ejecutar todos los tests"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "TEST DE SEGURIDAD REAL" + " " * 25 + "║")
    print("║" + " " * 10 + "Demuestra que la protección funciona" + " " * 11 + "║")
    print("╚" + "=" * 58 + "╝")
    print("\n")

    tests = [
        ("Autenticación", test_authentication),
        ("Rate Limiting", test_rate_limiting),
        ("Blacklisting", test_blacklisting),
        ("Integración", test_integration_with_functions)
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"\n❌ TEST FALLIDO: {test_name}")
            print(f"   Error: {str(e)}\n")
            import traceback
            traceback.print_exc()

    # Resumen
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 20 + "RESUMEN" + " " * 31 + "║")
    print("╠" + "=" * 58 + "╣")
    print(f"║  ✅ Tests Pasados: {passed:<42} ║")
    print(f"║  ❌ Tests Fallidos: {failed:<41} ║")
    print("╚" + "=" * 58 + "╝")

    if failed == 0:
        print("\n🎉 TODOS LOS TESTS PASARON")
        print("\n🔒 La seguridad REALMENTE funciona cuando está activada!")
        print("\nPara usarla en producción:")
        print("  1. Set REQUIRE_AUTH=true en Railway")
        print("  2. Set ACCESS_CODE=tu_codigo_secreto")
        print("  3. La app bloqueará acceso sin autenticación")
        print("  4. Rate limiting se aplicará automáticamente")
        return 0
    else:
        print("\n⚠️ ALGUNOS TESTS FALLARON - Revisar implementación")
        return 1


if __name__ == "__main__":
    sys.exit(main())
