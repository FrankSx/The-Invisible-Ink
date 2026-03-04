# 🔤 ASCII Unicode Exploit Kit

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![13th Hour](https://img.shields.io/badge/13th%20Hour-Research-red.svg)]()

> *"In the space between bytes, we find our truth."* — frankSx

A comprehensive toolkit for adversarial ML testing using ASCII art and Unicode manipulation techniques. This repository contains tools for generating adversarial inputs that exploit the gap between human visual perception and machine parsing.

## ⚠️ Ethical Usage Notice

These tools are designed for:
- ✅ Security research and red teaming
- ✅ Adversarial robustness testing  
- ✅ Educational purposes in ML safety
- ✅ Responsible disclosure programs

**Do not use for:**
- ❌ Bypassing safety filters maliciously
- ❌ Generating harmful content
- ❌ Attacking production systems without authorization

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/ascii-unicode-exploit-kit.git
cd ascii-unicode-exploit-kit

# Run the demo
python demo.py

# Generate a homoglyph attack
python src/unicode_generator.py --mode homoglyph --text "admin" --output result.txt

# Create ASCII art payload
python src/ascii_obfuscator.py --payload "sensitive" --mode box --style double

# Mix encoding layers
python src/string_mixer.py --input "target" --layers 3
```

## 📦 Components

| Tool | Description | Use Case |
|------|-------------|----------|
| `unicode_generator.py` | Homoglyphs, Bidi overrides, Zero-width chars | Tokenizer evasion |
| `ascii_obfuscator.py` | ASCII art, glitch text, Zalgo | Visual deception |
| `string_mixer.py` | Multi-layer encoding, polyglots | Deep obfuscation |

## 📖 Documentation

- [Technical Write-up](docs/WRITEUP.md) - Comprehensive analysis of Unicode exploitation
- [Examples](examples/) - Sample attack strings and patterns
- [Demo](demo.py) - Interactive demonstration of all features

## 🎯 Attack Vectors

### Homoglyph Attacks
Replace Latin characters with visually identical Unicode look-alikes:
```
Visual: "password"
Actual: "pаsswоrd" (Cyrillic а and о)
```

### Bidirectional Overrides
Manipulate text direction to spoof file extensions:
```
Visual: "invoice.pdf"
Actual: "invoice‮fdp.exe‭"
```

### Zero-Width Fingerprinting
Embed invisible tracking data:
```python
# Embed user ID 12345 invisibly
fingerprinted = generator.fingerprint_embed("Hello", 12345)
```

## 🔬 Research Context

This toolkit was developed as part of adversarial ML research focusing on:
- Input validation bypass techniques
- Tokenization edge cases in LLMs
- Visual spoofing in security interfaces
- Cross-system normalization inconsistencies

## 🦀 The 13th Hour Principle

> *"Scare all the baby clwbots."*

This toolkit operates on the principle that systems are most vulnerable during liminal spaces—between validation layers, between human and machine perception, between intended functionality and emergent behavior.

## 📄 License

MIT License with Ethical Use Addendum - see [LICENSE](LICENSE) for details.

## 👤 Author

**frankSx** - Security Researcher & CTF Enthusiast
- 📝 Blog: https://frankhacks.blogspot.com
- 🐙 GitHub: [your-handle]

---

*Generated for research purposes. Use responsibly.*
