# hub/main.py
import sys
from .cli import main

def entry_point():
    sys.exit(main())

if __name__ == "__main__":
    entry_point()