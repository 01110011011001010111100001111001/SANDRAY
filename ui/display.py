from datetime import datetime

from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text
from rich import box

from core.process import get_verbose_lines
from core.logger import get_performance_panel


console = Console()


class Display:
    def __init__(self):
        self.version = ""
        self.current_status = "READY"
        self.mode = "MANUAL MODE"
        self.history = []
        self.logger = None

        self.theme = {
            "brand": "bold cyan",
            "muted": "dim",
            "ready": "green",
            "listening": "yellow",
            "thinking": "magenta",
            "speaking": "cyan",
            "error": "red",
            "user": "bold green",
            "assistant": "bold cyan",
            "instruction": "bold yellow",
            "assistant_border": "cyan",
            "status_border": "green",
            "conversation_border": "blue",
            "verbose_border": "magenta",
        }

    def attach_logger(self, logger):
        self.logger = logger

    def clear(self):
        console.clear()

    def header(self, version):
        self.version = version
        self._render()

    def status(self, text):
        self.current_status = text.upper()
        self._render()

    def instruction(self, text):
        self.history.append(
            self._entry("INSTRUCTION", text, self.theme["instruction"])
        )
        self._render()

    def divider(self):
        self._render()

    def user(self, text):
        self.history.append(
            self._entry("YOU", text, self.theme["user"])
        )
        self._render()

    def assistant(self, text):
        self.history.append(
            self._entry("SANDRAY", text, self.theme["assistant"])
        )
        self._render()

    def footer(self):
        pass

    def set_mode(self, mode):
        self.mode = str(mode).upper()
        self._render()

    def error(self, subsystem, message):
        self.current_status = "ERROR"
        self.history.append(
            self._entry(
                "ERROR",
                f"{subsystem}: {message}",
                self.theme["error"],
            )
        )
        self._render()

    def _entry(self, speaker, message, style):
        return {
            "time": self._clock(),
            "speaker": speaker,
            "message": str(message).strip(),
            "style": style,
        }

    def _render(self):
        console.clear()

        top = Table.grid(expand=True)
        top.add_column(ratio=1)
        top.add_column(ratio=1)
        top.add_row(
            self._assistant_panel(),
            self._status_panel(),
        )

        lower = Table.grid(expand=True)
        lower.add_column(ratio=1)
        lower.add_column(ratio=1)
        lower.add_row(
            self._verbose_panel(),
            self._performance_panel(),
        )

        console.print(top)
        console.print(self._conversation_panel())
        console.print(lower)

    def _assistant_panel(self):
        grid = Table.grid(expand=True)
        grid.add_column(justify="left", ratio=1)
        grid.add_column(justify="right")

        grid.add_row(
            Text("SANDRAY", style=self.theme["brand"]),
            Text(f"Version {self.version}", style=self.theme["muted"]),
        )

        return Panel(
            grid,
            title="ASSISTANT",
            title_align="left",
            border_style=self.theme["assistant_border"],
            box=box.SQUARE,
            padding=(1, 2),
            expand=True,
        )

    def _status_panel(self):
        status = self.current_status
        style = self._status_style(status)

        grid = Table.grid(expand=True)
        grid.add_column(justify="left", ratio=1)
        grid.add_column(justify="right")

        grid.add_row(
            Text(status, style=f"bold {style}"),
            Text(
                self._clock(),
                style=self.theme["muted"]
            ),
        )

        return Panel(
            grid,
            title="STATUS",
            title_align="left",
            border_style=style,
            box=box.SQUARE,
            padding=(1, 2),
            expand=True,
        )

    def _conversation_panel(self):
        table = Table.grid(expand=True)
        table.add_column(ratio=1)

        if not self.history:
            table.add_row(
                Align.left(
                    Text(
                        "Ready for a typed or spoken request.",
                        style=self.theme["muted"],
                    )
                )
            )
        else:
            conversation = [
                entry for entry in self.history
                if entry["speaker"] in ("YOU", "SANDRAY")
            ]

            for entry in conversation[-8:]:
                header = Table.grid(expand=True)
                header.add_column(justify="left", ratio=1)
                header.add_column(justify="right")

                header.add_row(
                    Text(entry["speaker"], style=entry["style"]),
                    Text(entry["time"], style=self.theme["muted"]),
                )

                table.add_row(header)
                table.add_row(Text(entry["message"], style="white"))
                table.add_row(Rule(style="dim"))

        return Panel(
            table,
            title="CONVERSATION",
            title_align="left",
            border_style=self.theme["conversation_border"],
            box=box.SQUARE,
            padding=(1, 2),
            expand=True,
        )

    def _verbose_panel(self):
        lines = get_verbose_lines()

        if not lines:
            lines = ["No technical output captured."]

        lines = lines[-10:]

        table = Table(
            expand=True,
            box=box.SIMPLE,
            show_header=True,
            header_style="bold magenta",
        )

        table.add_column("OUTPUT", style="dim")

        for line in lines:
            table.add_row(str(line))

        while len(table.rows) < 10:
            table.add_row("")

        return Panel(
            table,
            title="ENGINE",
            title_align="left",
            border_style=self.theme["verbose_border"],
            box=box.SQUARE,
            padding=(1, 2),
            expand=True,
        )

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

        if self.logger is not None:
            for name in order:
                if name in self.logger.timings:
                    found = True
                    label = name
                    elapsed = f"{self.logger.timings[name]:.2f} s"

                    if name == "TOTAL":
                        label = "[bold red]TOTAL[/bold red]"
                        elapsed = f"[bold red]{elapsed}[/bold red]"

                    table.add_row(label, elapsed, "[green]OK[/green]")

            for name, value in self.logger.stats.items():
                found = True
                table.add_row(str(name), "", str(value))

        if not found:
            table.add_row("SYSTEM", "", "Waiting for first completed turn.")

        ROWS = 10

        while len(table.rows) < ROWS:
            table.add_row("", "", "")

        return Panel(
            table,
            title="PERFORMANCE",
            title_align="left",
            border_style="red",
            box=box.SQUARE,
            padding=(1, 2),
            expand=True,
        )

    def _status_style(self, status):
        styles = {
            "READY": self.theme["ready"],
            "LISTENING": self.theme["listening"],
            "THINKING": self.theme["thinking"],
            "SPEAKING": self.theme["speaking"],
            "ERROR": self.theme["error"],
        }

        return styles.get(status, "white")

    def _clock(self):
        return datetime.now().strftime("%H:%M:%S")
