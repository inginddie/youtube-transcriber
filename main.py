"""
CLI interface for YouTube Transcriber Pro
"""
import sys
import argparse
from pathlib import Path

from config import create_directories
from src.transcriber import YouTubeTranscriber
from src.utils import parse_urls_input, validate_url


def print_progress(message: str):
    """Print progress message"""
    print(message)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='YouTube Transcriber Pro - Transcribe YouTube videos using OpenAI Whisper',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py https://youtu.be/VIDEO_ID
  python main.py --file urls.txt
  python main.py URL1 URL2 URL3
        """
    )
    
    parser.add_argument(
        'urls',
        nargs='*',
        help='YouTube video URLs to transcribe'
    )
    
    parser.add_argument(
        '--file',
        '-f',
        type=str,
        help='File containing YouTube URLs (one per line)'
    )
    
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force re-transcription even if video already exists'
    )
    
    args = parser.parse_args()
    
    # Collect URLs
    urls = []
    
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"❌ Error: File not found: {args.file}")
            sys.exit(1)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            urls = parse_urls_input(content)
    
    if args.urls:
        for url in args.urls:
            if validate_url(url):
                urls.append(url)
            else:
                print(f"⚠️  Warning: Invalid URL skipped: {url}")
    
    if not urls:
        print("❌ Error: No valid URLs provided")
        print("\nUsage:")
        parser.print_help()
        sys.exit(1)
    
    # Create directories
    print("🔧 Setting up directories...")
    create_directories()
    
    # Initialize transcriber
    print("🚀 Starting YouTube Transcriber Pro")
    print(f"📝 Processing {len(urls)} video(s)...\n")
    
    transcriber = YouTubeTranscriber()
    
    # Process videos
    skip_if_exists = not args.force
    results = transcriber.process_multiple_videos(
        urls, 
        progress_callback=print_progress,
        skip_if_exists=skip_if_exists
    )
    
    # Print summary
    print("\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)
    
    successful = [r for r in results if r.get('success') and not r.get('skipped')]
    skipped = [r for r in results if r.get('success') and r.get('skipped')]
    failed = [r for r in results if not r.get('success')]
    
    print(f"\n✅ Newly transcribed: {len(successful)}/{len(results)}")
    for result in successful:
        print(f"   - {result['title']} ({result['word_count']} words)")
    
    if skipped:
        print(f"\n⏭️  Skipped (already exist): {len(skipped)}/{len(results)}")
        for result in skipped:
            print(f"   - {result['title']}")
    
    if failed:
        print(f"\n❌ Failed: {len(failed)}/{len(results)}")
        for result in failed:
            print(f"   - {result['url']}: {result['error']}")
    
    print("\n✨ Done! Check the 'transcripts' folder for output files.")


if __name__ == "__main__":
    main()
