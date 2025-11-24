"""
YouTube API Test Script
Run this to verify your API key is working.
"""

import sys
sys.path.insert(0, "src")

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

console = Console()

def test_api():
    """Test YouTube API connection."""
    
    console.print("\n[bold cyan]YouTube SEO AGI Tool - API Test[/bold cyan]\n")
    
    # Check API key
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        console.print("[bold red]ERROR: YOUTUBE_API_KEY not found![/bold red]")
        console.print("\n[yellow]Please create a .env file with your API key:[/yellow]")
        console.print("  1. Copy .env.example to .env")
        console.print("  2. Replace 'your_api_key_here' with your actual YouTube API key")
        console.print("\n[dim]Get your API key from: https://console.cloud.google.com/apis/credentials[/dim]")
        return False
    
    console.print(f"[green]OK: API Key found[/green] (ends with ...{api_key[-4:]})")
    
    # Test API connection
    try:
        from utils.youtube_client import YouTubeClient
        
        console.print("[yellow]Connecting to YouTube API...[/yellow]")
        client = YouTubeClient(api_key)
        
        # Test with target channel
        target_handle = "anatolianturkishrock"
        console.print(f"\n[cyan]Fetching channel: @{target_handle}[/cyan]")
        
        channel_data = client.get_channel_by_handle(target_handle)
        
        if channel_data.get("items"):
            channel = channel_data["items"][0]
            snippet = channel["snippet"]
            stats = channel["statistics"]
            
            # Display channel info
            table = Table(title="Channel Info", show_header=False, border_style="cyan")
            table.add_column("Property", style="bold")
            table.add_column("Value")
            
            table.add_row("Channel ID", channel["id"])
            table.add_row("Title", snippet["title"])
            table.add_row("Description", snippet["description"][:100] + "..." if len(snippet.get("description", "")) > 100 else snippet.get("description", "N/A"))
            table.add_row("Subscribers", f"{int(stats.get('subscriberCount', 0)):,}")
            table.add_row("Total Views", f"{int(stats.get('viewCount', 0)):,}")
            table.add_row("Video Count", stats.get("videoCount", "N/A"))
            table.add_row("Created", snippet.get("publishedAt", "N/A")[:10])
            
            console.print(table)
            
            # Get videos
            console.print("\n[cyan]Fetching videos...[/cyan]")
            videos = client.get_channel_videos(channel["id"], max_results=10)
            
            if videos:
                video_table = Table(title="Recent Videos", border_style="magenta")
                video_table.add_column("#", style="dim")
                video_table.add_column("Title", max_width=50)
                video_table.add_column("Views", justify="right")
                video_table.add_column("Likes", justify="right")
                video_table.add_column("Comments", justify="right")
                
                for i, video in enumerate(videos[:6], 1):
                    v_snippet = video["snippet"]
                    v_stats = video.get("statistics", {})
                    
                    video_table.add_row(
                        str(i),
                        v_snippet["title"][:50],
                        f"{int(v_stats.get('viewCount', 0)):,}",
                        f"{int(v_stats.get('likeCount', 0)):,}",
                        v_stats.get("commentCount", "N/A")
                    )
                
                console.print(video_table)
            
            console.print(Panel(
                "[bold green]SUCCESS: API Test Successful![/bold green]\n\n"
                "Your YouTube API is working correctly.\n"
                "You can now use the SEO tools.",
                title="Success",
                border_style="green"
            ))
            
            return True
        else:
            console.print("[red]ERROR: Channel not found[/red]")
            return False
            
    except Exception as e:
        console.print(f"[bold red]ERROR: API Error: {e}[/bold red]")
        console.print("\n[yellow]Common issues:[/yellow]")
        console.print("  • Invalid API key")
        console.print("  • YouTube Data API not enabled in Google Cloud Console")
        console.print("  • Quota exceeded")
        return False


if __name__ == "__main__":
    success = test_api()
    sys.exit(0 if success else 1)

