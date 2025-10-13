# GitHub Configuration

This directory contains GitHub-specific configuration files.

## 📋 Issue Templates

### Bug Report (`ISSUE_TEMPLATE/bug_report.md`)
Template for users to report bugs with all necessary information.

**When to use:** When something isn't working as expected.

### Feature Request (`ISSUE_TEMPLATE/feature_request.md`)
Template for users to suggest new features or improvements.

**When to use:** When you have an idea for a new feature.

## 🔄 Pull Request Template

### PR Template (`pull_request_template.md`)
Template for contributors to submit pull requests with proper documentation.

**When to use:** Automatically used when creating a PR.

## 🤖 GitHub Actions Workflows

### Tests Workflow (`workflows/tests.yml`)
Automatically runs tests on every push and pull request.

**Runs:**
- Python tests with pytest
- Code coverage reporting
- Linting with flake8
- On multiple OS (Ubuntu, Windows, macOS)
- On multiple Python versions (3.8, 3.9, 3.10, 3.11)

### Lint Workflow (`workflows/lint.yml`)
Automatically checks code formatting and style.

**Runs:**
- Black formatting check
- isort import sorting check
- flake8 linting

## 🔧 Configuration

To enable GitHub Actions:
1. Push your code to GitHub
2. Go to Actions tab
3. Enable workflows if needed

To add secrets (for CI/CD):
1. Go to Settings → Secrets and variables → Actions
2. Add `OPENAI_API_KEY` if needed for tests

## 📝 Customization

Feel free to customize these templates and workflows to match your project's needs.

### Modifying Issue Templates

Edit files in `ISSUE_TEMPLATE/` to add or remove fields.

### Modifying Workflows

Edit files in `workflows/` to change:
- Python versions tested
- Operating systems
- Test commands
- Coverage thresholds

## 🚀 Best Practices

1. **Use templates** - They ensure consistent issue/PR quality
2. **Keep workflows fast** - Optimize test runs
3. **Monitor Actions** - Check for failures regularly
4. **Update regularly** - Keep actions versions current

## 📚 Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Issue Templates Guide](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

---

**Note:** These configurations are optional but recommended for professional projects.
