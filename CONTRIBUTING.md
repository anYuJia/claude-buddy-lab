# Contributing to Claude Buddy Lab

Thanks for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/claude-buddy-lab.git`
3. Install dependencies: `pip install -e ".[dev]"`
4. Create a branch: `git checkout -b feature/your-feature`

## Development

### Code Style

- Use Black for formatting: `black src/`
- Use Ruff for linting: `ruff check src/`
- Python 3.8+ compatible

### Testing

```bash
# Run tests
pytest

# Test CLI
python -m src.cli --help
python -m src.cli preview --salt test-123
```

## Pull Request Process

1. Update the README.md if needed
2. Add tests for new features
3. Ensure all tests pass
4. Update documentation
5. Request review

## Issue Labels

- `bug`: Something isn't working
- `enhancement`: New feature request
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention needed
- `documentation`: Documentation improvements

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Welcome newcomers and help them learn

---

**Questions?** Open an issue or discussion on GitHub!
