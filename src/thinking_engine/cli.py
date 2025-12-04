"""CLI for the Thinking Engine."""

from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from dotenv import load_dotenv

from .document_loaders import DocumentLoader
from .llm_orchestrator import LLMOrchestrator
from .blog_generator import BlogGenerator
from .tweet_generator import TweetGenerator

load_dotenv()

app = typer.Typer(help="AI Content Thinking Engine - Generate blog posts and tweets from curated research")
console = Console()


def _select_week_folder(loader: DocumentLoader) -> str:
    folders = loader.list_week_folders()
    if not folders:
        console.print("[red]No week folders found in data/ directory[/red]")
        console.print("Please create a folder like: data/week-2024-01-15/")
        raise typer.Exit(1)
    
    console.print("\n[bold]Available week folders:[/bold]")
    for i, folder in enumerate(folders, 1):
        console.print(f"  {i}. {folder}")
    
    choice = Prompt.ask("\nSelect week folder (number or name)", default="1")
    try:
        return folders[int(choice) - 1] if choice.isdigit() else choice
    except (ValueError, IndexError):
        return choice


@app.command()
def generate_blog(week_folder: Optional[str] = typer.Argument(None, help="Week folder name")):
    """Generate a blog post from curated documents."""
    loader = DocumentLoader()
    
    if not week_folder:
        week_folder = _select_week_folder(loader)
    
    console.print(f"\n[cyan]Loading documents from {week_folder}...[/cyan]")
    try:
        docs = loader.load_week_folder(week_folder)
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
    
    if not docs:
        console.print("[red]No documents found in the selected folder[/red]")
        raise typer.Exit(1)
    
    console.print(f"[green]Loaded {len(docs)} documents[/green]")
    for doc in docs:
        console.print(f"  • {doc.title} ({doc.source})")
    
    try:
        llm = LLMOrchestrator()
        blog_gen = BlogGenerator(llm)
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        console.print("[yellow]Make sure OPENAI_API_KEY is set in .env file[/yellow]")
        raise typer.Exit(1)
    
    output_path = f"output/{week_folder}/blog-post.md"
    console.print(f"\n[bold]Generating blog post...[/bold]")
    
    try:
        result = blog_gen.generate(docs, output_path)
        console.print(f"\n[green]✓ Blog post generated![/green]")
        console.print(f"  Output: {result['output_file']}")
        console.print(f"  Citations: {result['fact_check']['citation_count']}")
        
        if result['fact_check']['has_issues']:
            console.print(f"\n[yellow]⚠ Fact-check found some issues - please review[/yellow]")
    except Exception as e:
        console.print(f"[red]Error generating blog post: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def generate_tweets(
    week_folder: Optional[str] = typer.Argument(None, help="Week folder name"),
    count: int = typer.Option(25, "--count", "-c", help="Number of tweet ideas")
):
    """Generate tweet ideas from curated documents."""
    loader = DocumentLoader()
    
    if not week_folder:
        week_folder = _select_week_folder(loader)
    
    console.print(f"\n[cyan]Loading documents from {week_folder}...[/cyan]")
    try:
        docs = loader.load_week_folder(week_folder)
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
    
    if not docs:
        console.print("[red]No documents found in the selected folder[/red]")
        raise typer.Exit(1)
    
    console.print(f"[green]Loaded {len(docs)} documents[/green]")
    
    try:
        llm = LLMOrchestrator()
        tweet_gen = TweetGenerator(llm, count=count)
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        console.print("[yellow]Make sure OPENAI_API_KEY is set in .env file[/yellow]")
        raise typer.Exit(1)
    
    output_dir = f"output/{week_folder}"
    console.print(f"\n[bold]Generating {count} tweet ideas...[/bold]")
    
    try:
        result = tweet_gen.generate(docs, output_dir)
        console.print(f"\n[green]✓ Tweet ideas generated![/green]")
        console.print(f"  JSON: {result['json_file']}")
        console.print(f"  Text: {result['txt_file']}")
        console.print(f"  Count: {result['tweet_count']}")
        
        if result['fact_check']['has_issues']:
            console.print(f"\n[yellow]⚠ Fact-check found some issues - please review[/yellow]")
    except Exception as e:
        console.print(f"[red]Error generating tweets: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def generate_all(
    week_folder: Optional[str] = typer.Argument(None, help="Week folder name"),
    tweet_count: int = typer.Option(25, "--tweet-count", "-c", help="Number of tweet ideas")
):
    """Generate both blog post and tweet ideas."""
    generate_blog(week_folder)
    generate_tweets(week_folder, tweet_count)
    console.print("\n[bold green]✓ All content generated![/bold green]")


@app.command()
def list_weeks():
    """List all available week folders."""
    loader = DocumentLoader()
    folders = loader.list_week_folders()
    
    if not folders:
        console.print("[yellow]No week folders found in data/ directory[/yellow]")
        console.print("Create folders like: data/week-2024-01-15/")
        return
    
    table = Table(title="Available Week Folders")
    table.add_column("Week Folder", style="cyan")
    table.add_column("Status", style="green")
    
    for folder in folders:
        try:
            docs = loader.load_week_folder(folder)
            table.add_row(folder, f"{len(docs)} documents")
        except:
            table.add_row(folder, "Error loading")
    
    console.print(table)


if __name__ == "__main__":
    app()
