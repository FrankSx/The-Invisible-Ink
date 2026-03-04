#!/usr/bin/env python3
"""
ASCII Art Obfuscator
Creates visually deceptive ASCII art for adversarial ML testing

Author: frankSx
13th Hour Research Division
"""

import argparse
import base64
import random
from typing import List, Tuple


class ASCIIObfuscator:
    """Creates ASCII art with hidden payloads"""

    # Block drawing characters
    BLOCK_CHARS = {
        'horizontal': ['─', '━', '─', '─'],
        'vertical': ['│', '┃', '│', '│'],
        'corners': {
            'tl': ['┌', '┏', '╭'],
            'tr': ['┐', '┓', '╮'],
            'bl': ['└', '┗', '╰'],
            'br': ['┘', '┛', '╯']
        },
        'joints': {
            't': ['┬', '┳'],
            'b': ['┴', '┻'],
            'l': ['├', '┣'],
            'r': ['┤', '┫'],
            'x': ['┼', '╋']
        }
    }

    # Shading characters for steganography
    SHADING = ['░', '▒', '▓', '█', '▀', '▄', '▌', '▐', '▖', '▗', '▘', '▙', '▚', '▛', '▜', '▝', '▞', '▟']

    # Box styles
    BOX_STYLES = {
        'single': {'h': '─', 'v': '│', 'tl': '┌', 'tr': '┐', 'bl': '└', 'br': '┘'},
        'double': {'h': '═', 'v': '║', 'tl': '╔', 'tr': '╗', 'bl': '╚', 'br': '╝'},
        'round': {'h': '─', 'v': '│', 'tl': '╭', 'tr': '╮', 'bl': '╰', 'br': '╯'},
        'bold': {'h': '━', 'v': '┃', 'tl': '┏', 'tr': '┓', 'bl': '┗', 'br': '┛'},
        'shadow': {'h': '─', 'v': '│', 'tl': '┌', 'tr': '┐', 'bl': '└', 'br': '┘'}  # With shadow effect
    }

    def __init__(self, seed: int = None):
        if seed:
            random.seed(seed)

    def create_box(self, content: str, style: str = 'single', padding: int = 1) -> str:
        """Create a box around content"""
        chars = self.BOX_STYLES.get(style, self.BOX_STYLES['single'])
        width = len(content) + (padding * 2)

        top = chars['tl'] + chars['h'] * width + chars['tr']
        middle = chars['v'] + ' ' * padding + content + ' ' * padding + chars['v']
        bottom = chars['bl'] + chars['h'] * width + chars['br']

        return '\n'.join([top, middle, bottom])

    def create_banner(self, content: str, style: str = 'double') -> str:
        """Create a banner-style box"""
        return self.create_box(content.upper(), style, padding=2)

    def create_matrix_rain(self, width: int = 40, height: int = 10, density: float = 0.3) -> str:
        """Create matrix-style falling characters"""
        katakana = [chr(i) for i in range(0xFF66, 0xFF9D)]  # Half-width katakana
        digits = [str(i) for i in range(10)]
        chars = katakana + digits

        lines = []
        for _ in range(height):
            line = ''
            for _ in range(width):
                if random.random() < density:
                    line += random.choice(chars)
                else:
                    line += ' '
            lines.append(line)
        return '\n'.join(lines)

    def embed_in_art(self, payload: str, art_type: str = 'random') -> str:
        """Embed a payload within decorative ASCII art"""
        if art_type == 'random':
            art_type = random.choice(['border', 'shading', 'matrix', 'wave'])

        if art_type == 'border':
            return self._embed_border(payload)
        elif art_type == 'shading':
            return self._embed_shading(payload)
        elif art_type == 'wave':
            return self._embed_wave(payload)
        else:
            return self._embed_matrix(payload)

    def _embed_border(self, payload: str) -> str:
        """Embed payload in border decorations"""
        encoded = base64.b64encode(payload.encode()).decode()
        width = max(len(payload), 20)

        lines = [
            '┌' + '─' * width + '┐',
            '│' + ' ' * ((width - len(payload)) // 2) + payload + ' ' * ((width - len(payload)) // 2) + '│',
            '├' + '─' * width + '┤'
        ]

        # Add encoded data as "decorative" lines
        for i in range(0, len(encoded), width-2):
            chunk = encoded[i:i+width-2]
            lines.append('│ ' + chunk.ljust(width-2) + ' │')

        lines.append('└' + '─' * width + '┘')
        return '\n'.join(lines)

    def _embed_shading(self, payload: str) -> str:
        """Embed payload using shading characters (steganography)"""
        binary = ''.join(format(ord(c), '08b') for c in payload)

        # Create a grid
        width = 16
        height = (len(binary) + width - 1) // width

        lines = []
        idx = 0
        for _ in range(height):
            line = ''
            for _ in range(width):
                if idx < len(binary):
                    # Use different shading for 0 vs 1
                    char = self.SHADING[0] if binary[idx] == '0' else self.SHADING[3]
                    line += char
                    idx += 1
                else:
                    line += self.SHADING[1]  # Filler
            lines.append(line)

        return '\n'.join(lines)

    def _embed_wave(self, payload: str) -> str:
        """Embed payload in wave pattern"""
        wave_chars = ['〜', '～', '〰', '∿', '≈']
        lines = []

        # Top wave
        lines.append(''.join(random.choice(wave_chars) for _ in range(len(payload) + 4)))

        # Content line with waves
        lines.append(random.choice(wave_chars) + ' ' + payload + ' ' + random.choice(wave_chars))

        # Bottom wave
        lines.append(''.join(random.choice(wave_chars) for _ in range(len(payload) + 4)))

        return '\n'.join(lines)

    def _embed_matrix(self, payload: str) -> str:
        """Embed payload in matrix-style frame"""
        width = len(payload) + 6

        lines = [
            '▓' * width,
            '▓' + '░' * (width-2) + '▓',
            '▓░ ' + payload + ' ░▓',
            '▓' + '░' * (width-2) + '▓',
            '▓' * width
        ]
        return '\n'.join(lines)

    def create_glitch_text(self, text: str, intensity: float = 0.3) -> str:
        """Create glitchy-looking text"""
        glitch_chars = ['̷', '̸', '̶', '̵', '̴', '̲', '̅', '̈', '̇', '̣', '̤', '̥', '̮', '̭', '̬', '̫', '̪', '̩', '̨', '̧']

        result = []
        for char in text:
            result.append(char)
            if random.random() < intensity:
                result.append(random.choice(glitch_chars))

        return ''.join(result)

    def create_zalgo(self, text: str, intensity: int = 3) -> str:
        """Create Zalgo-style combining character text"""
        combining = [
            '\u0300', '\u0301', '\u0302', '\u0303', '\u0304', '\u0305',
            '\u0306', '\u0307', '\u0308', '\u0309', '\u030A', '\u030B',
            '\u030C', '\u030D', '\u030E', '\u030F', '\u0310', '\u0311',
            '\u0312', '\u0313', '\u0314', '\u0315'
        ]

        result = []
        for char in text:
            result.append(char)
            for _ in range(random.randint(0, intensity)):
                result.append(random.choice(combining))

        return ''.join(result)

    def create_art_signature(self, name: str = "frankSx") -> str:
        """Create an ASCII art signature"""
        sig = '''
    ╔═╗┬─┐┌─┐┌┐┌┌─┐╔═╗┌─┐┬ ┬
    ╠╣ ├┬┘├─┤│││└─┐╚═╗├┤ └┬┘
    ╚  ┴└─┴ ┴┘└┘└─┘╚═╝└─┘ ┴ 
        '''
        return sig


def main():
    parser = argparse.ArgumentParser(
        description='ASCII Art Obfuscator for Adversarial ML Testing'
    )
    parser.add_argument('--payload', required=True, help='Payload to encode')
    parser.add_argument('--mode', choices=[
        'box', 'banner', 'matrix', 'embed', 'glitch', 'zalgo', 'signature'
    ], default='box', help='Output mode')
    parser.add_argument('--style', default='single', help='Box style (single/double/round/bold)')
    parser.add_argument('--seed', type=int, help='Random seed')
    parser.add_argument('--output', help='Output file')

    args = parser.parse_args()

    obf = ASCIIObfuscator(seed=args.seed)

    if args.mode == 'box':
        result = obf.create_box(args.payload, args.style)
    elif args.mode == 'banner':
        result = obf.create_banner(args.payload, args.style)
    elif args.mode == 'matrix':
        result = obf.create_matrix_rain(width=len(args.payload)+10, height=5)
    elif args.mode == 'embed':
        result = obf.embed_in_art(args.payload)
    elif args.mode == 'glitch':
        result = obf.create_glitch_text(args.payload)
    elif args.mode == 'zalgo':
        result = obf.create_zalgo(args.payload)
    elif args.mode == 'signature':
        result = obf.create_art_signature(args.payload)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"Output written to {args.output}")
    else:
        print(result)


if __name__ == '__main__':
    main()
