# ficha/cli.py
import argparse
from .core import FichaCore

class FichaCLI:
    def __init__(self):
        self.core = FichaCore()

    def run(self):
        parser = argparse.ArgumentParser(description="Ficha - Advanced Steganography")
        subparsers = parser.add_subparsers(dest="command")

        # Embed
        e = subparsers.add_parser("embed", help="Embed file")
        e.add_argument("-c", "--carrier", required=True)
        e.add_argument("-s", "--secret", required=True)
        e.add_argument("-p", "--passphrase", required=True)
        e.add_argument("-t", "--type", choices=["image", "video", "audio"], default="image")

        # Extract
        x = subparsers.add_parser("extract", help="Extract file")
        x.add_argument("-c", "--carrier", required=True)
        x.add_argument("-o", "--output", required=True)
        x.add_argument("-p", "--passphrase", required=True)

        args = parser.parse_args()

        if args.command == "embed":
            try:
                if args.type == "video":
                    out = self.core.embed_video(args.carrier, args.secret, args.passphrase)
                elif args.type == "audio":
                    out = self.core.embed_audio(args.carrier, args.secret, args.passphrase)
                else:
                    out = self.core.embed_image(args.carrier, args.secret, args.passphrase)
                print(f"[+] Success → {out}")
            except Exception as e:
                print(f"[-] Error: {e}")

        elif args.command == "extract":
            try:
                result = self.core.extract(args.carrier, args.output, args.passphrase)
                print(f"[+] Extracted → {result}")
            except Exception as e:
                print(f"[-] Error: {e}")
        else:
            parser.print_help()
