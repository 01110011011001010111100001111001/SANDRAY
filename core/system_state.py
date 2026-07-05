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
        stats = net_if_stats()
        io = net_io_counters()

        active_iface = None
        for iface, s in stats.items():
            if s.isup and iface != "lo":
                active_iface = iface
                break

        return {
            "wifi": active_iface or "unknown",
            "signal": "active" if active_iface else "down",
            "internet": "online" if io.bytes_sent > 0 else "unknown"
        }
    except Exception:
        return {
            "wifi": "unknown",
            "signal": "unknown",
            "internet": "unknown"
        }
import psutil

def get_system_state():
    try:
        return {
            "cpu": round(psutil.cpu_percent(interval=0.1), 1),
            "temp": "n/a",
            "mem": round(psutil.virtual_memory().percent, 1)
        }
    except Exception:
        return {
            "cpu": 0,
            "temp": "unknown",
            "mem": 0
        }

import subprocess

def _run(cmd):
    try:
        return subprocess.check_output(cmd, shell=True).decode().strip()
    except:
        return None


def get_network_state():
    try:
        ssid = _run("nmcli -t -f active,ssid dev wifi | grep '^yes' | cut -d: -f2")

        bluetooth = _run("rfkill list bluetooth | grep -i 'Soft blocked'")

        interfaces = _run("ls /sys/class/net")
        active_iface = None
        for iface in (interfaces or "").split():
            if iface != "lo":
                active_iface = iface
                break

        return {
            "interface": active_iface or "unknown",
            "ssid": ssid or "not connected",
            "bluetooth": bluetooth or "unknown",
            "connection": "wifi" if ssid else "none",
        }

    except Exception:
        return {
            "interface": "error",
            "ssid": "error",
            "bluetooth": "error",
            "connection": "error",
        }

import os

def get_system_state():
    try:
        import psutil

        # CPU + memory (real)
        cpu = psutil.cpu_percent(interval=0.1)
        mem = psutil.virtual_memory().percent

        # battery (Linux sysfs)
        battery = "unknown"
        bat_path = "/sys/class/power_supply"
        if os.path.exists(bat_path):
            for b in os.listdir(bat_path):
                if "BAT" in b:
                    try:
                        with open(f"{bat_path}/{b}/capacity") as f:
                            battery = f.read().strip() + "%"
                    except:
                        battery = "unknown"

        # temperature (best-effort)
        temp = "unknown"
        try:
            with open("/sys/class/thermal/thermal_zone0/temp") as f:
                temp = str(int(f.read().strip()) / 1000) + "C"
        except:
            pass

        return {
            "cpu": cpu,
            "mem": mem,
            "battery": battery,
            "temp": temp,
            "device": os.uname().nodename,
            "mic": "system device (not directly queryable)",
            "speaker": "system device (not directly queryable)",
        }

    except Exception:
        return {
            "cpu": 0,
            "mem": 0,
            "battery": "error",
            "temp": "error",
            "device": "unknown",
            "mic": "unknown",
            "speaker": "unknown",
        }

import os
import subprocess

def _run(cmd):
    try:
        return subprocess.check_output(cmd, shell=True).decode().strip()
    except:
        return None


def get_network_state():
    iface = None
    try:
        for i in os.listdir("/sys/class/net"):
            if i != "lo":
                iface = i
                break
    except:
        pass

    ssid = _run("nmcli -t -f active,ssid dev wifi | grep '^yes' | cut -d: -f2")
    bt = _run("rfkill list bluetooth | grep -i 'Soft blocked'")

    return {
        "interface": iface,
        "ssid": ssid,
        "bluetooth": bt,
        "connection": "wifi" if ssid else None
    }


import psutil
import os
import platform

def get_system_state():
    cpu = psutil.cpu_percent(interval=0.1)
    mem = psutil.virtual_memory().percent

    battery = None
    try:
        base = "/sys/class/power_supply"
        for b in os.listdir(base):
            if "BAT" in b:
                with open(f"{base}/{b}/capacity") as f:
                    battery = f.read().strip()
    except:
        pass

    temp = None
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            temp = str(int(f.read()) / 1000)
    except:
        pass

    return {
        "cpu": cpu,
        "mem": mem,
        "battery": battery,
        "temp": temp,
        "device": platform.node()
    }


def get_network_state():
    import os

    # interface detection (REAL)
    iface = None
    try:
        for i in os.listdir("/sys/class/net"):
            if i != "lo":
                iface = i
                break
    except:
        iface = None

    # wireless signal (REAL if exists)
    signal = None
    try:
        with open("/proc/net/wireless", "r") as f:
            lines = f.readlines()
            if len(lines) > 2:
                parts = lines[2].split()
                signal = parts[2] if len(parts) > 2 else None
    except:
        signal = None

    # bluetooth (ONLY if rfkill output exists via system command fallback)
    bluetooth = None
    try:
        import subprocess
        bluetooth = subprocess.getoutput("rfkill list bluetooth | grep -i 'Soft blocked'")
    except:
        bluetooth = None

    return {
        "interface": iface,
        "signal": signal,
        "bluetooth": bluetooth,
        "connection": "unknown"
    }


def get_system_state():
    import psutil
    import os
    import platform

    cpu = psutil.cpu_percent(interval=0.1)
    mem = psutil.virtual_memory().percent

    # REAL battery (only if exists)
    battery = None
    try:
        base = "/sys/class/power_supply"
        if os.path.exists(base):
            for b in os.listdir(base):
                if "BAT" in b:
                    with open(f"{base}/{b}/capacity") as f:
                        battery = f.read().strip()
    except:
        battery = None

    # REAL temperature (only kernel exposed)
    temp = None
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            temp = str(int(f.read().strip()) / 1000)
    except:
        temp = None

    return {
        "cpu": cpu,
        "mem": mem,
        "battery": battery,
        "temp": temp,
        "device": platform.node()
    }

