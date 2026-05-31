#!/usr/bin/env python3
import sys
from ficha.gui import FichaGUI
from ficha.cli import FichaCLI

def main():
    if len(sys.argv) > 1 and sys.argv[1] in ["-G", "--gui"]:
        FichaGUI().run()
    else:
        FichaCLI().run()

if __name__ == "__main__":
    main()
