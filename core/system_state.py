import psutil
import subprocess


# ---------------- CORE SYSTEM METRICS ----------------

def get_system_state():
    return {
        "cpu": psutil.cpu_percent(interval=0.1),
        "temp": _get_temp()
    }


def _get_temp():
    try:
        temps = psutil.sensors_temperatures()
        for v in temps.values():
            if v:
                return v[0].current
    except:
        pass
    return 0.0


# ---------------- NETWORK ----------------

def get_network_state():
    try:
        out = subprocess.check_output(
            ["nmcli", "-t", "-f", "ssid,signal", "dev", "wifi"],
            stderr=subprocess.DEVNULL
        ).decode().strip()

        if not out:
            return {"wifi": "Unavailable", "signal": 0}

        line = out.split("\\n")[0]
        parts = line.split(":")
        return {
            "wifi": parts[0] if len(parts) > 0 else "Unknown",
            "signal": parts[1] if len(parts) > 1 else 0,
            "bluetooth": "Unknown",
            "cellular": "Unavailable",
            "internet": "Online"
        }

    except:
        return {
            "wifi": "Unavailable",
            "signal": 0,
            "bluetooth": "Unknown",
            "cellular": "Unavailable",
            "internet": "Offline"
        }


# ---------------- AUDIO ----------------

def get_audio_state():
    return {
        "sink": "default",
        "port": "analog-output",
        "mic": "active",
        "speaker": "active"
    }


# ---------------- HDMI ----------------

def get_hdmi_state():
    try:
        out = subprocess.check_output(["xrandr"], stderr=subprocess.DEVNULL).decode()
        for line in out.splitlines():
            if " connected " in line:
                return {
                    "status": "Connected",
                    "device": line.split()[0]
                }
        return {"status": "Disconnected", "device": None}
    except:
        return {"status": "Unknown", "device": None}
