from datetime import datetime

from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text
from rich import box

console = Console()


class Display:
    def __init__(self):
        self.version = ""
        self.current_status = "READY"
        self.mode = "MANUAL MODE"
        self.history = []
        self.logs = []

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
            "border": "cyan",
            "conversation": "blue",
            "performance": "red",
            "footer": "dim",
            "log": "white",
        }

    def clear(self):
        console.clear()

    def header(self, version):
        self.version = version
        self._render()

    def status(self, text):
        self.current_status = text.upper()
        self._render()

    def instruction(self, text):
        self.history.append(self._entry("INSTRUCTION", text, self.theme["instruction"]))
        self._render()

    def divider(self):
        self._render()

    def user(self, text):
        self.history.append(self._entry("YOU", text, self.theme["user"]))
        self._render()

    def assistant(self, text):
        self.history.append(self._entry("SANDRAY", text, self.theme["assistant"]))
        self._render()

    def footer(self):
        self._render()

    def log(self, subsystem, message):
        self.logs.append((self._clock(), str(subsystem), str(message)))
        self.logs = self.logs[-8:]
        self._render()

    def set_mode(self, mode):
        self.mode = str(mode).upper()
        self._render()

    def error(self, subsystem, message):
        self.current_status = "ERROR"
        self.history.append(
            self._entry("ERROR", f"{subsystem}: {message}", self.theme["error"])
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
        console.print(self._header_panel())
        console.print(self._status_panel())
        console.print(self._conversation_panel())
        console.print(self._footer_panel())

    def _header_panel(self):
        grid = Table.grid(expand=True)
        grid.add_column(justify="left", ratio=1)
        grid.add_column(justify="right")

        grid.add_row(
            Text("SANDRAY", style=self.theme["brand"]),
            Text(f"Version {self.version}", style=self.theme["muted"]),
        )

        return Panel(
            grid,
            border_style=self.theme["border"],
            box=box.SQUARE,
            padding=(1, 2),
            expand=True,
        )

    def _status_panel(self):
        status = self.current_status
        style = self._status_style(status)

        grid = Table.grid(expand=True)
        grid.add_column(justify="left", ratio=1)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right", ratio=1)

        grid.add_row(
            Text(f"STATUS  {status}", style=f"bold {style}"),
            Text(self.mode, style=self.theme["muted"]),
            Text(self._clock(), style=self.theme["muted"]),
        )

        return Panel(
            grid,
            border_style=style,
            box=box.SQUARE,
            padding=(0, 2),
            expand=True,
        )

    def _conversation_panel(self):
        table = Table.grid(expand=True)
        table.add_column(ratio=1)

        if not self.history:
            table.add_row(
                Align.left(
                    Text("Ready for a typed or spoken request.", style=self.theme["muted"])
                )
            )
        else:
            for entry in self.history[-8:]:
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
            border_style=self.theme["conversation"],
            box=box.SQUARE,
            padding=(1, 2),
            expand=True,
        )

    def _footer_panel(self):
        grid = Table.grid(expand=True)
        grid.add_column(justify="left", ratio=1)
        grid.add_column(justify="right")

        grid.add_row(
            Text("ENTER=talk   q=quit", style=self.theme["footer"]),
            Text("local-first assistant", style=self.theme["footer"]),
        )

        return Panel(
            grid,
            border_style="dim",
            box=box.SQUARE,
            padding=(0, 2),
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
