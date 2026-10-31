"""
Unit Tests for Keylogger Simulator
----------------------------------
Tests cover the core requirements:
1. Logging starts successfully.
2. Logging stops successfully.
3. Typed characters are recorded.
4. Special keys are represented correctly.
5. Timestamps are generated.
6. Log entries are saved to the correct file.
7. Previous log entries are preserved.
8. No events are recorded when logging is inactive.
"""

import os
import re
import pytest
import sys

# Ensure parent directory is in Python path for importing logger
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from logger import KeystrokeLogger


class MockKeyEvent:
    """Mock object replicating a Tkinter KeyPress event."""
    def __init__(self, char: str = "", keysym: str = ""):
        self.char = char
        self.keysym = keysym


@pytest.fixture
def temp_logger(tmp_path):
    """Provides a fresh KeystrokeLogger pointing to a temporary test file."""
    log_file = tmp_path / "test_keylog.txt"
    return KeystrokeLogger(log_file_path=str(log_file))


def test_logging_start(temp_logger):
    """1. Test that logging starts successfully and updates state."""
    assert not temp_logger.is_logging
    result = temp_logger.start_logging()
    assert result is True
    assert temp_logger.is_logging is True

    # Repeated start should return False
    assert temp_logger.start_logging() is False


def test_logging_stop(temp_logger):
    """2. Test that logging stops successfully and updates state."""
    temp_logger.start_logging()
    assert temp_logger.is_logging is True

    result = temp_logger.stop_logging()
    assert result is True
    assert temp_logger.is_logging is False

    # Repeated stop should return False
    assert temp_logger.stop_logging() is False


def test_typed_characters_recorded(temp_logger):
    """3. Test that regular typed characters are accurately recorded."""
    temp_logger.start_logging()

    # Record alphanumeric characters
    event_a = temp_logger.record_event(MockKeyEvent(char="a", keysym="a"))
    event_z = temp_logger.record_event(MockKeyEvent(char="Z", keysym="Z"))
    event_num = temp_logger.record_event(MockKeyEvent(char="9", keysym="9"))
    event_sym = temp_logger.record_event(MockKeyEvent(char="@", keysym="at"))

    assert event_a["key"] == "a"
    assert event_z["key"] == "Z"
    assert event_num["key"] == "9"
    assert event_sym["key"] == "@"
    assert temp_logger.session_events_count == 4


def test_special_keys_representation(temp_logger):
    """4. Test that special keys (ENTER, SPACE, BACKSPACE, TAB, DELETE, etc.) are mapped to readable labels."""
    temp_logger.start_logging()

    keys_to_test = [
        (MockKeyEvent(char="", keysym="Return"), "[ENTER]"),
        (MockKeyEvent(char=" ", keysym="space"), "[SPACE]"),
        (MockKeyEvent(char="", keysym="BackSpace"), "[BACKSPACE]"),
        (MockKeyEvent(char="\t", keysym="Tab"), "[TAB]"),
        (MockKeyEvent(char="", keysym="Delete"), "[DELETE]"),
        (MockKeyEvent(char="", keysym="Escape"), "[ESCAPE]"),
    ]

    for mock_event, expected_label in keys_to_test:
        recorded = temp_logger.record_event(mock_event)
        assert recorded["key"] == expected_label


def test_timestamps_generated(temp_logger):
    """5. Test that valid YYYY-MM-DD HH:MM:SS timestamps are generated for events."""
    temp_logger.start_logging()
    recorded = temp_logger.record_event(MockKeyEvent(char="k", keysym="k"))

    timestamp = recorded["timestamp"]
    assert timestamp is not None

    # Matches YYYY-MM-DD HH:MM:SS regex pattern
    pattern = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"
    assert re.match(pattern, timestamp) is not None
    assert f"[{timestamp}] Key: k" == recorded["log_line"]


def test_log_saved_to_file(temp_logger):
    """6. Test that log entries are physically written to the configured file."""
    temp_logger.start_logging()
    temp_logger.record_event(MockKeyEvent(char="x", keysym="x"))
    temp_logger.stop_logging()

    assert os.path.exists(temp_logger.log_file_path)

    contents = temp_logger.get_log_contents()
    assert "[SESSION START]" in contents
    assert "Key: x" in contents
    assert "[SESSION END]" in contents
    assert "Total Keys Recorded: 1" in contents


def test_previous_logs_preserved(temp_logger):
    """7. Test that subsequent sessions append without overwriting previous logs."""
    # Session 1
    temp_logger.start_logging()
    temp_logger.record_event(MockKeyEvent(char="1", keysym="1"))
    temp_logger.stop_logging()

    # Session 2
    temp_logger.start_logging()
    temp_logger.record_event(MockKeyEvent(char="2", keysym="2"))
    temp_logger.stop_logging()

    contents = temp_logger.get_log_contents()

    # Both session markers and keys should be present in the same file
    assert contents.count("[SESSION START]") == 2
    assert contents.count("[SESSION END]") == 2
    assert "Key: 1" in contents
    assert "Key: 2" in contents


def test_no_events_when_inactive(temp_logger):
    """8. Test that no events are recorded when logging has not been started or is stopped."""
    # Inactive before start
    assert not temp_logger.is_logging
    result1 = temp_logger.record_event(MockKeyEvent(char="a", keysym="a"))
    assert result1 is None
    assert temp_logger.session_events_count == 0

    # Start and stop
    temp_logger.start_logging()
    temp_logger.stop_logging()
    assert not temp_logger.is_logging

    # Inactive after stop
    result2 = temp_logger.record_event(MockKeyEvent(char="b", keysym="b"))
    assert result2 is None
    assert temp_logger.session_events_count == 0

    # The file should not contain 'a' or 'b'
    contents = temp_logger.get_log_contents()
    assert "Key: a" not in contents
    assert "Key: b" not in contents

