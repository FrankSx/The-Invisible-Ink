#!/usr/bin/env python3
"""
Demo script showing ASCII Unicode Exploit Kit capabilities
Run this to see examples of all techniques
"""

import sys
sys.path.insert(0, 'src')

from unicode_generator import UnicodeExploitGenerator
from ascii_obfuscator import ASCIIObfuscator
from string_mixer import StringMixer

def main():
    print("=" * 60)
    print("ASCII UNICODE EXPLOIT KIT - DEMO")
    print("13th Hour Research Division | frankSx")
    print("=" * 60)

    # Unicode Generator Demo
    print("\n[1] UNICODE EXPLOIT GENERATOR")
    print("-" * 40)

    gen = UnicodeExploitGenerator(seed=42)
    test_string = "password123"

    print(f"Original: {test_string}")
    print(f"Homoglyph: {gen.homoglyph_replace(test_string, 0.5)}")
    print(f"Zero-width: {gen.insert_zero_width(test_string, 0.3)}")
    print(f"Bidi RTL: {gen.bidi_override(test_string, 'rtl')}")

    # ASCII Obfuscator Demo
    print("\n[2] ASCII OBFUSCATOR")
    print("-" * 40)

    obf = ASCIIObfuscator(seed=42)
    payload = "SECRET"

    print("Box style:")
    print(obf.create_box(payload, 'double'))

    print("\nGlitch text:")
    print(obf.create_glitch_text(payload, 0.4))

    # String Mixer Demo
    print("\n[3] STRING MIXER")
    print("-" * 40)

    mixer = StringMixer(seed=42)
    result = mixer.mix("attack", layers=3)

    print(f"Original: {result['original']}")
    print(f"Techniques: {', '.join(result['techniques'])}")
    print(f"Final: {result['final']}")

    print("\n" + "=" * 60)
    print("Demo complete. See docs/WRITEUP.md for full documentation.")
    print("=" * 60)

if __name__ == '__main__':
    main()
