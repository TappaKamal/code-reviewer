"""
Command-Line Interface (CLI)
----------------------------
This file allows developers to run the Multi-Agent Code Reviewer
directly from the terminal.

Usage:
    python -m cli.main review <path_to_file>
"""

import json
import pathlib
import typer
from rich.console import Console
from rich.table import Table
from reviewer_core.orchestrator import review_file

app = typer.Typer(help="🤖 Multi-Agent Code Review CLI")
console = Console()


@app.command()
def review(path: str):
    """
    Run a full multi-agent review on the specified Python file.
    """
    file_path = pathlib.Path(path)
    if not file_path.exists():
        console.print(f"[red]❌ File not found:[/red] {path}")
        raise typer.Exit(code=1)

    console.print(f"[bold cyan]🔍 Starting code review for:[/bold cyan] {file_path.name}\n")

    code = file_path.read_text(encoding="utf-8")
    bundle = review_file(str(file_path), code)

    # --------------------------
    # Section 1: Static Findings
    # --------------------------
    if bundle.static_findings:
        table = Table(title="🧩 Static Analysis Findings", show_header=True, header_style="bold magenta")
        table.add_column("Rule ID", style="cyan", no_wrap=True)
        table.add_column("Line", style="yellow")
        table.add_column("Message", style="white")

        for f in bundle.static_findings:
            table.add_row(f.rule_id, str(f.line), f.message)
        console.print(table)
    else:
        console.print("[green]✅ No static issues found![/green]")

    # --------------------------
    # Section 2: Security Findings
    # --------------------------
    if bundle.security_findings:
        table = Table(title="🛡️ Security Warnings", show_header=True, header_style="bold red")
        table.add_column("Rule ID", style="cyan", no_wrap=True)
        table.add_column("Line", style="yellow")
        table.add_column("Message", style="white")

        for f in bundle.security_findings:
            table.add_row(f.rule_id, str(f.line), f.message)
        console.print(table)
    else:
        console.print("[green]✅ No security risks detected![/green]")

    # --------------------------
    # Section 3: LLM Reviewer Comments
    # --------------------------
    console.print("\n🤖 [bold magenta]Gemini Code Review:[/bold magenta]")
    llm_comment = bundle.llm_comments[0].message if bundle.llm_comments else "(No comments)"
    console.print(f"\n{llm_comment}")

    # --------------------------
    # Optional JSON output
    # --------------------------
    output_path = file_path.with_suffix(".review.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({
            "static": [f.__dict__ for f in bundle.static_findings],
            "security": [f.__dict__ for f in bundle.security_findings],
            "llm": [f.__dict__ for f in bundle.llm_comments],
        }, f, indent=2)
    console.print(f"\n💾 Review saved to [bold green]{output_path}[/bold green]\n")


if __name__ == "__main__":
    app()
