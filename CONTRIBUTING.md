# Contributing to YouTube Transcriber Pro

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help others learn and grow

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported
2. Use the bug report template
3. Include:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version)
   - Error messages/logs

### Suggesting Features

1. Check if the feature has been requested
2. Use the feature request template
3. Explain:
   - Use case
   - Expected behavior
   - Why it's valuable
   - Possible implementation

### Pull Requests

1. **Fork the repository**
```bash
git clone https://github.com/YOUR_USERNAME/youtube-transcriber.git
cd youtube-transcriber
```

2. **Create a branch**
```bash
git checkout -b feature/your-feature-name
```

3. **Make your changes**
   - Follow code style guidelines
   - Add tests for new features
   - Update documentation
   - Keep commits atomic and descriptive

4. **Test your changes**
```bash
# Run tests
pytest

# Check coverage
pytest --cov=src

# Run linting
flake8 src tests
```

5. **Commit your changes**
```bash
git add .
git commit -m "feat: add amazing feature"
```

Use conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `test:` Tests
- `refactor:` Code refactoring
- `style:` Formatting
- `chore:` Maintenance

6. **Push and create PR**
```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Development Setup

### Prerequisites
- Python 3.8+
- FFmpeg
- Git

### Setup

```bash
# Clone repository
git clone <repo-url>
cd youtube-transcriber

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install pytest pytest-cov pytest-mock flake8 black

# Setup pre-commit hooks (optional)
pip install pre-commit
pre-commit install
```

### Running Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/test_utils.py

# With coverage
pytest --cov=src --cov-report=html

# Watch mode
pytest-watch
```

## Code Style

### Python Style Guide

Follow PEP 8 with these specifics:

- **Line length**: 100 characters
- **Indentation**: 4 spaces
- **Quotes**: Double quotes for strings
- **Imports**: Grouped and sorted

### Formatting

Use Black for formatting:

```bash
black src tests
```

### Linting

Use flake8:

```bash
flake8 src tests --max-line-length=100
```

### Type Hints

Use type hints for function signatures:

```python
def process_video(url: str, index: int = 1) -> Dict[str, Any]:
    """Process a video"""
    pass
```

### Docstrings

Use Google-style docstrings:

```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief description.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When something is wrong
    """
    pass
```

## Testing Guidelines

### Unit Tests

- Test individual functions
- Mock external dependencies
- Cover edge cases
- Use descriptive test names

Example:

```python
def test_extract_video_id_with_standard_url():
    """Test video ID extraction from standard YouTube URL"""
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    result = extract_video_id(url)
    assert result == "dQw4w9WgXcQ"
```

### Integration Tests

- Test complete workflows
- Use real (but small) data
- Mark as integration tests

```python
@pytest.mark.integration
def test_full_transcription_workflow():
    """Test complete transcription process"""
    # Test implementation
    pass
```

### Test Coverage

Aim for:
- **Minimum**: 80% coverage
- **Target**: 90% coverage
- **Critical paths**: 100% coverage

## Documentation

### Code Documentation

- Add docstrings to all public functions
- Include type hints
- Explain complex logic with comments

### User Documentation

Update relevant docs:
- `README.md` - Overview and quick start
- `docs/USAGE.md` - Detailed usage
- `docs/API.md` - API reference
- `docs/DEPLOYMENT.md` - Deployment guide

### Changelog

Update `CHANGELOG.md` with your changes:

```markdown
## [Unreleased]

### Added
- New feature X

### Fixed
- Bug in Y

### Changed
- Improved Z
```

## Project Structure

```
youtube-transcriber/
├── src/                    # Source code
│   ├── transcriber.py     # Core logic
│   ├── rag_engine.py      # RAG features
│   └── utils.py           # Utilities
├── tests/                 # Test suite
│   ├── test_*.py          # Test files
│   └── conftest.py        # Fixtures
├── docs/                  # Documentation
├── main.py               # CLI entry
├── app_gradio.py         # UI entry
└── config.py             # Configuration
```

## Areas for Contribution

### High Priority

- [ ] Parallel video processing
- [ ] Automatic video summarization
- [ ] Playlist support
- [ ] Better error messages
- [ ] Performance optimization

### Medium Priority

- [ ] Export to PDF/Markdown
- [ ] Speaker detection
- [ ] Timestamp extraction
- [ ] Multi-language UI
- [ ] Video thumbnail display

### Low Priority

- [ ] Dark mode UI
- [ ] Custom themes
- [ ] Keyboard shortcuts
- [ ] Video preview
- [ ] Statistics dashboard

### Documentation

- [ ] Video tutorials
- [ ] More examples
- [ ] API cookbook
- [ ] Troubleshooting guide
- [ ] Performance tuning guide

## Review Process

1. **Automated checks**
   - Tests must pass
   - Coverage must not decrease
   - Linting must pass

2. **Code review**
   - At least one approval required
   - Address all comments
   - Keep discussions constructive

3. **Documentation review**
   - Check for clarity
   - Verify examples work
   - Update related docs

4. **Merge**
   - Squash commits if needed
   - Update changelog
   - Close related issues

## Getting Help

- **Questions**: Open a discussion
- **Bugs**: Open an issue
- **Chat**: Join our Discord (coming soon)
- **Email**: Contact maintainers

## Recognition

Contributors will be:
- Listed in `CONTRIBUTORS.md`
- Mentioned in release notes
- Credited in documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to YouTube Transcriber Pro! 🎉
