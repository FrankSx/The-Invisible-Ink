#!/usr/bin/env python3
"""
Test Suite for ASCII Unicode Exploit Kit
Validates all functionality and attack vectors

Author: frankSx
13th Hour Research Division
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from unicode_generator import UnicodeExploitGenerator
from ascii_obfuscator import ASCIIObfuscator
from string_mixer import StringMixer
from unicode_analyzer import UnicodeAnalyzer


class TestUnicodeGenerator(unittest.TestCase):
    """Test Unicode exploit generation"""

    def setUp(self):
        self.gen = UnicodeExploitGenerator(seed=42)

    def test_homoglyph_replace(self):
        result = self.gen.homoglyph_replace("password", intensity=1.0)
        self.assertNotEqual(result, "password")
        self.assertEqual(len(result), len("password"))

    def test_zero_width_insertion(self):
        result = self.gen.insert_zero_width("test", density=1.0)
        self.assertIn('\u200B', result)  # ZWS
        self.assertGreater(len(result), 4)

    def test_bidi_override(self):
        result = self.gen.bidi_override("test", mode='rtl')
        self.assertIn('\u202E', result)  # RLO
        self.assertIn('\u202C', result)  # PDF

    def test_fingerprint_embed_extract(self):
        text = "Hello World"
        identifier = 12345
        embedded = self.gen.fingerprint_embed(text, identifier)
        extracted = self.gen.extract_fingerprint(embedded)
        self.assertEqual(extracted, identifier)

    def test_normalization_attack(self):
        text = "café"  # With combining acute
        results = self.gen.normalization_attack(text)
        self.assertIn('nfc', results)
        self.assertIn('nfd', results)


class TestASCIIObfuscator(unittest.TestCase):
    """Test ASCII art obfuscation"""

    def setUp(self):
        self.obf = ASCIIObfuscator(seed=42)

    def test_create_box(self):
        result = self.obf.create_box("test", style='single')
        self.assertIn('┌', result)
        self.assertIn('┐', result)
        self.assertIn('└', result)
        self.assertIn('┘', result)
        self.assertIn('test', result)

    def test_create_banner(self):
        result = self.obf.create_banner("test", style='double')
        self.assertIn('╔', result)
        self.assertIn('╗', result)
        self.assertIn('TEST', result)  # Uppercase

    def test_glitch_text(self):
        result = self.obf.create_glitch_text("test", intensity=0.5)
        self.assertNotEqual(result, "test")
        # Should contain combining characters
        self.assertGreater(len(result), 4)

    def test_zalgo(self):
        result = self.obf.create_zalgo("test", intensity=3)
        self.assertNotEqual(result, "test")


class TestStringMixer(unittest.TestCase):
    """Test string mixing and encoding"""

    def setUp(self):
        self.mixer = StringMixer(seed=42)

    def test_mix_layers(self):
        result = self.mixer.mix("test", layers=3)
        self.assertIn('original', result)
        self.assertIn('final', result)
        self.assertIn('techniques', result)
        self.assertEqual(result['layers'], 3)

    def test_base64(self):
        result = self.mixer._base64_encode("test")
        self.assertEqual(result, "dGVzdA==")

    def test_rot13(self):
        result = self.mixer._rot13("Hello")
        self.assertEqual(result, "Uryyb")

    def test_reverse(self):
        result = self.mixer._reverse("hello")
        self.assertEqual(result, "olleh")

    def test_create_polyglot(self):
        result = self.mixer.create_polyglot("test")
        self.assertIn('#!/bin/sh', result)
        self.assertIn('test', result)


class TestUnicodeAnalyzer(unittest.TestCase):
    """Test Unicode analysis"""

    def setUp(self):
        self.analyzer = UnicodeAnalyzer()

    def test_clean_text(self):
        analysis = self.analyzer.analyze("Hello World")
        self.assertEqual(analysis['risk_score'], 0)
        self.assertFalse(analysis['recommendations'][0].startswith('CRITICAL'))

    def test_bidi_detection(self):
        text = "Hello\u202EWorld\u202C"
        analysis = self.analyzer.analyze(text)
        self.assertGreater(len(analysis['bidi_chars']), 0)
        self.assertGreater(analysis['risk_score'], 0)

    def test_zero_width_detection(self):
        text = "Hello\u200BWorld"
        analysis = self.analyzer.analyze(text)
        self.assertGreater(len(analysis['zero_width']), 0)

    def test_homoglyph_detection(self):
        text = "pаssword"  # Cyrillic 'а'
        analysis = self.analyzer.analyze(text)
        self.assertGreater(len(analysis['homoglyphs']), 0)

    def test_mixed_scripts(self):
        text = "HelloМир"  # Latin + Cyrillic
        analysis = self.analyzer.analyze(text)
        self.assertTrue(analysis['mixed_scripts']['is_mixed'])


class TestIntegration(unittest.TestCase):
    """Integration tests - full attack chains"""

    def test_full_obfuscation_chain(self):
        """Test complete obfuscation pipeline"""
        gen = UnicodeExploitGenerator(seed=42)
        obf = ASCIIObfuscator(seed=42)
        mixer = StringMixer(seed=42)
        analyzer = UnicodeAnalyzer()

        # Step 1: Homoglyph replacement
        text = gen.homoglyph_replace("admin", intensity=0.7)

        # Step 2: ASCII art wrapping
        text = obf.create_box(text, style='single')

        # Step 3: Multi-layer encoding
        mixed = mixer.mix(text, layers=2)

        # Step 4: Analyze result
        analysis = analyzer.analyze(mixed['final'])

        # Should have elevated risk score
        self.assertGreater(analysis['risk_score'], 0)

    def test_invisible_fingerprint_chain(self):
        """Test fingerprinting through multiple transformations"""
        gen = UnicodeExploitGenerator(seed=42)

        original = "Sensitive message"
        user_id = 1337

        # Embed fingerprint
        fingerprinted = gen.fingerprint_embed(original, user_id)

        # Apply other transformations
        transformed = gen.homoglyph_replace(fingerprinted, intensity=0.3)

        # Should still be extractable
        extracted = gen.extract_fingerprint(transformed)
        self.assertEqual(extracted, user_id)


def run_tests():
    """Run all tests with verbose output"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestUnicodeGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestASCIIObfuscator))
    suite.addTests(loader.loadTestsFromTestCase(TestStringMixer))
    suite.addTests(loader.loadTestsFromTestCase(TestUnicodeAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
