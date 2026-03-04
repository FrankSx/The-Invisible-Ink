# Contributing to ASCII Unicode Exploit Kit

Thank you for your interest in contributing to the ASCII Unicode Exploit Kit! This document provides guidelines for contributing to the project.

## 🎯 Contribution Areas

### 1. New Attack Vectors
- Novel Unicode exploitation techniques
- Additional homoglyph mappings
- Cross-platform normalization quirks
- ML-system specific bypasses

### 2. Detection Improvements
- Enhanced analyzer heuristics
- New suspicious character patterns
- Script mixing detection
- Risk scoring refinements

### 3. Tool Enhancements
- Additional output formats
- Performance optimizations
- New obfuscation techniques
- Integration with other security tools

### 4. Documentation
- Technical write-ups
- Real-world case studies
- Mitigation strategies
- Educational materials

## 📝 Code Standards

### Python Style
- Follow PEP 8
- Use type hints where possible
- Document all public functions
- Include docstrings with examples

### Testing
- Add tests for new features
- Maintain >80% code coverage
- Test edge cases with Unicode
- Validate on Python 3.8+

### Commit Messages
```
type(scope): description

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Example:
```
feat(unicode): add Cherokee homoglyphs

Add Cherokee letters that resemble Latin characters
to the homoglyph mapping dictionary.

Closes #123
```

## 🔬 Research Contributions

When contributing research findings:

1. **Document the target system** (if applicable)
2. **Provide reproducible examples**
3. **Include mitigation strategies**
4. **Follow responsible disclosure**

## 🧪 Testing Your Changes

```bash
# Run all tests
python tests/test_suite.py

# Test specific module
python -m pytest tests/test_suite.py::TestUnicodeGenerator -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

## 📋 Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Update documentation
6. Run the test suite
7. Submit a pull request

### PR Checklist
- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Commit messages are clear

## 🐛 Reporting Bugs

When reporting bugs, please include:

1. **Python version**
2. **Operating system**
3. **Minimal reproduction case**
4. **Expected vs actual behavior**
5. **Any error messages**

## 💡 Feature Requests

Feature requests are welcome! Please:

1. Check existing issues first
2. Describe the use case
3. Explain why current tools don't suffice
4. Provide examples if possible

## 🏆 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

## ⚖️ Ethical Guidelines

All contributions must adhere to our ethical use policy:

- Research-focused only
- No malicious exploitation tools
- Include defensive recommendations
- Follow responsible disclosure

## 📞 Contact

- Open an issue for questions
- Email: [your-email]
- Blog: https://frankhacks.blogspot.com

---

**13th Hour Research Division** 🦀
