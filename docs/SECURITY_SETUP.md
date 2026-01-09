# 🔒 Security Setup Guide

This guide explains how to configure and use the security features in YouTube Transcriber Pro.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Security Features](#security-features)
- [Configuration](#configuration)
- [Usage Guide](#usage-guide)
- [Production Deployment](#production-deployment)
- [Troubleshooting](#troubleshooting)

---

## Overview

YouTube Transcriber Pro includes a comprehensive security system to protect your instance from unauthorized access and abuse:

- **🔐 Authentication**: Access control with secure access codes
- **⏱️ Rate Limiting**: Automatic throttling to prevent API abuse
- **🛡️ Session Management**: Secure session handling with automatic timeout
- **🚫 Blacklisting**: Automatic IP blocking after repeated failed attempts

---

## Quick Start

### Development (No Authentication)

By default, authentication is **disabled** for easier development:

```bash
# No configuration needed - just run the app
python app_gradio.py
```

### Production (With Authentication)

1. **Copy environment file**:
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` and set**:
   ```bash
   REQUIRE_AUTH=true
   ACCESS_CODE=your_super_secret_code_here
   ```

3. **Start the application**:
   ```bash
   python app_gradio.py
   ```

4. **Login**: Navigate to the "🔐 Login" tab and enter your access code

---

## Security Features

### 1. Authentication System

**How it works:**
- Users must enter an access code to use the application
- Successful login creates a secure session (1-hour timeout)
- Session persists across all tabs and operations
- Failed attempts are tracked and can trigger automatic blocking

**Configuration:**
```bash
REQUIRE_AUTH=true                    # Enable authentication
ACCESS_CODE=my_secret_code_123       # Set your access code
```

**Recommendations:**
- Use strong access codes (min 20 characters)
- Include uppercase, lowercase, numbers, and symbols
- Don't share access codes publicly
- Rotate codes periodically

### 2. Rate Limiting

**Prevents:**
- API cost explosions from abuse
- Excessive OpenAI API usage
- Denial-of-service attacks

**Default Limits:**
```bash
MAX_TRANSCRIPTIONS_PER_HOUR=5        # 5 transcriptions per hour per user
MAX_SEARCHES_PER_MINUTE=20           # 20 searches per minute per user
MAX_CHATS_PER_MINUTE=10              # 10 chat messages per minute per user
```

**How it works:**
- Limits tracked per IP address (or session)
- Sliding window: limits reset gradually over time
- Clear error messages show remaining time
- Different limits for different operations

### 3. Session Management

**Features:**
- Automatic session creation on successful login
- Session timeout after 1 hour of inactivity
- Last activity timestamp updated on each request
- Automatic cleanup of expired sessions

**Technical Details:**
```python
SESSION_TIMEOUT = 3600  # 1 hour in seconds
```

### 4. Failed Attempt Tracking

**Protection against:**
- Brute force attacks
- Password guessing
- Unauthorized access attempts

**Behavior:**
- After 5 failed login attempts, IP is blacklisted
- Blacklisted IPs cannot use any features
- Requires manual removal from blacklist

---

## Configuration

### Environment Variables

All security settings are configured through environment variables in `.env`:

```bash
# ============================================================================
# SECURITY CONFIGURATION
# ============================================================================

# Authentication
REQUIRE_AUTH=false                   # Set to "true" to enable
ACCESS_CODE=                         # Your secret access code

# Rate Limiting
MAX_TRANSCRIPTIONS_PER_HOUR=5        # Transcriptions per hour
MAX_SEARCHES_PER_MINUTE=20           # Searches per minute
MAX_CHATS_PER_MINUTE=10              # Chat messages per minute
```

### Setting for Different Environments

#### Development
```bash
REQUIRE_AUTH=false
# No rate limits enforced
```

#### Staging
```bash
REQUIRE_AUTH=true
ACCESS_CODE=staging_test_code
MAX_TRANSCRIPTIONS_PER_HOUR=10
MAX_SEARCHES_PER_MINUTE=30
MAX_CHATS_PER_MINUTE=15
```

#### Production
```bash
REQUIRE_AUTH=true
ACCESS_CODE=Xk9$mP2nQ7!wL4zR8vC3hT6yB1dF5sA0  # Strong code!
MAX_TRANSCRIPTIONS_PER_HOUR=3                   # Conservative limits
MAX_SEARCHES_PER_MINUTE=10
MAX_CHATS_PER_MINUTE=5
```

---

## Usage Guide

### For End Users

#### 1. First Time Login

1. Open the application in your browser
2. Navigate to the **"🔐 Login"** tab
3. Enter the access code provided by your administrator
4. Click **"🔓 Login"**
5. You'll see a success message with your session ID
6. Now you can use all other tabs (Transcribe, Chat, Search, etc.)

#### 2. Using Features

After logging in, all features work normally:

- **Transcribe Videos**: Subject to rate limits (e.g., 5/hour)
- **Search**: Subject to rate limits (e.g., 20/minute)
- **Chat**: Subject to rate limits (e.g., 10/minute)

If you exceed a rate limit, you'll see a message like:

```
⚠️ Rate Limit Exceeded

Rate limit exceeded for transcription.
Please wait 3542 seconds.
Remaining requests: 0
```

#### 3. Session Timeout

Your session lasts 1 hour. After timeout, you'll need to log in again.

### For Administrators

#### Setting Up Access Codes

1. **Generate a strong code**:
   ```bash
   # Using Python
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Set in environment**:
   ```bash
   ACCESS_CODE=generated_code_here
   ```

3. **Share code securely** with authorized users (Signal, 1Password, etc.)

#### Monitoring Usage

Currently, usage monitoring is basic. Future enhancements:
- [ ] Usage dashboard
- [ ] Per-user quotas
- [ ] Analytics and reporting

#### Managing Blacklisted IPs

Blacklisted IPs are stored in memory. To clear:

1. **Restart the application** (clears all blacklists)

For persistent blacklisting, you'll need to extend `src/security.py` to use a database.

---

## Production Deployment

### Railway

1. **Set environment variables in Railway dashboard**:
   ```bash
   REQUIRE_AUTH=true
   ACCESS_CODE=your_secret_code
   MAX_TRANSCRIPTIONS_PER_HOUR=3
   ```

2. **Deploy**:
   ```bash
   git push origin main
   ```

Railway will automatically redeploy with new settings.

### Docker

1. **Create `.env.production`**:
   ```bash
   REQUIRE_AUTH=true
   ACCESS_CODE=your_secret_code
   MAX_TRANSCRIPTIONS_PER_HOUR=3
   ```

2. **Run container**:
   ```bash
   docker run --env-file .env.production -p 7860:7860 youtube-transcriber
   ```

### Other Platforms

Most platforms (Heroku, Render, Fly.io) support environment variables in their dashboard:

1. Navigate to your app settings
2. Add environment variables
3. Redeploy

---

## Troubleshooting

### "Authentication Required" even though I logged in

**Cause**: Session expired or invalid

**Solution**:
1. Go back to the Login tab
2. Log in again
3. Your session lasts 1 hour

### "Rate Limit Exceeded" - I'm the only user!

**Cause**: You hit your configured limits

**Solutions**:
1. Wait for the time specified in the error message
2. Increase limits in `.env`:
   ```bash
   MAX_TRANSCRIPTIONS_PER_HOUR=20  # Increase from 5
   ```
3. Restart the application for changes to take effect

### Forgot access code

**Solution**:
1. Check `.env` file on the server
2. Or regenerate and update:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

### Can't login - "Invalid Access Code"

**Possible causes**:
1. **Wrong code**: Double-check spelling and case (codes are case-sensitive)
2. **Trailing spaces**: Copy-paste carefully
3. **Environment not loaded**: Restart the application

**Debug**:
```bash
# Check if environment variables are set
python -c "import os; print(os.getenv('ACCESS_CODE'))"
```

### IP Blacklisted after too many failed attempts

**Solution**:
1. **Restart the application** (clears blacklist)
2. Or modify `src/security.py`:
   ```python
   # Temporarily increase max attempts
   self.max_failed_attempts = 10  # Default is 5
   ```

### Authentication not working at all

**Check**:
1. Is `REQUIRE_AUTH=true` set?
   ```bash
   python -c "import os; print(os.getenv('REQUIRE_AUTH'))"
   ```

2. Is `.env` file loaded?
   ```python
   # In app_gradio.py or security.py
   from dotenv import load_dotenv
   load_dotenv()  # Should be called at startup
   ```

---

## Advanced Configuration

### Custom Session Timeout

Edit `app_gradio.py`:

```python
# Change this line
SESSION_TIMEOUT = 3600  # 1 hour

# To your preferred timeout (in seconds)
SESSION_TIMEOUT = 7200  # 2 hours
SESSION_TIMEOUT = 1800  # 30 minutes
```

### Custom Rate Limits per Operation

Edit `src/security.py`:

```python
def __init__(self):
    # Transcription limiter
    self.transcription_limiter = RateLimiter(
        max_requests=int(os.getenv("MAX_TRANSCRIPTIONS_PER_HOUR", "5")),
        window_seconds=3600  # Change to 7200 for 2-hour window
    )
```

### Multiple Access Codes (Future Enhancement)

Currently supports one code. To add multiple users:

1. Use a database-backed authentication system
2. Consider integrating OAuth (Google, GitHub, etc.)
3. Or implement JWT token-based auth

---

## Security Best Practices

### ✅ DO:
- Use strong, unique access codes (20+ characters)
- Set conservative rate limits for production
- Enable REQUIRE_AUTH=true in production
- Use HTTPS in production (handled by Railway/Vercel)
- Rotate access codes periodically (every 3-6 months)
- Monitor logs for suspicious activity

### ❌ DON'T:
- Share access codes publicly (GitHub, Discord, etc.)
- Use weak codes like "password123"
- Commit `.env` files with real credentials
- Set rate limits too high (prevents cost control)
- Disable auth in production deployments

---

## Next Steps

1. **Enable authentication** for your production deployment
2. **Set appropriate rate limits** based on your budget
3. **Test the login flow** before sharing with users
4. **Monitor usage** to adjust limits as needed
5. Consider **additional features**:
   - User management dashboard
   - Per-user quotas
   - Usage analytics
   - Webhook notifications

---

## Need Help?

- **Issues**: https://github.com/your-username/youtube-transcriber/issues
- **Security Concerns**: Email security@yourapp.com
- **Documentation**: Check `/docs` folder for more guides

---

**Last Updated**: 2026-01-09
**Version**: 1.0.0 (Security Integration)
