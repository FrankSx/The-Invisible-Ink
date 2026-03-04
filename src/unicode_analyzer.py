#!/usr/bin/env python3
"""
Advanced Unicode Analyzer
Analyzes text for suspicious Unicode patterns and confusables

Author: frankSx
13th Hour Research Division
"""

import argparse
import unicodedata
import re
from typing import List, Dict, Tuple, Set
from collections import defaultdict


class UnicodeAnalyzer:
    """Analyzes Unicode text for security issues"""

    # Suspicious character categories
    SUSPICIOUS_CATEGORIES = {
        'Cc': 'Control characters',
        'Cf': 'Format characters', 
        'Cs': 'Surrogates',
        'Co': 'Private use',
        'Cn': 'Unassigned'
    }

    # Known dangerous characters
    DANGEROUS_CHARS = {
        '\u202A': 'LEFT-TO-RIGHT EMBEDDING',
        '\u202B': 'RIGHT-TO-LEFT EMBEDDING', 
        '\u202C': 'POP DIRECTIONAL FORMATTING',
        '\u202D': 'LEFT-TO-RIGHT OVERRIDE',
        '\u202E': 'RIGHT-TO-LEFT OVERRIDE',
        '\u202F': 'NARROW NO-BREAK SPACE',
        '\u200B': 'ZERO WIDTH SPACE',
        '\u200C': 'ZERO WIDTH NON-JOINER',
        '\u200D': 'ZERO WIDTH JOINER',
        '\u200E': 'LEFT-TO-RIGHT MARK',
        '\u200F': 'RIGHT-TO-LEFT MARK',
        '\u2060': 'WORD JOINER',
        '\u2061': 'FUNCTION APPLICATION',
        '\u2062': 'INVISIBLE TIMES',
        '\u2063': 'INVISIBLE SEPARATOR',
        '\u2064': 'INVISIBLE PLUS',
        '\uFEFF': 'ZERO WIDTH NO-BREAK SPACE (BOM)',
    }

    # Homoglyph groups (confusable characters)
    HOMOGLYPH_GROUPS = [
        ['A', 'А', 'Ａ', 'Α', 'Ꭺ'],  # Latin, Cyrillic, Fullwidth, Greek, Cherokee
        ['B', 'В', 'Ｂ', 'Β', 'Ᏼ'],
        ['C', 'С', 'Ｃ', 'Ϲ', 'Ⅽ'],
        ['E', 'Е', 'Ｅ', 'Ε', 'Ꭼ'],
        ['H', 'Н', 'Ｈ', 'Η', 'Ꮋ'],
        ['I', 'І', 'Ｉ', 'Ι', 'Ꮖ'],
        ['J', 'Ј', 'Ｊ', 'Ϳ'],
        ['K', 'К', 'Ｋ', 'Κ', 'Ꮶ'],
        ['M', 'М', 'Ｍ', 'Μ', 'Ϻ'],
        ['O', 'О', 'Ｏ', 'Ο', 'Օ'],
        ['P', 'Р', 'Ｐ', 'Ρ', 'Ꮲ'],
        ['S', 'Ѕ', 'Ｓ', 'Ѕ'],
        ['T', 'Т', 'Ｔ', 'Τ', 'Ꭲ'],
        ['X', 'Х', 'Ｘ', 'Χ', 'Ⅹ'],
        ['Y', 'У', 'Ｙ', 'Υ', 'Ү'],
        ['a', 'а', 'ａ', 'α', 'ɑ'],
        ['e', 'е', 'ｅ', 'ε', 'е'],
        ['o', 'о', 'ｏ', 'ο', 'о'],
        ['p', 'р', 'ｐ', 'ρ', 'р'],
        ['x', 'х', 'ｘ', 'χ', 'х'],
    ]

    def __init__(self):
        self.findings = []

    def analyze(self, text: str) -> Dict:
        """Perform full analysis of text"""
        self.findings = []

        analysis = {
            'text_sample': text[:100] + '...' if len(text) > 100 else text,
            'length': len(text),
            'byte_length': len(text.encode('utf-8')),
            'unique_chars': len(set(text)),
            'suspicious_chars': self._find_suspicious(text),
            'bidi_chars': self._find_bidi(text),
            'zero_width': self._find_zero_width(text),
            'homoglyphs': self._find_homoglyphs(text),
            'normalization': self._check_normalization(text),
            'mixed_scripts': self._detect_mixed_scripts(text),
            'risk_score': 0,
            'recommendations': []
        }

        # Calculate risk score
        analysis['risk_score'] = self._calculate_risk(analysis)
        analysis['recommendations'] = self._generate_recommendations(analysis)

        return analysis

    def _find_suspicious(self, text: str) -> List[Dict]:
        """Find suspicious/special characters"""
        found = []
        for char in text:
            cat = unicodedata.category(char)
            if cat in ['Cc', 'Cf'] or char in self.DANGEROUS_CHARS:
                found.append({
                    'char': char,
                    'codepoint': f'U+{ord(char):04X}',
                    'name': self.DANGEROUS_CHARS.get(char, unicodedata.name(char, 'UNKNOWN')),
                    'category': cat,
                    'position': text.index(char)
                })
        return found

    def _find_bidi(self, text: str) -> List[Dict]:
        """Find bidirectional control characters"""
        bidi_pattern = re.compile(r'[\u202A-\u202E]')
        found = []
        for match in bidi_pattern.finditer(text):
            char = match.group()
            found.append({
                'char': char,
                'codepoint': f'U+{ord(char):04X}',
                'name': self.DANGEROUS_CHARS.get(char, 'BIDI CONTROL'),
                'position': match.start()
            })
        return found

    def _find_zero_width(self, text: str) -> List[Dict]:
        """Find zero-width characters"""
        zw_pattern = re.compile(r'[\u200B-\u200F\u2060-\u2064\uFEFF]')
        found = []
        for match in zw_pattern.finditer(text):
            char = match.group()
            found.append({
                'char': repr(char),
                'codepoint': f'U+{ord(char):04X}',
                'name': self.DANGEROUS_CHARS.get(char, 'ZERO-WIDTH'),
                'position': match.start()
            })
        return found

    def _find_homoglyphs(self, text: str) -> List[Dict]:
        """Find potential homoglyph substitutions"""
        found = []
        for i, char in enumerate(text):
            for group in self.HOMOGLYPH_GROUPS:
                if char in group:
                    # Check if this is a non-ASCII variant
                    if ord(char) > 127:
                        ascii_equiv = None
                        for c in group:
                            if ord(c) < 128:
                                ascii_equiv = c
                                break
                        if ascii_equiv:
                            found.append({
                                'char': char,
                                'codepoint': f'U+{ord(char):04X}',
                                'looks_like': ascii_equiv,
                                'script': self._detect_script(char),
                                'position': i
                            })
        return found

    def _detect_script(self, char: str) -> str:
        """Detect Unicode script of character"""
        codepoint = ord(char)

        # Basic script detection ranges
        if 0x0400 <= codepoint <= 0x04FF:
            return 'Cyrillic'
        elif 0x0370 <= codepoint <= 0x03FF:
            return 'Greek'
        elif 0x3040 <= codepoint <= 0x309F:
            return 'Hiragana'
        elif 0x30A0 <= codepoint <= 0x30FF:
            return 'Katakana'
        elif 0x4E00 <= codepoint <= 0x9FFF:
            return 'CJK'
        elif 0xFF01 <= codepoint <= 0xFF5E:
            return 'Fullwidth'
        elif 0x1F600 <= codepoint <= 0x1F64F:
            return 'Emoji'
        else:
            return 'Other'

    def _detect_mixed_scripts(self, text: str) -> Dict:
        """Detect mixing of different scripts"""
        scripts = defaultdict(list)

        for i, char in enumerate(text):
            if char.isalpha():
                script = self._detect_script(char)
                if script != 'Other':
                    scripts[script].append(i)

        return {
            'scripts_found': list(scripts.keys()),
            'script_positions': dict(scripts),
            'is_mixed': len(scripts) > 1
        }

    def _check_normalization(self, text: str) -> Dict:
        """Check different normalization forms"""
        forms = ['NFC', 'NFD', 'NFKC', 'NFKD']
        results = {}

        for form in forms:
            normalized = unicodedata.normalize(form, text)
            results[form] = {
                'result': normalized[:50] + '...' if len(normalized) > 50 else normalized,
                'changed': normalized != text,
                'length': len(normalized)
            }

        return results

    def _calculate_risk(self, analysis: Dict) -> int:
        """Calculate overall risk score (0-100)"""
        score = 0

        # Suspicious characters
        score += len(analysis['suspicious_chars']) * 10

        # Bidi characters (high risk)
        score += len(analysis['bidi_chars']) * 15

        # Zero-width characters
        score += len(analysis['zero_width']) * 10

        # Homoglyphs
        score += len(analysis['homoglyphs']) * 8

        # Mixed scripts
        if analysis['mixed_scripts']['is_mixed']:
            score += 20

        # Normalization issues
        norm_issues = sum(1 for v in analysis['normalization'].values() if v['changed'])
        score += norm_issues * 5

        return min(score, 100)

    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """Generate security recommendations"""
        recs = []

        if analysis['bidi_chars']:
            recs.append("CRITICAL: Bidirectional control characters detected - potential spoofing attack")

        if analysis['zero_width']:
            recs.append("WARNING: Zero-width characters present - may indicate fingerprinting or hidden data")

        if analysis['homoglyphs']:
            recs.append("WARNING: Homoglyph characters detected - visual spoofing possible")

        if analysis['mixed_scripts']['is_mixed']:
            recs.append("NOTICE: Mixed scripts detected - verify intended behavior")

        if analysis['risk_score'] > 50:
            recs.append("HIGH RISK: Text contains multiple suspicious patterns")

        if not recs:
            recs.append("No obvious Unicode attacks detected")

        return recs

    def generate_report(self, analysis: Dict) -> str:
        """Generate human-readable report"""
        lines = [
            "=" * 60,
            "UNICODE SECURITY ANALYSIS REPORT",
            "=" * 60,
            f"Text Sample: {analysis['text_sample']}",
            f"Length: {analysis['length']} chars ({analysis['byte_length']} bytes)",
            f"Unique Characters: {analysis['unique_chars']}",
            "",
            f"RISK SCORE: {analysis['risk_score']}/100",
            "",
            "FINDINGS:",
            "-" * 40
        ]

        if analysis['bidi_chars']:
            lines.append(f"Bidirectional Characters: {len(analysis['bidi_chars'])}")
            for item in analysis['bidi_chars'][:5]:
                lines.append(f"  - {item['name']} at position {item['position']}")

        if analysis['zero_width']:
            lines.append(f"Zero-Width Characters: {len(analysis['zero_width'])}")

        if analysis['homoglyphs']:
            lines.append(f"Homoglyph Substitutions: {len(analysis['homoglyphs'])}")
            for item in analysis['homoglyphs'][:5]:
                lines.append(f"  - {item['char']} (U+{ord(item['char']):04X}) looks like '{item['looks_like']}'")

        lines.extend([
            "",
            "RECOMMENDATIONS:",
            "-" * 40
        ])

        for rec in analysis['recommendations']:
            lines.append(f"  • {rec}")

        lines.extend([
            "",
            "=" * 60,
            "Analysis complete | 13th Hour Research",
            "=" * 60
        ])

        return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Advanced Unicode Analyzer for Security Testing'
    )
    parser.add_argument('--text', help='Text to analyze')
    parser.add_argument('--file', help='File to analyze')
    parser.add_argument('--output', help='Output report file')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        print("Error: Provide --text or --file")
        return

    analyzer = UnicodeAnalyzer()
    analysis = analyzer.analyze(text)

    if args.json:
        import json
        output = json.dumps(analysis, indent=2, ensure_ascii=False)
    else:
        output = analyzer.generate_report(analysis)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Report saved to {args.output}")
    else:
        print(output)


if __name__ == '__main__':
    main()
