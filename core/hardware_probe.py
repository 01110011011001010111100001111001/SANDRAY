import subprocess


# ----------------------------
# AUDIO (REAL DEVICE + ACTIVE PORT)
# ----------------------------
def get_audio_route():
    try:
        sink = subprocess.check_output(
            "pactl get-default-sink",
            shell=True
        ).decode().strip()
    except:
        sink = "Unknown"

    try:
        port = subprocess.check_output(
            f"pactl list sinks | grep -A20 'Name: {sink}' | grep 'Active Port' | cut -d':' -f2",
            shell=True
        ).decode().strip()
    except:
        port = "Unknown"

    return sink, port


# ----------------------------
# HDMI (STATE + DEVICE)
# ----------------------------
def get_hdmi_status():
    try:
        out = subprocess.check_output(
            "cat /sys/class/drm/*HDMI*/status 2>/dev/null",
            shell=True
        ).decode().strip()

        return "Connected" if "connected" in out else "Disconnected"
    except:
        return "Unknown"


def get_hdmi_device():
    try:
        out = subprocess.check_output(
            "xrandr --query 2>/dev/null | grep ' connected' | grep HDMI | cut -d' ' -f1",
            shell=True
        ).decode().strip()

        if out:
            return out

        # fallback EDID name attempt
        edid = subprocess.check_output(
            "for f in /sys/class/drm/*HDMI*/edid; do cat $f 2>/dev/null | strings; done | head -n 1",
            shell=True
        ).decode().strip()

        return edid if edid else "Unknown Display"

    except:
        return "Unavailable"
