# Security Policy

## 🔒 Supported Versions

Currently supported versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## 🚨 Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please follow these steps:

### 1. Do NOT Open a Public Issue

Please do not report security vulnerabilities through public GitHub issues.

### 2. Report Privately

Send an email to: **[your-email@example.com]**

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### 3. Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Depends on severity
  - Critical: 1-7 days
  - High: 7-14 days
  - Medium: 14-30 days
  - Low: 30-90 days

## 🛡️ Security Best Practices

### For Users

1. **API Keys**
   - Never commit `.env` files
   - Use environment variables
   - Rotate keys regularly
   - Use separate keys for dev/prod

2. **Dependencies**
   - Keep dependencies updated
   - Review `requirements.txt` regularly
   - Use `pip-audit` to check for vulnerabilities

3. **Data Privacy**
   - Don't share transcripts with sensitive information
   - Be aware of OpenAI's data usage policy
   - Consider local Whisper for sensitive content

### For Contributors

1. **Code Review**
   - All PRs require review
   - Security-sensitive changes need extra scrutiny
   - Use static analysis tools

2. **Dependencies**
   - Vet new dependencies carefully
   - Pin versions in `requirements.txt`
   - Document why each dependency is needed

3. **Secrets**
   - Never hardcode secrets
   - Use GitHub Secrets for CI/CD
   - Scan commits for leaked secrets

## 🔍 Security Measures

### Current Implementations

- ✅ Environment variable for API keys
- ✅ `.gitignore` for sensitive files
- ✅ Input validation for URLs
- ✅ Error handling without exposing internals
- ✅ Dependency pinning

### Planned Improvements

- [ ] Rate limiting for API calls
- [ ] Input sanitization for file names
- [ ] Automated dependency scanning
- [ ] Security headers for web interface
- [ ] Audit logging

## 📋 Security Checklist

Before deploying:

- [ ] All API keys in environment variables
- [ ] `.env` file not committed
- [ ] Dependencies updated
- [ ] No hardcoded secrets
- [ ] Input validation in place
- [ ] Error messages don't leak info
- [ ] HTTPS enabled (if deployed)
- [ ] Access controls configured

## 🔐 Known Security Considerations

### OpenAI API

- Audio files are sent to OpenAI for transcription
- Review [OpenAI's data usage policy](https://openai.com/policies/api-data-usage-policies)
- For sensitive content, consider self-hosted Whisper

### Vector Database

- ChromaDB stores embeddings locally
- Embeddings may contain semantic information
- Secure the `vector_db/` directory appropriately

### YouTube Downloads

- yt-dlp downloads videos temporarily
- Files are deleted after processing
- Ensure `temp_audio/` is not publicly accessible

## 📚 Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [GitHub Security Advisories](https://github.com/advisories)

## 🙏 Acknowledgments

We appreciate responsible disclosure and will acknowledge security researchers who help improve our security.

---

**Last Updated**: October 2025
