#!/usr/bin/env python3
import argparse
from pathlib import Path

from . import convert_docx_to_md


def main():
    parser = argparse.ArgumentParser(
        prog="doc-to-md",
        description="Convert DOCX files to Markdown using word2md.com"
    )

    parser.add_argument(
        "input",
        help="DOCX file or directory containing DOCX files"
    )

    parser.add_argument(
        "--out",
        default="./md",
        help="Output directory (default: ./md)"
    )

    parser.add_argument(
        "--headless",
        action="store_true",
        default=True,
        help="Run browser in headless mode (default: True)"
    )

    parser.add_argument(
        "--no-headless",
        action="store_false",
        dest="headless",
        help="Show browser window"
    )

    args = parser.parse_args()

    try:
        converted_files = convert_docx_to_md(
            args.input,
            output_dir=args.out,
            headless=args.headless,
        )
        for f in converted_files:
            print(f"✔ Saved: {f}")
    except (FileNotFoundError, ValueError) as e:
        raise SystemExit(f"❌ {e}")


if __name__ == "__main__":
    main()
