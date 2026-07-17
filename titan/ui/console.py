"""
console.py

Rich console UI for Titan.

Author: Titan Team
"""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from titan.planner.models import OptimizationRoadmap


class TitanConsole:
    """
    Rich console wrapper used throughout Titan.
    """

    def __init__(self):

        self.console = Console()

    def banner(self):

        title = Text(
            "⚡ TITAN AI ENGINEER ⚡",
            justify="center",
            style="bold cyan",
        )

        subtitle = Text(
            "AI Repository Optimization Platform",
            justify="center",
            style="green",
        )

        self.console.print(
            Panel.fit(
                f"{title}\n{subtitle}",
                border_style="cyan",
            )
        )

    def status(
        self,
        message: str,
    ):

        self.console.print(
            f"[green]✓[/green] {message}"
        )

    def info(
        self,
        message: str,
    ):

        self.console.print(
            f"[cyan]{message}[/cyan]"
        )

    def warning(
        self,
        message: str,
    ):

        self.console.print(
            f"[yellow]{message}[/yellow]"
        )

    def error(
        self,
        message: str,
    ):

        self.console.print(
            f"[red]{message}[/red]"
        )

    def roadmap(
        self,
        roadmap: OptimizationRoadmap,
    ):

        self.console.print()

        self.console.print(
            Panel.fit(
                f"[bold]Repository[/bold]\n"
                f"{roadmap.repository_name or "Unknown Repository"}\n\n"
                f"[bold]Summary[/bold]\n"
                f"{roadmap.summary}",
                title="Optimization Roadmap",
                border_style="blue",
            )
        )

        table = Table(
            show_lines=True
        )

        table.add_column(
            "Priority",
            style="cyan",
        )

        table.add_column(
            "Recommendation",
            style="green",
        )

        table.add_column(
            "Impact",
            style="yellow",
        )

        table.add_column(
            "Confidence",
            justify="right",
        )

        for recommendation in roadmap.recommendations:

            table.add_row(
                str(recommendation.priority),
                recommendation.title,
                recommendation.expected_impact,
                f"{recommendation.confidence:.0f}%",
            )

        self.console.print(table)

        for item in roadmap.recommendations:

            implementation = "\n".join(
                f"• {step}"
                for step in item.implementation_steps
            )

            if item.affected_files:

                affected = "\n".join(
                    item.affected_files
                )

            else:

                affected = (
                    "Requires repository-level analysis"
                )

            self.console.print(
                Panel.fit(
                    f"[bold cyan]{item.title}[/bold cyan]\n\n"

                    f"[green]Difficulty:[/green] "
                    f"{item.implementation_difficulty}\n"

                    f"[green]Estimated Speedup:[/green] "
                    f"{item.estimated_speedup} (LLM Estimate)\n"

                    f"[green]Confidence:[/green] "
                    f"{item.confidence:.0f}%\n\n"

                    f"[bold]Affected Files[/bold]\n"
                    f"{affected}\n\n"

                    f"[bold]Implementation Steps[/bold]\n"
                    f"{implementation}",
                    border_style="green",
                )
            )

        self.console.print(
            f"\n[bold green]Overall Confidence:[/bold green] "
            f"{roadmap.overall_confidence:.0f}%"
        )