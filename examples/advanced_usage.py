"""
Advanced usage examples for YouTube Transcriber Pro
"""
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from src.transcriber import YouTubeTranscriber
from src.utils import extract_video_id


def example_parallel_processing():
    """Example: Process multiple videos in parallel"""
    print("Advanced Example 1: Parallel Processing")
    print("=" * 60)
    
    urls = [
        "https://youtu.be/VIDEO_ID_1",
        "https://youtu.be/VIDEO_ID_2",
        "https://youtu.be/VIDEO_ID_3"
    ]
    
    transcriber = YouTubeTranscriber()
    
    def process_single(url_with_index):
        url, index = url_with_index
        return transcriber.process_video(url, index)
    
    # Process in parallel (max 3 concurrent)
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(
            process_single, 
            [(url, i) for i, url in enumerate(urls, 1)]
        ))
    
    successful = sum(1 for r in results if r['success'])
    print(f"✅ Completed: {successful}/{len(results)}")


def example_caching():
    """Example: Check if video already transcribed"""
    print("\nAdvanced Example 2: Caching")
    print("=" * 60)
    
    def is_already_transcribed(video_id: str) -> bool:
        """Check if video is already transcribed"""
        transcripts_dir = Path("transcripts")
        
        if not transcripts_dir.exists():
            return False
        
        for json_file in transcripts_dir.glob("*.json"):
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                    if data.get('video_id') == video_id:
                        return True
            except:
                continue
        
        return False
    
    # Check before processing
    url = "https://youtu.be/dQw4w9WgXcQ"
    video_id = extract_video_id(url)
    
    if is_already_transcribed(video_id):
        print(f"✅ Video {video_id} already transcribed, skipping...")
    else:
        print(f"🔄 Processing new video: {video_id}")
        # transcriber.process_video(url, 1)


def example_batch_processing():
    """Example: Process videos in batches"""
    print("\nAdvanced Example 3: Batch Processing")
    print("=" * 60)
    
    import time
    
    def process_in_batches(urls, batch_size=5, delay=60):
        """Process URLs in batches with delay"""
        transcriber = YouTubeTranscriber()
        all_results = []
        
        for i in range(0, len(urls), batch_size):
            batch = urls[i:i+batch_size]
            batch_num = i // batch_size + 1
            
            print(f"\n📦 Processing batch {batch_num} ({len(batch)} videos)")
            
            results = transcriber.process_multiple_videos(batch)
            all_results.extend(results)
            
            # Delay between batches (rate limiting)
            if i + batch_size < len(urls):
                print(f"⏳ Waiting {delay}s before next batch...")
                time.sleep(delay)
        
        return all_results
    
    urls = [f"https://youtu.be/VIDEO_{i}" for i in range(15)]
    # results = process_in_batches(urls, batch_size=5, delay=30)


def example_custom_output():
    """Example: Custom output formatting"""
    print("\nAdvanced Example 4: Custom Output")
    print("=" * 60)
    
    def export_to_markdown(json_path: str) -> str:
        """Convert transcript to Markdown format"""
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        markdown = f"""# {data['title']}

## Metadata
- **URL**: [{data['url']}]({data['url']})
- **Video ID**: `{data['video_id']}`
- **Date**: {data['timestamp']}
- **Word Count**: {data['word_count']}

## Transcript

{data['transcript']}

---
*Transcribed with YouTube Transcriber Pro*
"""
        return markdown
    
    # Example usage
    json_path = "transcripts/01_example_video.json"
    if Path(json_path).exists():
        markdown = export_to_markdown(json_path)
        
        # Save as markdown
        md_path = json_path.replace('.json', '.md')
        with open(md_path, 'w') as f:
            f.write(markdown)
        
        print(f"✅ Exported to: {md_path}")


def example_statistics():
    """Example: Generate statistics from transcripts"""
    print("\nAdvanced Example 5: Statistics")
    print("=" * 60)
    
    def get_statistics():
        """Get statistics from all transcripts"""
        transcripts_dir = Path("transcripts")
        
        if not transcripts_dir.exists():
            return None
        
        stats = {
            'total_videos': 0,
            'total_words': 0,
            'avg_words': 0,
            'languages': {},
            'videos': []
        }
        
        for json_file in transcripts_dir.glob("*.json"):
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                    
                    stats['total_videos'] += 1
                    stats['total_words'] += data.get('word_count', 0)
                    
                    lang = data.get('language', 'unknown')
                    stats['languages'][lang] = stats['languages'].get(lang, 0) + 1
                    
                    stats['videos'].append({
                        'title': data['title'],
                        'words': data['word_count']
                    })
            except:
                continue
        
        if stats['total_videos'] > 0:
            stats['avg_words'] = stats['total_words'] / stats['total_videos']
        
        return stats
    
    stats = get_statistics()
    
    if stats:
        print(f"📊 Total Videos: {stats['total_videos']}")
        print(f"📝 Total Words: {stats['total_words']:,}")
        print(f"📈 Average Words: {stats['avg_words']:.0f}")
        print(f"🌍 Languages: {stats['languages']}")


def example_cost_estimation():
    """Example: Estimate transcription costs"""
    print("\nAdvanced Example 6: Cost Estimation")
    print("=" * 60)
    
    def estimate_cost(duration_minutes: int) -> dict:
        """Estimate cost for transcription"""
        cost_per_minute = 0.006
        
        return {
            'duration_minutes': duration_minutes,
            'cost_usd': duration_minutes * cost_per_minute,
            'cost_per_hour': 60 * cost_per_minute
        }
    
    # Example durations
    durations = [10, 30, 60, 120]
    
    print("\n💰 Cost Estimates:")
    print("-" * 40)
    
    for duration in durations:
        estimate = estimate_cost(duration)
        print(f"{duration:3d} min → ${estimate['cost_usd']:.2f} USD")
    
    print(f"\nRate: ${estimate['cost_per_hour']:.2f} per hour")


if __name__ == "__main__":
    # Run examples (uncomment as needed)
    # example_parallel_processing()
    example_caching()
    # example_batch_processing()
    # example_custom_output()
    example_statistics()
    example_cost_estimation()
