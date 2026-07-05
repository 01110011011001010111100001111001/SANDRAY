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
        self.current_status = "READY"
        self.mode = "MANUAL MODE"
        self.history = []
        self.logger = None

        self._cached_conversation = None
        self._cache_dirty = True

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

    # ---------------- CORE ----------------

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
        self.history.append(self._entry("INSTRUCTION", text, self.theme["instruction"]))
        self._cache_dirty = True
        self._render()

    def divider(self):
        self._render()

    def user(self, text):
        self.history.append(self._entry("YOU", text, self.theme["user"]))
        self._cache_dirty = True
        self._render()

    def assistant(self, text):
        self.history.append(self._entry("SANDRAY", text, self.theme["assistant"]))
        self._cache_dirty = True
        self._render()

    def error(self, subsystem, message):
        self.current_status = "ERROR"
        self.history.append(
            self._entry("ERROR", f"{subsystem}: {message}", self.theme["error"])
        )
        self._cache_dirty = True
        self._render()

    def set_mode(self, mode):
        self.mode = str(mode).upper()
        self._render()

    def footer(self):
        pass

    # ---------------- ENTRY ----------------

    def _entry(self, speaker, message, style):
        return {
            "time": self._clock(),
            "speaker": speaker,
            "message": str(message).strip(),
            "style": style,
        }

    # ---------------- CACHE ----------------

    def _get_conversation(self):
        if not self._cache_dirty and self._cached_conversation is not None:
            return self._cached_conversation

        self._cached_conversation = [
            e for e in self.history if e["speaker"] in ("YOU", "SANDRAY")
        ]
        self._cache_dirty = False
        return self._cached_conversation

    # ---------------- VISUAL HELPERS (NEW) ----------------

    def _panel(self, title, border, content):
        return Panel(
            content,
            title=title,
            title_align="left",
            border_style=border,
            box=box.SQUARE,
            padding=(1, 2),
            expand=True,
        )

    def _grid(self, *rows):
        table = Table.grid(expand=True)
        table.add_column(ratio=1)
        for r in rows:
            table.add_row(r)
        return table

    # ---------------- RENDER ----------------

    def _render(self):
        console.clear()
        self._render_top()
        self._render_middle()
        self._render_bottom()

    def _render_top(self):
        console.print(
            self._two_panel_row(
                self._assistant_panel(),
                self._status_panel(),
            )
        )

    def _render_middle(self):
        console.print(self._conversation_panel())

    def _render_bottom(self):
        console.print(
            self._two_panel_row(
                self._verbose_panel(),
                self._performance_panel(),
            )
        )

    # ---------------- PANELS ----------------

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
            Text("SANDRAY", style=self.theme["brand"]),
            Text(f"Version {self.version}", style=self.theme["muted"]),
        )

        return self._panel("ASSISTANT", self.theme["assistant_border"], grid)

    def _status_panel(self):
        status = self.current_status
        style = self._status_style(status)

        grid = Table.grid(expand=True)
        grid.add_column(justify="left", ratio=1)
        grid.add_column(justify="right")

        grid.add_row(
            Text(status, style=f"bold {style}"),
            Text(self._clock(), style=self.theme["muted"]),
        )

        return self._panel("STATUS", style, grid)

    def _conversation_panel(self):
        table = Table.grid(expand=True)
        table.add_column(ratio=1)

        conv = self._get_conversation()

        if not conv:
            table.add_row(
                Align.left(Text("Ready for a typed or spoken request.", style=self.theme["muted"]))
            )
        else:
            for e in conv[-8:]:
                header = Table.grid(expand=True)
                header.add_column(justify="left", ratio=1)
                header.add_column(justify="right")

                header.add_row(
                    Text(e["speaker"], style=e["style"]),
                    Text(e["time"], style=self.theme["muted"]),
                )

                table.add_row(header)
                table.add_row(Text(e["message"], style="white"))
                table.add_row(Rule(style="dim"))

        return self._panel("CONVERSATION", self.theme["conversation_border"], table)

    def _verbose_panel(self):
        lines = get_verbose_lines() or ["No technical output captured."]
        lines = lines[-10:]

        table = Table(expand=True, box=box.SIMPLE, show_header=True, header_style="bold magenta")
        table.add_column("OUTPUT", style="dim")

        for l in lines:
            table.add_row(str(l))

        return self._panel("ENGINE", self.theme["verbose_border"], table)

    def _performance_panel(self):
        table = Table(expand=True, box=box.SIMPLE, show_header=True, header_style="bold red")

        table.add_column("PROCESS", style="white", no_wrap=True)
        table.add_column("TIME", justify="right", style="white", no_wrap=True)
        table.add_column("DETAIL", style="white")

        order = ["WAKE_WORD","RECORDER","WHISPER","AI","PIPER","PLAYBACK","TOTAL"]

        found = False

        if self.logger:
            timings = self.logger.get_timings()
            stats = self.logger.get_stats()

            for n in order:
                if n in timings:
                    found = True
                    t = f"{timings[n]:.2f} s"
                    if n == "TOTAL":
                        n = f"[bold red]{n}[/bold red]"
                        t = f"[bold red]{t}[/bold red]"
                    table.add_row(n, t, "[green]OK[/green]")

            for k, v in stats.items():
                found = True
                table.add_row(str(k), "", str(v))

        if not found:
            table.add_row("SYSTEM", "", "Waiting for first completed turn.")

        while len(table.rows) < 10:
            table.add_row("", "", "")

        return self._panel("PERFORMANCE", "red", table)

    # ---------------- STATUS ----------------

    def _status_style(self, status):
        return {
            "READY": self.theme["ready"],
            "LISTENING": self.theme["listening"],
            "THINKING": self.theme["thinking"],
            "SPEAKING": self.theme["speaking"],
            "ERROR": self.theme["error"],
        }.get(status, "white")

    def _clock(self):
        return datetime.now().strftime("%H:%M:%S")
