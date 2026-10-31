"""
Keylogger Simulator - Core Logging Module
----------------------------------------
Implements ethical, in-application keystroke monitoring, key formatting,
and timestamped file logging using Python's built-in standard library.

Design Principles:
- Strictly local to the application: No global system hooks.
- Transparent: Visible events and user-controlled recording.
- Non-destructive: Appends sessions without overwriting history.
"""

import os
from datetime import datetime
from typing import Optional, Dict, Any, List


class KeystrokeLogger:
    """
    Manages in-application keystroke recording, event formatting,
    and structured file persistence.
    """

    # Mapping of special Tkinter keysyms to human-readable representations
    SPECIAL_KEYS_MAP = {
        "Return": "[ENTER]",
        "BackSpace": "[BACKSPACE]",
        "space": "[SPACE]",
        "Tab": "[TAB]",
        "Delete": "[DELETE]",
        "Escape": "[ESCAPE]",
        "Caps_Lock": "[CAPSLOCK]",
        "Shift_L": "[SHIFT]",
        "Shift_R": "[SHIFT]",
        "Control_L": "[CTRL]",
        "Control_R": "[CTRL]",
        "Alt_L": "[ALT]",
        "Alt_R": "[ALT]",
        "Up": "[UP]",
        "Down": "[DOWN]",
        "Left": "[LEFT]",
        "Right": "[RIGHT]",
        "Home": "[HOME]",
        "End": "[END]",
        "Prior": "[PGUP]",
        "Next": "[PGDN]",
        "Insert": "[INSERT]",
    }

    def __init__(self, log_file_path: str = "keylog.txt"):
        """
        Initializes the KeystrokeLogger instance.

        Args:
            log_file_path (str): Relative or absolute path to the output log file.
        """
        self.log_file_path = os.path.abspath(log_file_path)
        self.is_logging = False
        self.session_events_count = 0
        self.current_session_events: List[Dict[str, Any]] = []

        # Ensure target directory exists
        log_dir = os.path.dirname(self.log_file_path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

    @staticmethod
    def get_timestamp() -> str:
        """Returns the current timestamp in YYYY-MM-DD HH:MM:SS format."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def start_logging(self) -> bool:
        """
        Activates keystroke recording and writes a session start marker.

        Returns:
            bool: True if logging transitioned from inactive to active, False otherwise.
        """
        if self.is_logging:
            return False

        self.is_logging = True
        self.session_events_count = 0
        self.current_session_events = []

        header = f"\n======================================================\n" \
                 f"[SESSION START] {self.get_timestamp()}\n" \
                 f"======================================================\n"
        self._write_to_file(header)
        return True

    def stop_logging(self) -> bool:
        """
        Deactivates keystroke recording and writes a session summary footer.

        Returns:
            bool: True if logging transitioned from active to inactive, False otherwise.
        """
        if not self.is_logging:
            return False

        self.is_logging = False
        footer = f"[SESSION END] {self.get_timestamp()} | Total Keys Recorded: {self.session_events_count}\n" \
                 f"======================================================\n"
        self._write_to_file(footer)
        return True

    def format_key(self, key_data: Any) -> str:
        """
        Translates raw keyboard input (characters or Tkinter events)
        into standardized, readable key representations.

        Args:
            key_data: Either a Tkinter event object or a string key identifier.

        Returns:
            str: Normalized, human-readable key string.
        """
        # If passed a Tkinter event object
        if hasattr(key_data, "keysym"):
            keysym = key_data.keysym
            char = getattr(key_data, "char", "")

            # Check special keys mapping first
            if keysym in self.SPECIAL_KEYS_MAP:
                return self.SPECIAL_KEYS_MAP[keysym]

            # If it's a printable character
            if char and char.isprintable():
                return char

            # Fallback for other keysyms
            return f"[{keysym.upper()}]"

        # If passed a direct string
        key_str = str(key_data)
        if key_str in self.SPECIAL_KEYS_MAP:
            return self.SPECIAL_KEYS_MAP[key_str]

        return key_str

    def record_event(self, key_data: Any) -> Optional[Dict[str, Any]]:
        """
        Records a single keystroke event if logging is active.

        Args:
            key_data: The keystroke to record.

        Returns:
            Optional[Dict[str, Any]]: Event details dict if recorded, or None if inactive.
        """
        if not self.is_logging:
            return None

        formatted_key = self.format_key(key_data)
        timestamp = self.get_timestamp()
        log_line = f"[{timestamp}] Key: {formatted_key}\n"

        self._write_to_file(log_line)

        self.session_events_count += 1
        event_record = {
            "timestamp": timestamp,
            "raw": key_data,
            "key": formatted_key,
            "log_line": log_line.strip(),
            "event_number": self.session_events_count,
        }
        self.current_session_events.append(event_record)
        return event_record

    def _write_to_file(self, content: str) -> bool:
        """
        Appends content to the configured log file using robust error handling.

        Args:
            content (str): The string content to append.

        Returns:
            bool: True if write succeeded, False if an I/O error occurred.
        """
        try:
            with open(self.log_file_path, "a", encoding="utf-8") as file:
                file.write(content)
            return True
        except IOError as e:
            # Gracefully handle file I/O exceptions
            print(f"[!] KeystrokeLogger File Write Error: {e}")
            return False

    def get_log_contents(self) -> str:
        """
        Reads and returns the complete contents of the log file.

        Returns:
            str: Log file content, or an empty string if file does not exist.
        """
        if not os.path.exists(self.log_file_path):
            return ""
        try:
            with open(self.log_file_path, "r", encoding="utf-8") as file:
                return file.read()
        except IOError:
            return ""

    def clear_session_history(self) -> None:
        """Resets the in-memory event tracking list for the active session."""
        self.current_session_events = []
        self.session_events_count = 0

