"""
YouTube SEO AGI Tool - Main CLI Interface
Universal Self-Evolving Open-Source AGI Assistant for YouTube SEO
"""

import sys
import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from dotenv import load_dotenv
import os

# Load environment
load_dotenv()

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from utils.youtube_client import YouTubeClient, YouTubeAPIError
from modules.channel_analyzer import ChannelAnalyzer
from modules.keyword_researcher import KeywordResearcher
from modules.competitor_analyzer import CompetitorAnalyzer
from modules.title_optimizer import TitleOptimizer
from modules.description_generator import DescriptionGenerator
from modules.tag_suggester import TagSuggester
from modules.trend_predictor import TrendPredictor
from modules.proactive_advisor import ProactiveAdvisor

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """
    YouTube SEO AGI Tool
    
    Universal Self-Evolving Open-Source AGI Assistant
    for optimizing YouTube channel performance.
    
    Target: @anatolianturkishrock
    """
    pass


@cli.command()
def test():
    """Test YouTube API connection."""
    console.print("\n[bold cyan]Testing YouTube API Connection...[/bold cyan]\n")
    
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        console.print("[bold red]ERROR: YOUTUBE_API_KEY not found in .env file[/bold red]")
        return
    
    try:
        client = YouTubeClient(api_key)
        channel_data = client.get_channel_by_handle("anatolianturkishrock")
        
        if channel_data.get("items"):
            channel = channel_data["items"][0]
            console.print(f"[green]SUCCESS:[/green] Connected to YouTube API")
            console.print(f"Channel: [cyan]{channel['snippet']['title']}[/cyan]")
        else:
            console.print("[red]ERROR: Channel not found[/red]")
    except Exception as e:
        console.print(f"[bold red]ERROR: {e}[/bold red]")


@cli.command()
@click.option("--handle", default="anatolianturkishrock", help="Channel handle (without @)")
def channel(handle):
    """Analyze channel statistics."""
    console.print(f"\n[bold cyan]Analyzing Channel: @{handle}[/bold cyan]\n")
    
    try:
        client = YouTubeClient()
        channel_data = client.get_channel_by_handle(handle)
        
        if not channel_data.get("items"):
            console.print("[red]Channel not found[/red]")
            return
        
        channel = channel_data["items"][0]
        snippet = channel["snippet"]
        stats = channel["statistics"]
        
        # Channel Info Table
        table = Table(title="Channel Statistics", show_header=False, border_style="cyan")
        table.add_column("Metric", style="bold")
        table.add_column("Value", style="cyan")
        
        table.add_row("Channel ID", channel["id"])
        table.add_row("Title", snippet["title"])
        table.add_row("Subscribers", f"{int(stats.get('subscriberCount', 0)):,}")
        table.add_row("Total Views", f"{int(stats.get('viewCount', 0)):,}")
        table.add_row("Total Videos", stats.get("videoCount", "N/A"))
        table.add_row("Created", snippet.get("publishedAt", "N/A")[:10])
        
        console.print(table)
        
        # Get videos
        console.print("\n[yellow]Fetching video details...[/yellow]")
        videos = client.get_channel_videos(channel["id"], max_results=50)
        
        if videos:
            # Video Performance Table
            video_table = Table(title="Video Performance", border_style="magenta")
            video_table.add_column("#", style="dim", width=3)
            video_table.add_column("Title", max_width=40)
            video_table.add_column("Views", justify="right", style="cyan")
            video_table.add_column("Likes", justify="right", style="green")
            video_table.add_column("Comments", justify="right", style="yellow")
            video_table.add_column("CTR", justify="right", style="dim")
            
            for i, video in enumerate(videos, 1):
                v_snippet = video["snippet"]
                v_stats = video.get("statistics", {})
                
                views = int(v_stats.get("viewCount", 0))
                likes = int(v_stats.get("likeCount", 0))
                comments = int(v_stats.get("commentCount", 0))
                
                # Calculate engagement rate (simplified)
                engagement = (likes + comments) / max(views, 1) * 100
                
                video_table.add_row(
                    str(i),
                    v_snippet["title"][:40],
                    f"{views:,}",
                    f"{likes:,}",
                    str(comments),
                    f"{engagement:.2f}%"
                )
            
            console.print(video_table)
            
            # Summary Stats
            total_views = sum(int(v.get("statistics", {}).get("viewCount", 0)) for v in videos)
            total_likes = sum(int(v.get("statistics", {}).get("likeCount", 0)) for v in videos)
            avg_views = total_views / len(videos) if videos else 0
            
            summary = Table(title="Summary", show_header=False, border_style="green")
            summary.add_column("Metric", style="bold")
            summary.add_column("Value", style="green")
            summary.add_row("Total Videos Analyzed", str(len(videos)))
            summary.add_row("Total Views", f"{total_views:,}")
            summary.add_row("Total Likes", f"{total_likes:,}")
            summary.add_row("Average Views/Video", f"{avg_views:,.0f}")
            
            console.print("\n")
            console.print(summary)
        
    except YouTubeAPIError as e:
        console.print(f"[bold red]API Error: {e}[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")


@cli.command()
@click.argument("query")
@click.option("--max", default=10, help="Maximum results")
def search(query, max):
    """Search YouTube for videos matching query."""
    console.print(f"\n[bold cyan]Searching: {query}[/bold cyan]\n")
    
    try:
        client = YouTubeClient()
        results = client.search_videos(query, max_results=max)
        
        if results:
            table = Table(title=f"Search Results for: {query}", border_style="yellow")
            table.add_column("#", style="dim")
            table.add_column("Title", max_width=50)
            table.add_column("Channel", max_width=30)
            table.add_column("Published", style="dim")
            
            for i, item in enumerate(results, 1):
                snippet = item["snippet"]
                table.add_row(
                    str(i),
                    snippet["title"][:50],
                    snippet["channelTitle"][:30],
                    snippet["publishedAt"][:10]
                )
            
            console.print(table)
        else:
            console.print("[yellow]No results found[/yellow]")
            
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")


@cli.command()
def suggest():
    """Get keyword suggestions for your niche."""
    console.print("\n[bold cyan]Keyword Suggestions for Psychedelic Anatolian Rock[/bold cyan]\n")
    
    queries = [
        "psychedelic anatolian rock",
        "turkish rock music",
        "anadolu rock",
        "70s turkish rock",
        "turkish psychedelic"
    ]
    
    try:
        client = YouTubeClient()
        
        all_suggestions = set()
        
        for query in queries:
            console.print(f"[yellow]Fetching suggestions for: {query}...[/yellow]")
            suggestions = client.get_search_suggestions(query)
            all_suggestions.update(suggestions)
            if len(all_suggestions) >= 50:
                break
        
        if all_suggestions:
            # Display as columns
            suggestions_list = sorted(list(all_suggestions))[:50]
            
            table = Table(title="Keyword Suggestions", border_style="green")
            table.add_column("Keywords", style="cyan")
            
            for i in range(0, len(suggestions_list), 3):
                row = " | ".join(suggestions_list[i:i+3])
                table.add_row(row)
            
            console.print(table)
            console.print(f"\n[dim]Total suggestions: {len(suggestions_list)}[/dim]")
        else:
            console.print("[yellow]No suggestions found[/yellow]")
            
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")


@cli.command()
@click.option("--handle", default="anatolianturkishrock", help="Channel handle")
def analyze(handle):
    """Comprehensive channel analysis."""
    console.print(f"\n[bold cyan]Analyzing Channel: @{handle}[/bold cyan]\n")
    
    try:
        client = YouTubeClient()
        analyzer = ChannelAnalyzer(client)
        analysis = analyzer.analyze_channel(handle)
        
        # Display key metrics
        stats = analysis["statistics"]
        console.print("[bold]Channel Statistics:[/bold]")
        console.print(f"  Subscribers: {stats['subscribers']:,}")
        console.print(f"  Total Views: {stats['total_views']:,}")
        console.print(f"  Videos: {stats['total_videos']}")
        console.print(f"  Avg Views/Video: {stats['average_views_per_video']:,.0f}")
        
        # Recommendations
        console.print("\n[bold]Recommendations:[/bold]")
        for rec in analysis["recommendations"]:
            console.print(f"  • {rec}")
            
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")


@cli.command()
@click.argument("title")
@click.option("--song", help="Song name")
def optimize_title(title, song):
    """Optimize video title for SEO."""
    console.print(f"\n[bold cyan]Optimizing Title: {title}[/bold cyan]\n")
    
    try:
        client = YouTubeClient()
        keyword_researcher = KeywordResearcher(client)
        optimizer = TitleOptimizer(keyword_researcher)
        
        variations = optimizer.generate_title_variations(title, song, num_variations=5)
        
        table = Table(title="Title Variations (Ranked by SEO Score)", border_style="green")
        table.add_column("#", style="dim")
        table.add_column("Title", max_width=50)
        table.add_column("Score", justify="right")
        table.add_column("Length", justify="right")
        
        for i, var in enumerate(variations, 1):
            table.add_row(
                str(i),
                var["title"],
                str(var["seo_score"]),
                str(var["length"])
            )
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")


@cli.command()
@click.argument("title")
@click.option("--song", help="Song name")
def generate_desc(title, song):
    """Generate SEO-optimized video description."""
    console.print(f"\n[bold cyan]Generating Description for: {title}[/bold cyan]\n")
    
    try:
        generator = DescriptionGenerator()
        result = generator.generate_description(title, song)
        
        console.print("[bold]Generated Description:[/bold]")
        console.print(result["description"])
        
        console.print(f"\n[bold]Analysis:[/bold]")
        console.print(f"  Word Count: {result['word_count']}")
        console.print(f"  Character Count: {result['character_count']}")
        console.print(f"  SEO Score: {result['analysis']['seo_score']}/100")
        
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")


@cli.command()
@click.argument("title")
@click.option("--song", help="Song name")
def suggest_tags(title, song):
    """Suggest optimized tags for video."""
    console.print(f"\n[bold cyan]Suggesting Tags for: {title}[/bold cyan]\n")
    
    try:
        client = YouTubeClient()
        suggester = TagSuggester(client)
        result = suggester.suggest_tags(title, song)
        
        console.print("[bold]Suggested Tags:[/bold]")
        console.print(", ".join(result["suggested_tags"]))
        
        console.print(f"\n[bold]Analysis:[/bold]")
        console.print(f"  Total Tags: {result['tag_count']}")
        console.print(f"  Optimization Score: {result['analysis']['optimization_score']}/100")
        
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")


@cli.command()
def proactive():
    """Get proactive suggestions and alerts."""
    console.print("\n[bold cyan]Proactive Advisor - Getting Suggestions...[/bold cyan]\n")
    
    try:
        client = YouTubeClient()
        channel_analyzer = ChannelAnalyzer(client)
        competitor_analyzer = CompetitorAnalyzer(client)
        advisor = ProactiveAdvisor(client, channel_analyzer, competitor_analyzer)
        
        suggestions = advisor.get_proactive_suggestions("anatolianturkishrock")
        
        if suggestions.get("alerts"):
            console.print("[bold yellow]Alerts:[/bold yellow]")
            for alert in suggestions["alerts"]:
                console.print(f"  [{alert['type'].upper()}] {alert['title']}: {alert['message']}")
        
        if suggestions.get("suggestions"):
            console.print("\n[bold green]Suggestions:[/bold green]")
            for suggestion in suggestions["suggestions"]:
                console.print(f"  • {suggestion['title']}: {suggestion['message']}")
        
        if suggestions.get("priority_actions"):
            console.print("\n[bold cyan]Priority Actions:[/bold cyan]")
            for action in suggestions["priority_actions"]:
                console.print(f"  • {action}")
        
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")


@cli.command()
def info():
    """Show tool information and current status."""
    console.print(Panel(
        "[bold cyan]YouTube SEO AGI Tool[/bold cyan]\n\n"
        "[bold]Version:[/bold] 0.1.0\n"
        "[bold]Target Channel:[/bold] @anatolianturkishrock\n"
        "[bold]Niche:[/bold] Psychedelic Anatolian Rock\n\n"
        "[bold]Available Commands:[/bold]\n"
        "  • [cyan]test[/cyan] - Test API connection\n"
        "  • [cyan]channel[/cyan] - Analyze channel statistics\n"
        "  • [cyan]analyze[/cyan] - Comprehensive channel analysis\n"
        "  • [cyan]search <query>[/cyan] - Search YouTube\n"
        "  • [cyan]suggest[/cyan] - Get keyword suggestions\n"
        "  • [cyan]optimize-title <title>[/cyan] - Optimize video title\n"
        "  • [cyan]generate-desc <title>[/cyan] - Generate description\n"
        "  • [cyan]suggest-tags <title>[/cyan] - Suggest tags\n"
        "  • [cyan]proactive[/cyan] - Get proactive suggestions\n"
        "  • [cyan]info[/cyan] - Show this information\n\n"
        "[dim]Use --help with any command for more information[/dim]",
        title="Tool Information",
        border_style="blue"
    ))


if __name__ == "__main__":
    cli()

