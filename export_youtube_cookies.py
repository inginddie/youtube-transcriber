#!/usr/bin/env python3
"""
Export YouTube cookies from browser to file for use with yt-dlp

This script helps export cookies from your browser so the transcriber
can handle YouTube's bot detection by authenticating requests.

Usage:
    1. Install the extension: https://github.com/kairi003/Get-cookies.txt-LOCALLY
    2. Visit YouTube.com
    3. Click the extension icon and save cookies as ~/youtube_cookies.txt
    4. Run this script to place it in the right location

Or manually:
    python export_youtube_cookies.py <path_to_cookies_file>
"""

import sys
import shutil
from pathlib import Path


def main():
    """Export YouTube cookies to home directory"""

    if len(sys.argv) > 1:
        source = Path(sys.argv[1])
        if not source.exists():
            print(f"❌ Error: File not found: {source}")
            sys.exit(1)
    else:
        print("🍪 YouTube Cookies Exporter")
        print("=" * 50)
        print("\n📖 To export cookies from your browser:")
        print("1. Install: https://github.com/kairi003/Get-cookies.txt-LOCALLY")
        print("2. Visit: https://www.youtube.com")
        print("3. Click extension → Export → Save as 'cookies.txt'")
        print("\n💾 Then run:")
        print("   python export_youtube_cookies.py /path/to/cookies.txt")
        print("\n📍 Or place cookies file at:")
        cookies_path = Path.home() / ".youtube_cookies.txt"
        print(f"   {cookies_path}")
        print("\n✅ This enables authenticated YouTube access and avoids bot detection!")
        sys.exit(0)

    dest = Path.home() / ".youtube_cookies.txt"

    try:
        shutil.copy2(source, dest)
        print(f"✅ Cookies exported to: {dest}")
        print("\n🎉 Your transcriber can now handle bot detection!")
        print("   Try transcribing a video now.")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
