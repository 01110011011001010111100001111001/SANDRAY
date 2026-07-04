import time

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

from core.process import add_verbose_line


console = Console()
_LAST_PERFORMANCE_PANEL = None


class Logger:
    def __init__(self, level="INFO"):
        self.level = level
        self.starts = {}
        self.timings = {}
        self.stats = {}

    def start(self, name):
        self.starts[name] = time.time()
        add_verbose_line(name, "started")

    def stop(self, name):
        if name in self.starts:
            self.timings[name] = time.time() - self.starts[name]
            add_verbose_line(
                name,
                f"completed in {self.timings[name]:.2f} s",
            )

    def log(self, name, message):
        add_verbose_line(name, message)

    def stat(self, name, value):
        self.stats[name] = value

    def summary(self):
        global _LAST_PERFORMANCE_PANEL
        _LAST_PERFORMANCE_PANEL = self._performance_panel()

    def _performance_panel(self):
        table = Table(
            expand=True,
            box=box.SIMPLE,
            show_header=True,
            header_style="bold red",
        )

        table.add_column("PROCESS", style="white", no_wrap=True)
        table.add_column("TIME", justify="right", style="white", no_wrap=True)
        table.add_column("DETAIL", style="white")

        order = [
            "WAKE_WORD",
            "RECORDER",
            "WHISPER",
            "AI",
            "PIPER",
            "PLAYBACK",
            "TOTAL",
        ]

        found = False

        for name in order:
            if name in self.timings:
                found = True
                label = name
                elapsed = f"{self.timings[name]:.2f} s"

                if name == "TOTAL":
                    label = "[bold red]TOTAL[/bold red]"
                    elapsed = f"[bold red]{elapsed}[/bold red]"

                table.add_row(label, elapsed, "[green]OK[/green]")

        for name, value in self.stats.items():
            found = True
            table.add_row(str(name), "", str(value))

        if not found:
            table.add_row("SYSTEM", "", "No performance data recorded.")

        return Panel(
            table,
            title="PERFORMANCE",
            title_align="left",
            border_style="red",
            box=box.SQUARE,
            padding=(1, 2),
            expand=True,
        )


def get_performance_panel():
    if _LAST_PERFORMANCE_PANEL is None:
        table = Table(
            expand=True,
            box=box.SIMPLE,
            show_header=True,
            header_style="bold red",
        )

        table.add_column("PROCESS", style="white", no_wrap=True)
        table.add_column("TIME", justify="right", style="white", no_wrap=True)
        table.add_column("DETAIL", style="white")
        table.add_row("SYSTEM", "", "No performance data recorded.")

        return Panel(
            table,
            title="PERFORMANCE",
            title_align="left",
            border_style="red",
            box=box.SQUARE,
            padding=(1, 2),
            expand=True,
        )

    return _LAST_PERFORMANCE_PANEL
