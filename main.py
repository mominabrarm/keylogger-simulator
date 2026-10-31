"""
Keylogger Simulator - Graphical User Interface Application
---------------------------------------------------------
A clean, educational desktop application built with Python Tkinter.
Demonstrates keystroke monitoring strictly localized within an application
input widget, featuring user controls, real-time activity tracking, and
timestamped file logging.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from logger import KeystrokeLogger

DEFAULT_LOG_PATH = "keylog.txt"


class KeyloggerSimulatorApp:
    """
    Main Tkinter GUI Application for the Keylogger Simulator.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Keylogger Simulator")
        self.root.geometry("740x660")
        self.root.minsize(680, 580)
        self.root.configure(bg="#0f172a")

        # Initialize the core logger component
        self.logger = KeystrokeLogger(log_file_path=DEFAULT_LOG_PATH)

        self._configure_styles()
        self._build_interface()
        self._update_status_display()

    def _configure_styles(self):
        """Configures ttk styles for a modern dark-themed interface."""
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Base style configuration
        self.style.configure(".", background="#0f172a", foreground="#e2e8f0", font=("Segoe UI", 10))
        self.style.configure("TFrame", background="#0f172a")
        self.style.configure("Card.TFrame", background="#1e293b", relief="flat")
        self.style.configure("Header.TLabel", background="#0f172a", foreground="#38bdf8", font=("Segoe UI", 16, "bold"))
        self.style.configure("SubHeader.TLabel", background="#0f172a", foreground="#94a3b8", font=("Segoe UI", 9))
        self.style.configure("Section.TLabel", background="#1e293b", foreground="#cbd5e1", font=("Segoe UI", 10, "bold"))

    def _build_interface(self):
        """Constructs all GUI elements: header, disclaimer, controls, inputs, and activity panel."""
        # Main padding container
        main_container = ttk.Frame(self.root, padding="18 14 18 18")
        main_container.pack(fill="both", expand=True)

        # 1. Header & Title Section
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(header_frame, text="Keylogger Simulator", style="Header.TLabel").pack(anchor="w")
        ttk.Label(
            header_frame,
            text="Prodigy InfoTech Cyber Security Internship — Task 04 (Educational Simulator)",
            style="SubHeader.TLabel"
        ).pack(anchor="w", pady=(2, 0))

        # 2. Ethical Use Disclaimer Card
        disclaimer_frame = tk.Frame(main_container, bg="#1e293b", bd=1, relief="solid", padx=12, pady=10)
        disclaimer_frame.pack(fill="x", pady=(0, 12))

        disclaimer_text = (
            "⚠ ETHICAL USE DISCLAIMER: This is a controlled educational simulator. Keystrokes are captured "
            "ONLY within the designated input box below. No system-wide hooks, background monitoring, "
            "or external application interception are performed."
        )
        tk.Label(
            disclaimer_frame,
            text=disclaimer_text,
            bg="#1e293b",
            fg="#facc15",
            font=("Segoe UI", 9),
            wraplength=680,
            justify="left"
        ).pack(anchor="w")

        # 3. Control Panel & Status Indicator
        controls_frame = tk.Frame(main_container, bg="#1e293b", bd=1, relief="solid", padx=14, pady=12)
        controls_frame.pack(fill="x", pady=(0, 12))

        # Buttons on left
        btn_box = tk.Frame(controls_frame, bg="#1e293b")
        btn_box.pack(side="left")

        self.btn_start = tk.Button(
            btn_box,
            text="▶ Start Logging",
            bg="#10b981",
            fg="#ffffff",
            activebackground="#059669",
            activeforeground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=14,
            pady=6,
            cursor="hand2",
            command=self.start_logging_action
        )
        self.btn_start.pack(side="left", padx=(0, 8))

        self.btn_stop = tk.Button(
            btn_box,
            text="⏹ Stop Logging",
            bg="#ef4444",
            fg="#ffffff",
            activebackground="#dc2626",
            activeforeground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=14,
            pady=6,
            cursor="hand2",
            state="disabled",
            command=self.stop_logging_action
        )
        self.btn_stop.pack(side="left", padx=8)

        self.btn_clear = tk.Button(
            btn_box,
            text="↺ Clear Session",
            bg="#475569",
            fg="#f8fafc",
            activebackground="#334155",
            activeforeground="#ffffff",
            font=("Segoe UI", 10),
            relief="flat",
            padx=12,
            pady=6,
            cursor="hand2",
            command=self.clear_session_action
        )
        self.btn_clear.pack(side="left", padx=8)

        self.btn_open_log = tk.Button(
            controls_frame,
            text="📄 Open Log File",
            bg="#2563eb",
            fg="#ffffff",
            activebackground="#1d4ed8",
            activeforeground="#ffffff",
            font=("Segoe UI", 10),
            relief="flat",
            padx=12,
            pady=6,
            cursor="hand2",
            command=self.open_log_file_action
        )
        self.btn_open_log.pack(side="right")

        # Status badge centered/right
        status_box = tk.Frame(controls_frame, bg="#1e293b")
        status_box.pack(side="right", padx=(0, 16))

        tk.Label(status_box, text="Status:", bg="#1e293b", fg="#94a3b8", font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 6))
        self.lbl_status = tk.Label(
            status_box,
            text=" ● STOPPED ",
            bg="#334155",
            fg="#94a3b8",
            font=("Segoe UI", 9, "bold"),
            padx=8,
            pady=3
        )
        self.lbl_status.pack(side="left")

        # 4. Designated Text Input Area
        input_container = tk.Frame(main_container, bg="#1e293b", bd=1, relief="solid", padx=12, pady=10)
        input_container.pack(fill="x", pady=(0, 12))

        input_header = tk.Frame(input_container, bg="#1e293b")
        input_header.pack(fill="x", pady=(0, 6))

        tk.Label(input_header, text="Designated Keystroke Input Area:", bg="#1e293b", fg="#38bdf8", font=("Segoe UI", 10, "bold")).pack(side="left")
        tk.Label(input_header, text="(Keystrokes are monitored only when typing inside this field)", bg="#1e293b", fg="#94a3b8", font=("Segoe UI", 8)).pack(side="right")

        self.txt_input = tk.Text(
            input_container,
            height=4,
            bg="#090d16",
            fg="#f8fafc",
            insertbackground="#38bdf8",
            font=("Segoe UI", 11),
            relief="flat",
            padx=10,
            pady=8,
            wrap="word"
        )
        self.txt_input.pack(fill="x")
        # Bind keypress events ONLY to this specific input box
        self.txt_input.bind("<KeyPress>", self._on_input_key_press)

        # 5. Live Activity Monitoring Panel
        activity_container = tk.Frame(main_container, bg="#1e293b", bd=1, relief="solid", padx=12, pady=10)
        activity_container.pack(fill="both", expand=True)

        activity_header = tk.Frame(activity_container, bg="#1e293b")
        activity_header.pack(fill="x", pady=(0, 6))

        tk.Label(activity_header, text="Live Keystroke Activity Panel (Audit Stream):", bg="#1e293b", fg="#10b981", font=("Segoe UI", 10, "bold")).pack(side="left")
        self.lbl_count = tk.Label(activity_header, text="Events: 0", bg="#1e293b", fg="#94a3b8", font=("Segoe UI", 9))
        self.lbl_count.pack(side="right")

        self.txt_activity = scrolledtext.ScrolledText(
            activity_container,
            bg="#090d16",
            fg="#a7f3d0",
            insertbackground="#ffffff",
            font=("Consolas", 10),
            relief="flat",
            padx=10,
            pady=8,
            wrap="word"
        )
        self.txt_activity.pack(fill="both", expand=True)
        self.txt_activity.insert(tk.END, "[System Idle] Click 'Start Logging' to activate keystroke capture.\n")
        self.txt_activity.configure(state="disabled")

    def _on_input_key_press(self, event: tk.Event):
        """
        Event handler triggered whenever a key is pressed inside the input area.
        Records the keystroke if logging is active.
        """
        if not self.logger.is_logging:
            return

        # Record through the logger module
        record = self.logger.record_event(event)
        if record:
            self._append_activity_log(record["log_line"])
            self.lbl_count.config(text=f"Events: {self.logger.session_events_count}")

    def _append_activity_log(self, text: str):
        """Appends a new line of log output to the activity panel."""
        self.txt_activity.configure(state="normal")
        self.txt_activity.insert(tk.END, text + "\n")
        self.txt_activity.see(tk.END)
        self.txt_activity.configure(state="disabled")

    def _update_status_display(self):
        """Synchronizes GUI buttons and status badge with logger state."""
        if self.logger.is_logging:
            self.lbl_status.config(text=" ● LOGGING ACTIVE ", bg="#065f46", fg="#34d399")
            self.btn_start.config(state="disabled", bg="#334155")
            self.btn_stop.config(state="normal", bg="#ef4444")
        else:
            self.lbl_status.config(text=" ● STOPPED ", bg="#334155", fg="#94a3b8")
            self.btn_start.config(state="normal", bg="#10b981")
            self.btn_stop.config(state="disabled", bg="#334155")

    def start_logging_action(self):
        """User action: starts keystroke logging."""
        if self.logger.start_logging():
            self._update_status_display()
            self._append_activity_log(f"\n--- [LOGGING STARTED at {self.logger.get_timestamp()}] ---")
            self.txt_input.focus_set()

    def stop_logging_action(self):
        """User action: stops keystroke logging."""
        count = self.logger.session_events_count
        if self.logger.stop_logging():
            self._update_status_display()
            self._append_activity_log(f"--- [LOGGING STOPPED at {self.logger.get_timestamp()} | Total: {count}] ---\n")

    def clear_session_action(self):
        """User action: clears input text and in-memory activity screen."""
        self.txt_input.delete("1.0", tk.END)
        self.logger.clear_session_history()
        self.lbl_count.config(text="Events: 0")

        self.txt_activity.configure(state="normal")
        self.txt_activity.delete("1.0", tk.END)
        status_note = "[Active Session]" if self.logger.is_logging else "[System Idle]"
        self.txt_activity.insert(tk.END, f"{status_note} Session view cleared. Logging to file remains preserved.\n")
        self.txt_activity.configure(state="disabled")

    def open_log_file_action(self):
        """User action: opens keylog.txt using the operating system's default text editor."""
        log_path = self.logger.log_file_path

        # If file doesn't exist yet, create it with a header
        if not os.path.exists(log_path):
            with open(log_path, "w", encoding="utf-8") as f:
                f.write(f"=== Keylogger Simulator Log Initialized: {self.logger.get_timestamp()} ===\n")

        try:
            if sys.platform.startswith("win"):
                os.startfile(log_path)
            elif sys.platform.startswith("darwin"):
                import subprocess
                subprocess.run(["open", log_path], check=True)
            else:
                import subprocess
                subprocess.run(["xdg-open", log_path], check=True)
        except Exception as e:
            messagebox.showerror("Error Opening Log", f"Could not open file: {e}\nPath: {log_path}")


def main():
    """Main entry point for running the Keylogger Simulator."""
    root = tk.Tk()
    app = KeyloggerSimulatorApp(root)

    def on_closing():
        if app.logger.is_logging:
            app.logger.stop_logging()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()

