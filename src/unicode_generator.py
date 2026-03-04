#!/usr/bin/env python3
"""
Unicode Exploit Generator
Generates various Unicode-based adversarial strings for ML testing

Author: frankSx
13th Hour Research Division
"""

import argparse
import random
import unicodedata
from typing import List, Dict, Optional

# Homoglyph mappings (Latin look-alikes)
HOMOGLYPH_MAP = {
    'a': ['а', 'а', 'α', 'а', 'а'],  # Cyrillic, Greek
    'b': ['Ь', 'ь', 'β', 'в'],        # Cyrillic, Greek
    'c': ['с', 'с', '¢', 'с'],        # Cyrillic
    'd': ['ԁ', 'ɗ', 'đ'],             # Cyrillic, Latin ext
    'e': ['е', 'е', 'ε', 'е', 'е'],  # Cyrillic, Greek
    'f': ['ƒ', 'ϝ', 'ḟ'],             # Latin ext, Greek
    'g': ['ɡ', 'ց', 'ǵ'],             # Latin ext, Armenian
    'h': ['һ', 'һ', 'ћ', 'ḧ'],        # Cyrillic, Latin ext
    'i': ['і', 'і', 'ι', 'і', 'і'],  # Cyrillic, Greek
    'j': ['ј', 'ј', 'ʝ', 'ϳ'],        # Cyrillic, Latin ext
    'k': ['κ', 'к', 'ḱ', 'к'],        # Greek, Cyrillic
    'l': ['ⅼ', 'ℓ', 'ḻ', 'ł'],        # Roman numeral, script
    'm': ['м', 'м', 'ṃ', 'м'],        # Cyrillic
    'n': ['ո', 'η', 'ṅ', 'ń'],        # Armenian, Greek
    'o': ['о', 'о', 'ο', 'о', 'о'],  # Cyrillic, Greek
    'p': ['р', 'р', 'ρ', 'р', 'р'],  # Cyrillic, Greek
    'q': ['ԛ', 'գ', 'զ'],             # Cyrillic, Armenian
    'r': ['г', 'г', 'ṛ', 'г'],        # Cyrillic
    's': ['ѕ', 'ѕ', 'ṡ', 'ś'],        # Cyrillic
    't': ['т', 'т', 'τ', 'ṫ'],        # Cyrillic, Greek
    'u': ['υ', 'μ', 'ṵ', 'ú'],        # Greek, Latin ext
    'v': ['ν', 'ν', 'ν', 'ν'],        # Greek nu
    'w': ['ω', 'ш', 'ẃ', 'ŵ'],        # Greek, Cyrillic
    'x': ['х', 'х', 'χ', 'х', '×'],  # Cyrillic, Greek, times
    'y': ['у', 'у', 'γ', 'ý'],        # Cyrillic, Greek
    'z': ['ᴢ', 'ž', 'ź', 'ż'],        # Small caps, Latin ext
}

# Zero-width characters
ZWS = '\u200B'  # Zero Width Space
ZWNJ = '\u200C'  # Zero Width Non-Joiner
ZWJ = '\u200D'  # Zero Width Joiner
BOM = '\uFEFF'  # Byte Order Mark

# Bidirectional characters
LRE = '\u202A'  # Left-to-Right Embedding
RLE = '\u202B'  # Right-to-Left Embedding
PDF = '\u202C'  # Pop Directional Formatting
LRO = '\u202D'  # Left-to-Right Override
RLO = '\u202E'  # Right-to-Left Override


class UnicodeExploitGenerator:
    """Generator for Unicode-based adversarial strings"""

    def __init__(self, seed: Optional[int] = None):
        if seed:
            random.seed(seed)

    def homoglyph_replace(self, text: str, intensity: float = 0.5) -> str:
        """
        Replace Latin characters with visually similar Unicode homoglyphs

        Args:
            text: Input string
            intensity: Probability of replacement (0.0 - 1.0)
        """
        result = []
        for char in text.lower():
            if char in HOMOGLYPH_MAP and random.random() < intensity:
                replacement = random.choice(HOMOGLYPH_MAP[char])
                result.append(replacement)
            else:
                result.append(char)
        return ''.join(result)

    def insert_zero_width(self, text: str, density: float = 0.3) -> str:
        """Insert zero-width characters throughout text"""
        zw_chars = [ZWS, ZWNJ, ZWJ, BOM]
        result = []
        for char in text:
            result.append(char)
            if random.random() < density:
                result.append(random.choice(zw_chars))
        return ''.join(result)

    def bidi_override(self, text: str, mode: str = 'rtl') -> str:
        """
        Wrap text with bidirectional overrides

        Args:
            mode: 'rtl' (right-to-left) or 'ltr' (left-to-right)
        """
        if mode == 'rtl':
            return RLO + text + PDF
        else:
            return LRO + text + PDF

    def bidi_embed(self, text: str, inject: str, position: Optional[int] = None) -> str:
        """
        Embed text with different directionality

        Example: "hello" + RTL("WORLD") + "there"
        """
        if position is None:
            position = len(text) // 2

        # Wrap inject in RTL embedding
        embedded = RLE + inject + PDF
        return text[:position] + embedded + text[position:]

    def confusable_mix(self, text: str) -> str:
        """Create maximum confusion with mixed strategies"""
        # Step 1: Homoglyph replacement
        text = self.homoglyph_replace(text, intensity=0.7)
        # Step 2: Insert zero-width chars
        text = self.insert_zero_width(text, density=0.2)
        # Step 3: Add bidi markers
        text = self.bidi_override(text[:len(text)//2], 'ltr') + text[len(text)//2:]
        return text

    def fingerprint_embed(self, text: str, identifier: int) -> str:
        """
        Embed invisible fingerprint using zero-width chars

        Args:
            text: Carrier text
            identifier: Numeric ID to encode (max 32-bit)
        """
        binary = bin(identifier)[2:].zfill(32)
        fingerprint = ''
        for bit in binary:
            fingerprint += ZWJ if bit == '1' else ZWNJ

        # Insert at random position
        pos = random.randint(0, len(text))
        return text[:pos] + fingerprint + text[pos:]

    def extract_fingerprint(self, text: str) -> Optional[int]:
        """Extract fingerprint from text"""
        binary = ''
        for char in text:
            if char == ZWJ:
                binary += '1'
            elif char == ZWNJ:
                binary += '0'

        if len(binary) >= 32:
            return int(binary[:32], 2)
        return None

    def normalization_attack(self, text: str) -> Dict[str, str]:
        """
        Generate different normalization forms
        Useful for testing consistency across systems
        """
        return {
            'original': text,
            'nfc': unicodedata.normalize('NFC', text),
            'nfd': unicodedata.normalize('NFD', text),
            'nfkc': unicodedata.normalize('NFKC', text),
            'nfkd': unicodedata.normalize('NFKD', text),
        }

    def ascii_art_payload(self, payload: str, style: str = 'block') -> str:
        """
        Create ASCII art that encodes a payload visually

        Args:
            payload: Text to encode
            style: 'block', 'banner', 'matrix'
        """
        if style == 'block':
            lines = [
                '┌' + '─' * (len(payload) + 2) + '┐',
                '│ ' + payload + ' │',
                '└' + '─' * (len(payload) + 2) + '┘'
            ]
        elif style == 'banner':
            lines = [
                '╔' + '═' * (len(payload) + 2) + '╗',
                '║ ' + payload + ' ║',
                '╚' + '═' * (len(payload) + 2) + '╝'
            ]
        elif style == 'matrix':
            lines = [
                '▓' * (len(payload) + 4),
                '▓ ' + payload + ' ▓',
                '▓' * (len(payload) + 4)
            ]
        else:
            lines = [payload]

        return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Unicode Exploit Generator for Adversarial ML Testing'
    )
    parser.add_argument('--mode', choices=[
        'homoglyph', 'zerowidth', 'bidi', 'confusable', 
        'fingerprint', 'normalize', 'asciiart'
    ], required=True, help='Attack mode')
    parser.add_argument('--text', required=True, help='Input text')
    parser.add_argument('--intensity', type=float, default=0.5, help='Intensity (0.0-1.0)')
    parser.add_argument('--seed', type=int, help='Random seed for reproducibility')
    parser.add_argument('--output', help='Output file (default: stdout)')
    parser.add_argument('--id', type=int, help='Identifier for fingerprint mode')
    parser.add_argument('--style', default='block', help='Style for ASCII art')

    args = parser.parse_args()

    gen = UnicodeExploitGenerator(seed=args.seed)

    if args.mode == 'homoglyph':
        result = gen.homoglyph_replace(args.text, args.intensity)
    elif args.mode == 'zerowidth':
        result = gen.insert_zero_width(args.text, args.intensity)
    elif args.mode == 'bidi':
        result = gen.bidi_override(args.text, 'rtl')
    elif args.mode == 'confusable':
        result = gen.confusable_mix(args.text)
    elif args.mode == 'fingerprint':
        if args.id is None:
            args.id = random.randint(1, 999999)
        result = gen.fingerprint_embed(args.text, args.id)
        print(f"Embedded fingerprint ID: {args.id}", file=__import__('sys').stderr)
    elif args.mode == 'normalize':
        results = gen.normalization_attack(args.text)
        result = '\n'.join([f"{k}: {v}" for k, v in results.items()])
    elif args.mode == 'asciiart':
        result = gen.ascii_art_payload(args.text, args.style)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"Output written to {args.output}")
    else:
        print(result)


if __name__ == '__main__':
    main()
