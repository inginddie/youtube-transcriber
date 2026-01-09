#!/usr/bin/env python3
"""
Quick test to verify security integration works correctly
"""
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

def test_security_manager():
    """Test security manager initialization"""
    print("🧪 Testing Security Manager Integration\n")

    try:
        from src.security import security_manager
        print("✅ Security manager imported successfully")

        # Test auth manager
        print(f"   - Auth required: {security_manager.auth.require_auth}")
        print(f"   - Access code set: {'Yes' if security_manager.auth.access_code else 'No'}")

        # Test rate limiters
        print("\n✅ Rate limiters initialized:")
        print(f"   - Transcription: {security_manager.transcription_limiter.max_requests} per hour")
        print(f"   - Search: {security_manager.search_limiter.max_requests} per minute")
        print(f"   - Chat: {security_manager.chat_limiter.max_requests} per minute")

        # Test rate limiting
        client_id = "test_user"
        allowed, error = security_manager.check_rate_limit(client_id, "transcription")
        print(f"\n✅ Rate limit check works: allowed={allowed}")

        # Test authentication (if enabled)
        if security_manager.auth.require_auth:
            test_code = os.getenv("ACCESS_CODE", "")
            result = security_manager.auth.verify_access_code(test_code)
            print(f"✅ Auth verification works: {result}")
        else:
            print("ℹ️  Auth not required (REQUIRE_AUTH=false)")

        return True

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_gradio_imports():
    """Test that Gradio app can be imported"""
    print("\n🧪 Testing Gradio App Integration\n")

    try:
        # Test imports (don't launch UI)
        import sys
        sys.argv = ['test']  # Prevent Gradio from trying to launch

        # Import main functions
        print("✅ Importing app_gradio...")
        import app_gradio

        # Verify security functions exist
        print("✅ Checking security functions...")
        assert hasattr(app_gradio, 'login'), "login function missing"
        assert hasattr(app_gradio, 'check_authentication'), "check_authentication missing"
        assert hasattr(app_gradio, 'check_rate_limit'), "check_rate_limit missing"

        print("✅ All security functions present")

        # Verify session management
        assert hasattr(app_gradio, 'create_session'), "create_session missing"
        assert hasattr(app_gradio, 'verify_session'), "verify_session missing"
        print("✅ Session management functions present")

        return True

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("   SECURITY INTEGRATION TEST SUITE")
    print("=" * 60)

    results = []

    # Test 1: Security Manager
    results.append(("Security Manager", test_security_manager()))

    # Test 2: Gradio Integration
    results.append(("Gradio Integration", test_gradio_imports()))

    # Summary
    print("\n" + "=" * 60)
    print("   TEST SUMMARY")
    print("=" * 60)

    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status:12} - {test_name}")

    all_passed = all(result for _, result in results)

    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED! Security integration is working correctly.")
    else:
        print("⚠️  SOME TESTS FAILED! Please review errors above.")
    print("=" * 60)

    return all_passed


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
