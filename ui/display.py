from datetime import datetime

from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text
from rich import box

from core.process import get_verbose_lines


console = Console()


class Display:
    def __init__(self):
        self.version = ""
        self.model = ""
        self.hostname = ""
        self.ip_address = ""
        self.current_status = "READY"
        self.mode = "MANUAL MODE"
        self.history = []
        self.logger = None

        self.theme = {}


    def set_theme(self, theme):
        self.theme = dict(theme)

    def attach_logger(self, logger):
        self.logger = logger

    def clear(self):
        console.clear()

    def header(self, version):
        self.version = version
        self._render()

    def configure_identity(
        self,
        model,
        hostname,
        ip_address
    ):
        self.model = str(model)
        self.hostname = str(hostname)
        self.ip_address = str(ip_address)

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

        console.print(
            self._two_panel_row(
                self._assistant_panel(),
                self._status_panel(),
            )
        )

        console.print(
            self._performance_panel()
        )

        console.print(
            self._conversation_panel()
        )

    def _two_panel_row(self, left, right):
        table = Table.grid(expand=True)
        table.add_column(ratio=1)
        table.add_column(ratio=1)
        table.add_row(left, right)
        return table

    def _assistant_panel(self):
        grid = Table.grid(expand=True)
        grid.add_column(justify="left", ratio=1)
        grid.add_column(justify="right")

        grid.add_row(
            Text(f"{self.hostname} {self.ip_address}", style=self.theme["brand"]),
            Text(self.model, style=self.theme["muted"]),
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
                table.add_row(Text(entry["message"], style=self.theme["normal"]))
                table.add_row(Rule(style=self.theme["rule"]))

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
            show_header=False,
            header_style=self.theme["table_header"],
        )

        table.add_column("OUTPUT", style=self.theme["table_text"])

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
        parts = []

        timing_order = [
            "TOTAL",
            "WAKE_WORD",
            "RECORDER",
            "WHISPER",
            "AI",
            "PIPER",
            "PLAYBACK",
        ]

        stats_order = [
            "INPUT",
            "OUTPUT",
        ]

        if self.logger is not None:
            timings = self.logger.get_timings()
            stats = self.logger.get_stats()

            for name in timing_order:
                if name in timings:
                    elapsed = f"{timings[name]:.2f} s"

                    if name == "TOTAL":
                        parts.append(
                            f"[bold red]{name} {elapsed}[/bold red]"
                        )

            for name in stats_order:
                if name in stats:
                    parts.append(f"{name} {stats[name]}")

            for name in timing_order:
                if name in timings and name != "TOTAL":
                    elapsed = f"{timings[name]:.2f} s"
                    parts.append(
                        f"{name} {elapsed} [green]OK[/green]"
                    )

            for name, value in stats.items():
                if name not in stats_order:
                    parts.append(f"{name} {value}")

        if not parts:
            parts.append("SYSTEM Waiting for first completed turn.")

        return Panel(
            Text.from_markup(" | ".join(parts)),
            title="SYSTEM",
            title_align="left",
            border_style=self.theme["system_border"],
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
