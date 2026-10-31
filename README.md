# Keylogger Simulator

### Prodigy InfoTech — Cyber Security Internship (Task 04)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![GUI](https://img.shields.io/badge/GUI-Tkinter-brightgreen)
![Tests](https://img.shields.io/badge/Tests-pytest-orange)
![Security Focus](https://img.shields.io/badge/Security-Educational_Simulator-red)

---

## 1. Project Title & Description

**Keylogger Simulator** is an educational, interactive desktop application designed to demonstrate the mechanics of keystroke event interception, user-space input monitoring, structured file logging, and ethical cybersecurity principles.

Unlike malicious spyware or covert keyloggers, this simulator operates **strictly within a controlled GUI environment**. Keystroke monitoring is scoped exclusively to the application's designated text input widget and requires explicit user activation, ensuring transparency and zero intrusion into the host operating system.

---

## 2. Internship Task Information
- **Organization**: Prodigy InfoTech
- **Track**: Cyber Security Internship
- **Task**: Task-04 (Simple Keylogger / Keylogger Simulator)
- **Status**: Completed & Fully Tested

---

## 3. Project Objectives
- Demonstrate keyboard event capture using Python GUI event bindings.
- Model in-application input monitoring without compromising OS security boundaries.
- Implement reliable, non-destructive file logging with timestamps and special key formatting.
- Emphasize ethical considerations and distinguish authorized diagnostic auditing from unauthorized surveillance.
- Provide a modular, unit-tested codebase adhering to senior engineering practices.

---

## 4. Technology Stack
- **Language**: Python 3.8+
- **Graphical Interface**: Tkinter (Python standard library)
- **File & Event Handling**: Python standard library (`datetime`, `os`, `sys`, `typing`)
- **Automated Testing**: `pytest`

*Note: No third-party system-hook dependencies (such as `pynput` or `keyboard`) are required. The application runs natively with standard Python.*

---

## 5. Core Features

### A. User Interface
- **Application Header & Branding**: Clear title and internship attribution.
- **Ethical Disclaimer Banner**: Prominent warning explaining the controlled simulator boundaries.
- **Designated Typing Area**: Multi-line text field where key events are isolated.
- **Start / Stop Controls**: Buttons that enforce strict control over when events are captured.
- **Session Reset**: "Clear Session" button to refresh the view without wiping historical file logs.
- **Live Status Indicator**: High-contrast badge displaying `● LOGGING ACTIVE` (Green) or `● STOPPED` (Gray/Red).
- **Log Opener**: One-click button to open `keylog.txt` directly in the system's default text editor.

### B. Keystroke Recording
- Event capture bound exclusively to the designated input widget (`<KeyPress>`).
- Normalization of printable characters (`a-z`, `A-Z`, numbers, punctuation).
- Readable label mapping for special keys:
  - `[ENTER]`
  - `[SPACE]`
  - `[BACKSPACE]`
  - `[TAB]`
  - `[DELETE]`
  - `[ESCAPE]`, `[CAPSLOCK]`, `[SHIFT]`, `[CTRL]`, `[ALT]`, `[UP]`, `[DOWN]`, `[LEFT]`, `[RIGHT]`
- Real-time event counter and scrollable activity panel.

### C. File Logging
- Events saved to `keylog.txt` in real time.
- Timestamp format: `[YYYY-MM-DD HH:MM:SS] Key: <label>`.
- Distinct `[SESSION START]` and `[SESSION END]` demarcation headers.
- Append mode (`"a"`): Historical logs are never overwritten across sessions.
- Robust exception handling for filesystem I/O.

### D. Security and Ethical Baseline
This simulator strictly conforms to ethical software guidelines:
- ❌ **No global keyboard hooks** (cannot intercept keystrokes outside the window).
- ❌ **No background daemon execution** (closes completely when terminated).
- ❌ **No stealth or process hiding** (fully visible GUI).
- ❌ **No startup persistence** (no registry, scheduled task, or cron modification).
- ❌ **No network exfiltration** (zero sockets, HTTP requests, or remote telemetry).
- ❌ **No password or credential harvesting**.

---

## 6. Project Structure

```
keylogger-simulator/
│
├── main.py              # Tkinter GUI application entry point
├── logger.py            # Core KeystrokeLogger module (event formatting & file I/O)
├── requirements.txt     # Test dependencies (pytest)
├── README.md            # Comprehensive project documentation
├── keylog.txt           # Generated persistent keystroke log file
└── tests/
    └── test_logger.py   # Automated unit test suite (8 test cases)
```

---

## 7. Installation Instructions

### Prerequisites
- Python 3.8 or higher installed on Windows, Linux, or macOS.

### Setup
1. Open your terminal and navigate to the project directory:
   ```bash
   cd keylogger-simulator
   ```
2. (Optional) Install `pytest` for running automated tests:
   ```bash
   pip install -r requirements.txt
   ```

---

## 8. How to Run & Use the Application

### Running the Application
Launch the graphical simulator:
```bash
python main.py
```

### Usage Steps:
1. **Launch**: The application starts in `STOPPED` mode. Keystrokes are not recorded.
2. **Start Logging**: Click the green **Start Logging** button. The status badge changes to `● LOGGING ACTIVE`.
3. **Type**: Click into the **Designated Keystroke Input Area** and type sentences, spaces, backspaces, and enters.
4. **Observe**: The **Live Keystroke Activity Panel** updates instantly with timestamped records.
5. **Stop Logging**: Click **Stop Logging**. Logging immediately halts.
6. **Review Logs**: Click **Open Log File** to review the persisted entries in `keylog.txt`.
7. **Clear Session**: Click **Clear Session** to reset the input box and live activity screen.

---

## 9. Sample Log Output (`keylog.txt`)

```text
======================================================
[SESSION START] 2026-10-31 23:50:00
======================================================
[2026-10-31 23:50:02] Key: H
[2026-10-31 23:50:02] Key: e
[2026-10-31 23:50:03] Key: l
[2026-10-31 23:50:03] Key: l
[2026-10-31 23:50:03] Key: o
[2026-10-31 23:50:04] Key: [SPACE]
[2026-10-31 23:50:04] Key: S
[2026-10-31 23:50:05] Key: e
[2026-10-31 23:50:05] Key: c
[2026-10-31 23:50:05] Key: u
[2026-10-31 23:50:06] Key: r
[2026-10-31 23:50:06] Key: i
[2026-10-31 23:50:06] Key: t
[2026-10-31 23:50:07] Key: y
[2026-10-31 23:50:08] Key: [ENTER]
[SESSION END] 2026-10-31 23:50:15 | Total Keys Recorded: 15
======================================================
```

---

## 10. Automated Testing

The project includes unit test coverage across all core features using `pytest`:

```bash
pytest tests/test_logger.py -v
```

### Verified Test Cases:
1. `test_logging_start`: Verifies state transitions when logging begins.
2. `test_logging_stop`: Verifies clean termination and state updates.
3. `test_typed_characters_recorded`: Validates capture of alphanumeric keys.
4. `test_special_keys_representation`: Validates mapping of ENTER, SPACE, BACKSPACE, TAB, DELETE, and ESCAPE.
5. `test_timestamps_generated`: Checks ISO/standard datetime formatting (`YYYY-MM-DD HH:MM:SS`).
6. `test_log_saved_to_file`: Confirms physical write operations to disk.
7. `test_previous_logs_preserved`: Ensures multi-session log append integrity.
8. `test_no_events_when_inactive`: Confirms zero recordings while in `STOPPED` state.

---

## 11. Ethical Considerations & Defensive Insights

In cybersecurity, keyloggers represent a significant threat vector often used by adversaries in credential theft and corporate espionage. By constructing a transparent, user-bound simulator, security students learn:

| Security Vector | Keylogger Risk | Defensive Countermeasure |
| :--- | :--- | :--- |
| **Credential Harvesting** | Intercepting plaintext passwords | Multi-Factor Authentication (MFA / 2FA / FIDO2) |
| **Physical Keystrokes** | Hardware or software scancode logging | Password Managers (browser DOM injection) |
| **Hook Detection** | Covert API calls (`SetWindowsHookEx`) | Endpoint Detection & Response (EDR) heuristics |
| **Process Isolation** | Memory inspection or user-space snooping | OS sandboxing and Least Privilege principles |

---

## 12. Learning Outcomes
- Proficient event handling with Python GUI frameworks (Tkinter).
- Clean software architecture: separation of UI (`main.py`) and business logic (`logger.py`).
- Deterministic, headless unit testing for event-driven logic.
- Ethical awareness of surveillance vectors and mitigation strategies.

