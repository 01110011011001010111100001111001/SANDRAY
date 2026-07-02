from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule

console = Console()


class Display:

    def clear(self):
        console.clear()

    def header(self, version):

        console.print(
            Panel.fit(
                f"[bold]SANDRAY[/bold]\nVersion {version}",
                border_style="white"
            )
        )

    def status(self, text):

        console.print(f"\nStatus : {text}")

    def divider(self):

        console.print(Rule())

    def user(self, text):

        console.print("\nYOU\n")
        console.print(text)

    def assistant(self, text):

        console.print("\nSANDRAY\n")
        console.print(text)

    def footer(self):

        console.print(Rule())
        console.print("Waiting...")
