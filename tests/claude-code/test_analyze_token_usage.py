import os
import unittest
import importlib.util

# Dynamically load analyze-token-usage.py since it has hyphens in the name
current_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.join(current_dir, "analyze-token-usage.py")

spec = importlib.util.spec_from_file_location("analyze_token_usage", module_path)
analyze_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(analyze_module)

class TestAnalyzeTokenUsage(unittest.TestCase):
    def test_format_tokens(self):
        """Test formatting token counts with thousands separators."""
        # Zero
        self.assertEqual(analyze_module.format_tokens(0), "0")

        # Small numbers (no separators)
        self.assertEqual(analyze_module.format_tokens(999), "999")
        self.assertEqual(analyze_module.format_tokens(1), "1")

        # Thousands
        self.assertEqual(analyze_module.format_tokens(1000), "1,000")
        self.assertEqual(analyze_module.format_tokens(9999), "9,999")

        # Millions
        self.assertEqual(analyze_module.format_tokens(1234567), "1,234,567")
        self.assertEqual(analyze_module.format_tokens(1000000), "1,000,000")

        # Negative numbers
        self.assertEqual(analyze_module.format_tokens(-1000), "-1,000")
        self.assertEqual(analyze_module.format_tokens(-1234567), "-1,234,567")

        # Floating point numbers
        self.assertEqual(analyze_module.format_tokens(1234.56), "1,234.56")
        self.assertEqual(analyze_module.format_tokens(1000.0), "1,000.0")

if __name__ == '__main__':
    unittest.main()
