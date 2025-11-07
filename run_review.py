"""
run_review.py
-------------
Quick demo runner for the Multi-Agent Code Reviewer system.

Usage:
    python run_review.py
"""

from reviewer_core.orchestrator import review_file
from rich.console import Console
from rich.table import Table

console = Console()

def display_findings(title: str, findings, color: str):
    """Pretty-print a list of findings in a rich table."""
    if not findings:
        console.print(f"[green]✅ No {title.lower()} found.[/green]")
        return

    table = Table(title=f"{title}", header_style=f"bold {color}")
    table.add_column("Rule ID", style="cyan", no_wrap=True)
    table.add_column("Line", style="yellow")
    table.add_column("Message", style="white")
    for f in findings:
        table.add_row(f.rule_id, str(f.line), f.message)
    console.print(table)


if __name__ == "__main__":
    filepath = "datasets/examples/bad_example.py"
    console.print(f"[bold cyan]🚀 Running full code review on:[/bold cyan] {filepath}\n")

    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()

    bundle = review_file(filepath, code)

    display_findings("🧩 Static Analysis Findings", bundle.static_findings, "magenta")
    display_findings("🛡️ Security Findings", bundle.security_findings, "red")

    console.print("\n🤖 [bold magenta]Gemini Review Comments:[/bold magenta]\n")
    if bundle.llm_comments:
        console.print(bundle.llm_comments[0].message)
    else:
        console.print("[yellow]No LLM feedback returned.[/yellow]")

    console.print("\n[bold green]🎯 Review complete![/bold green]")
