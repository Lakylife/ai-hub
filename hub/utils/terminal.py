# grok4_cli/utils/terminal.py
import os
import sys
import signal
from typing import Any


def setup_terminal():
    if sys.platform != "win32":
        signal.signal(signal.SIGINT, signal_handler)


def signal_handler(signum: int, frame: Any):
    print("\n\nKeyboard interrupt received. Use '/exit' or press Ctrl+C twice to quit.")
    

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_terminal_width() -> int:
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80


def truncate_text(text: str, max_length: int) -> str:
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def print_separator(char: str = "-", length: int = None):
    if length is None:
        length = get_terminal_width()
    print(char * length)