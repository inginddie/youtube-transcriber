"""
Basic usage examples for YouTube Transcriber Pro
"""
from src.transcriber import YouTubeTranscriber
from config import create_directories


def example_single_video():
    """Example: Transcribe a single video"""
    print("Example 1: Single Video Transcription")
    print("=" * 60)
    
    # Setup
    create_directories()
    transcriber = YouTubeTranscriber()
    
    # Process video
    url = "https://youtu.be/dQw4w9WgXcQ"
    result = transcriber.process_video(url, index=1)
    
    if result['success']:
        print(f"✅ Success!")
        print(f"Title: {result['title']}")
        print(f"Word Count: {result['word_count']}")
        print(f"JSON: {result['json_path']}")
        print(f"TXT: {result['txt_path']}")
    else:
        print(f"❌ Error: {result['error']}")


def example_multiple_videos():
    """Example: Transcribe multiple videos"""
    print("\nExample 2: Multiple Videos")
    print("=" * 60)
    
    transcriber = YouTubeTranscriber()
    
    urls = [
        "https://youtu.be/VIDEO_ID_1",
        "https://youtu.be/VIDEO_ID_2",
        "https://youtu.be/VIDEO_ID_3"
    ]
    
    results = transcriber.process_multiple_videos(urls)
    
    successful = [r for r in results if r['success']]
    print(f"\n✅ Completed: {len(successful)}/{len(results)}")


def example_with_progress():
    """Example: With progress callback"""
    print("\nExample 3: With Progress Tracking")
    print("=" * 60)
    
    def progress_callback(message: str):
        print(f"[PROGRESS] {message}")
    
    transcriber = YouTubeTranscriber()
    url = "https://youtu.be/dQw4w9WgXcQ"
    
    result = transcriber.process_video(
        url, 
        index=1, 
        progress_callback=progress_callback
    )
    
    print(f"\nFinal result: {result['success']}")


def example_error_handling():
    """Example: Proper error handling"""
    print("\nExample 4: Error Handling")
    print("=" * 60)
    
    transcriber = YouTubeTranscriber()
    
    # Invalid URL
    result = transcriber.process_video("https://www.google.com", 1)
    
    if not result['success']:
        print(f"Expected error: {result['error']}")
        print("Handled gracefully!")


if __name__ == "__main__":
    # Run examples
    example_single_video()
    # example_multiple_videos()  # Uncomment to run
    # example_with_progress()    # Uncomment to run
    # example_error_handling()   # Uncomment to run
