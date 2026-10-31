"""
Standalone Unit Test Runner using Python's standard 'unittest' module.
Allows verifying all 8 core test requirements without external packages.
"""

import os
import re
import sys
import shutil
import tempfile
import unittest

from logger import KeystrokeLogger


class MockKeyEvent:
    def __init__(self, char: str = "", keysym: str = ""):
        self.char = char
        self.keysym = keysym


class TestKeystrokeLogger(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_log_path = os.path.join(self.temp_dir, "test_keylog.txt")
        self.logger = KeystrokeLogger(log_file_path=self.test_log_path)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_1_logging_starts_successfully(self):
        """1. Verify logging starts successfully and updates state."""
        self.assertFalse(self.logger.is_logging)
        started = self.logger.start_logging()
        self.assertTrue(started)
        self.assertTrue(self.logger.is_logging)
        # Starting again should return False
        self.assertFalse(self.logger.start_logging())

    def test_2_logging_stops_successfully(self):
        """2. Verify logging stops successfully and updates state."""
        self.logger.start_logging()
        self.assertTrue(self.logger.is_logging)
        stopped = self.logger.stop_logging()
        self.assertTrue(stopped)
        self.assertFalse(self.logger.is_logging)
        # Stopping again should return False
        self.assertFalse(self.logger.stop_logging())

    def test_3_typed_characters_are_recorded(self):
        """3. Verify alphanumeric characters are accurately recorded."""
        self.logger.start_logging()
        e1 = self.logger.record_event(MockKeyEvent(char="a", keysym="a"))
        e2 = self.logger.record_event(MockKeyEvent(char="Z", keysym="Z"))
        e3 = self.logger.record_event(MockKeyEvent(char="5", keysym="5"))
        e4 = self.logger.record_event(MockKeyEvent(char="!", keysym="exclam"))

        self.assertEqual(e1["key"], "a")
        self.assertEqual(e2["key"], "Z")
        self.assertEqual(e3["key"], "5")
        self.assertEqual(e4["key"], "!")
        self.assertEqual(self.logger.session_events_count, 4)

    def test_4_special_keys_represented_correctly(self):
        """4. Verify special keys map to standard readable tags."""
        self.logger.start_logging()
        test_cases = [
            (MockKeyEvent(char="", keysym="Return"), "[ENTER]"),
            (MockKeyEvent(char=" ", keysym="space"), "[SPACE]"),
            (MockKeyEvent(char="", keysym="BackSpace"), "[BACKSPACE]"),
            (MockKeyEvent(char="\t", keysym="Tab"), "[TAB]"),
            (MockKeyEvent(char="", keysym="Delete"), "[DELETE]"),
            (MockKeyEvent(char="", keysym="Escape"), "[ESCAPE]"),
        ]
        for event, expected in test_cases:
            rec = self.logger.record_event(event)
            self.assertEqual(rec["key"], expected)

    def test_5_timestamps_are_generated(self):
        """5. Verify timestamps follow YYYY-MM-DD HH:MM:SS format."""
        self.logger.start_logging()
        event = self.logger.record_event(MockKeyEvent(char="m", keysym="m"))
        timestamp = event["timestamp"]
        pattern = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"
        self.assertIsNotNone(re.match(pattern, timestamp))
        self.assertIn(timestamp, event["log_line"])

    def test_6_log_entries_saved_to_file(self):
        """6. Verify log entries are physically written to the configured file."""
        self.logger.start_logging()
        self.logger.record_event(MockKeyEvent(char="w", keysym="w"))
        self.logger.stop_logging()

        self.assertTrue(os.path.exists(self.test_log_path))
        content = self.logger.get_log_contents()
        self.assertIn("[SESSION START]", content)
        self.assertIn("Key: w", content)
        self.assertIn("[SESSION END]", content)
        self.assertIn("Total Keys Recorded: 1", content)

    def test_7_previous_log_entries_preserved(self):
        """7. Verify subsequent sessions append to file without overwriting."""
        self.logger.start_logging()
        self.logger.record_event(MockKeyEvent(char="A", keysym="A"))
        self.logger.stop_logging()

        self.logger.start_logging()
        self.logger.record_event(MockKeyEvent(char="B", keysym="B"))
        self.logger.stop_logging()

        content = self.logger.get_log_contents()
        self.assertEqual(content.count("[SESSION START]"), 2)
        self.assertEqual(content.count("[SESSION END]"), 2)
        self.assertIn("Key: A", content)
        self.assertIn("Key: B", content)

    def test_8_no_events_recorded_when_inactive(self):
        """8. Verify no events are recorded when logging is stopped or inactive."""
        self.assertFalse(self.logger.is_logging)
        event1 = self.logger.record_event(MockKeyEvent(char="z", keysym="z"))
        self.assertIsNone(event1)
        self.assertEqual(self.logger.session_events_count, 0)

        # Start and Stop
        self.logger.start_logging()
        self.logger.stop_logging()
        self.assertFalse(self.logger.is_logging)

        event2 = self.logger.record_event(MockKeyEvent(char="y", keysym="y"))
        self.assertIsNone(event2)
        self.assertEqual(self.logger.session_events_count, 0)

        content = self.logger.get_log_contents()
        self.assertNotIn("Key: z", content)
        self.assertNotIn("Key: y", content)


if __name__ == "__main__":
    unittest.main()

