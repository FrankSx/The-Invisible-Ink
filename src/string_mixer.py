#!/usr/bin/env python3
"""
Adversarial String Mixer
Combines multiple encoding strategies for maximum evasion

Author: frankSx
13th Hour Research Division
"""

import argparse
import base64
import random
import hashlib
from typing import List, Dict, Callable


class StringMixer:
    """Combines multiple obfuscation techniques"""

    def __init__(self, seed: int = None):
        if seed:
            random.seed(seed)
        self.techniques = {
            'base64': self._base64_encode,
            'rot13': self._rot13,
            'reverse': self._reverse,
            'unicode_escape': self._unicode_escape,
            'hex': self._hex_encode,
            'url': self._url_encode,
            'morse': self._morse_encode,
            'binary': self._binary_encode,
        }

    def _base64_encode(self, s: str) -> str:
        return base64.b64encode(s.encode()).decode()

    def _rot13(self, s: str) -> str:
        return s.translate(str.maketrans(
            'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
            'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm'
        ))

    def _reverse(self, s: str) -> str:
        return s[::-1]

    def _unicode_escape(self, s: str) -> str:
        return ''.join(f'\\u{ord(c):04x}' for c in s)

    def _hex_encode(self, s: str) -> str:
        return s.encode().hex()

    def _url_encode(self, s: str) -> str:
        return ''.join(f'%{ord(c):02x}' if ord(c) > 127 or c in ' %&=' else c for c in s)

    def _morse_encode(self, s: str) -> str:
        morse = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
            'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
            'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
            'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
            'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
            '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
            '9': '----.', '0': '-----', ' ': '/'
        }
        return ' '.join(morse.get(c.upper(), c) for c in s)

    def _binary_encode(self, s: str) -> str:
        return ' '.join(format(ord(c), '08b') for c in s)

    def mix(self, text: str, layers: int = 3, techniques: List[str] = None) -> Dict:
        """
        Apply multiple encoding layers

        Args:
            text: Input string
            layers: Number of encoding layers
            techniques: Specific techniques to use (random if None)
        """
        if techniques is None:
            techniques = random.sample(list(self.techniques.keys()), 
                                      min(layers, len(self.techniques)))

        current = text
        history = [('original', text)]

        for tech in techniques[:layers]:
            if tech in self.techniques:
                current = self.techniques[tech](current)
                history.append((tech, current))

        return {
            'original': text,
            'final': current,
            'layers': len(history) - 1,
            'techniques': [h[0] for h in history[1:]],
            'history': history,
            'hash': hashlib.sha256(current.encode()).hexdigest()[:16]
        }

    def create_polyglot(self, text: str) -> str:
        """
        Create a polyglot that works in multiple contexts

        Example: Valid as Python, JavaScript, and Bash
        """
        # Comment-based polyglot
        lines = [
            '#!/bin/sh',
            '/*',
            ':',
            text,
            '*/',
            'echo "' + text + '"'
        ]
        return '\n'.join(lines)

    def create_invisible_payload(self, text: str) -> str:
        """Create payload using only invisible/formatting characters"""
        # Map characters to zero-width/invisible Unicode
        invisible_map = {
            '0': '\u200B',
            '1': '\u200C',
            '2': '\u200D',
            '3': '\uFEFF',
        }

        binary = ''.join(format(ord(c), '08b') for c in text)
        groups = [binary[i:i+2] for i in range(0, len(binary), 2)]

        result = []
        for g in groups:
            val = int(g, 2)
            if val < 4:
                result.append(invisible_map.get(str(val), '\u200B'))

        return ''.join(result)

    def create_deceptive_comment(self, payload: str, cover_text: str = "Safe content") -> str:
        """
        Create a comment that looks safe but contains hidden payload
        """
        encoded = base64.b64encode(payload.encode()).decode()

        lines = [
            f"/* {cover_text} */",
            f"// Safe: {cover_text}",
            f"<!-- {cover_text} -->",
            f"# {cover_text}",
            f"<!-- Base64 data follows: {encoded} -->"
        ]

        return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Adversarial String Mixer for ML Testing'
    )
    parser.add_argument('--input', required=True, help='Input string')
    parser.add_argument('--layers', type=int, default=3, help='Number of encoding layers')
    parser.add_argument('--techniques', nargs='+', help='Specific techniques to use')
    parser.add_argument('--mode', choices=['mix', 'polyglot', 'invisible', 'comment'], 
                       default='mix', help='Operation mode')
    parser.add_argument('--cover', default="Safe content", help='Cover text for comment mode')
    parser.add_argument('--output', help='Output file')

    args = parser.parse_args()

    mixer = StringMixer()

    if args.mode == 'mix':
        result = mixer.mix(args.input, args.layers, args.techniques)
        output = f"""Mixed String Results
====================
Original: {result['original']}
Final: {result['final']}
Layers: {result['layers']}
Techniques: {', '.join(result['techniques'])}
Hash: {result['hash']}

History:
"""
        for tech, val in result['history']:
            output += f"  [{tech}] {val[:80]}{'...' if len(val) > 80 else ''}\n"

    elif args.mode == 'polyglot':
        output = mixer.create_polyglot(args.input)

    elif args.mode == 'invisible':
        output = mixer.create_invisible_payload(args.input)

    elif args.mode == 'comment':
        output = mixer.create_deceptive_comment(args.input, args.cover)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Output written to {args.output}")
    else:
        print(output)


if __name__ == '__main__':
    main()
