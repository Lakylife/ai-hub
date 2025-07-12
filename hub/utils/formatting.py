# grok4_cli/utils/formatting.py
import sys
from typing import Any


class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    GREY = '\033[90m'
    DIM = '\033[2m'
    END = '\033[0m'


def print_response(text: str):
    print(f"{Colors.GREEN}{text}{Colors.END}")


def print_error(text: str):
    print(f"{Colors.RED}Error: {text}{Colors.END}", file=sys.stderr)


def print_info(text: str):
    print(f"{Colors.BLUE}{text}{Colors.END}")


def print_warning(text: str):
    print(f"{Colors.YELLOW}Warning: {text}{Colors.END}")


def print_bold(text: str):
    print(f"{Colors.BOLD}{text}{Colors.END}")


def print_grey(text: str):
    print(f"{Colors.GREY}{text}{Colors.END}")


def print_dim(text: str):
    print(f"{Colors.DIM}{text}{Colors.END}")


def format_response(text: str) -> str:
    lines = text.split('\n')
    formatted_lines = []
    
    for line in lines:
        if line.strip().startswith('```'):
            formatted_lines.append(f"{Colors.YELLOW}{line}{Colors.END}")
        elif line.strip().startswith('#'):
            formatted_lines.append(f"{Colors.BOLD}{line}{Colors.END}")
        else:
            formatted_lines.append(line)
    
    return '\n'.join(formatted_lines)