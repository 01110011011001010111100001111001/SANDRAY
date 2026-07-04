from rich.table import Table

from ui.theme import THEME
from core.system_state import (
    get_network_state,
    get_audio_state,
    get_hdmi_state,
    get_system_state,
)


def networks_panel():
    net = get_network_state()

    table = Table.grid(expand=True)
    table.add_column()

    table.add_row(f"WiFi        • {net.get('wifi')}")
    table.add_row(f"Bluetooth   • {net.get('bluetooth')}")
    table.add_row(f"Cellular    • {net.get('cellular')}")
    table.add_row(f"Internet    • {net.get('internet')}")

    return table


def hardware_panel():
    audio = get_audio_state()
    hdmi = get_hdmi_state()
    sys = get_system_state()

    table = Table.grid(expand=True)
    table.add_column()

    table.add_row(f"Microphone  • {audio.get('mic')}")
    table.add_row(f"Audio Port  • {audio.get('port')}")
    table.add_row(f"HDMI        • {hdmi.get('status')} ({hdmi.get('device')})")
    table.add_row(f"CPU         • {sys.get('cpu'):.2f}")
    table.add_row(f"Temp        • {sys.get('temp'):.1f}°C")
    table.add_row("Battery     • 87% Charging")

    return table
