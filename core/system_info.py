import subprocess
import os


def get_wifi_ssid():
    try:
        return subprocess.check_output(
            "nmcli -t -f active,ssid dev wifi | grep '^yes' | cut -d: -f2",
            shell=True
        ).decode().strip() or "Disconnected"
    except:
        return "Unavailable"


def get_bluetooth_device():
    try:
        return subprocess.check_output(
            "bluetoothctl info | grep 'Name' | cut -d' ' -f2-",
            shell=True
        ).decode().strip() or "None"
    except:
        return "Unavailable"


# -------------------------
# REAL AUDIO DEVICE INFO
# -------------------------

def get_audio_devices():
    """
    Returns actual ALSA/PulseAudio device names.
    """

    try:
        out = subprocess.check_output(
            "pactl list short sources",
            shell=True
        ).decode().strip().split("\n")

        sources = []
        for line in out:
            parts = line.split("\t")
            if len(parts) > 1:
                sources.append(parts[1])

        mic = sources[0] if sources else "No Mic Found"

    except:
        mic = "Mic Unknown"

    try:
        out = subprocess.check_output(
            "pactl list short sinks",
            shell=True
        ).decode().strip().split("\n")

        sinks = []
        for line in out:
            parts = line.split("\t")
            if len(parts) > 1:
                sinks.append(parts[1])

        speaker = sinks[0] if sinks else "No Speaker Found"

    except:
        speaker = "Speaker Unknown"

    return mic, speaker


def get_cpu():
    try:
        return f"{os.getloadavg()[0]:.2f}"
    except:
        return "N/A"


def get_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            return f"{int(f.read())/1000:.1f}°C"
    except:
        return "N/A"
