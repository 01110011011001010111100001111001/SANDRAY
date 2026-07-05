"""
SANDRAY

Module:
    core.view_model

Purpose:
    Builds the single data contract consumed by the UI.

Architecture:
    The UI should consume this module instead of calling low-level
    system probes directly.
"""

import core.system_state as ss


def build_view():
    """Return structured display data for UI panels."""

    system = ss.get_system_state()
    network = ss.get_network_state()
    audio = ss.get_audio_state()
    hdmi = ss.get_hdmi_state()

    return {
        "status": "READY",
        "conversation": "Ready for input",
        "assistant": "SANDRAY",
        "engine": {
            "cpu": system.get("cpu", 0.0),
            "temp": system.get("temp", 0.0),
        },
        "performance": {
            "battery": "Unknown",
        },
        "network": _network_view(network),
        "hardware": _hardware_view(
            audio,
            hdmi,
            system,
        ),
    }


def _network_view(network):
    return {
        "wifi": network.get("wifi", "Unknown"),
        "signal": network.get("signal", 0),
        "bluetooth": network.get("bluetooth", "Unknown"),
        "cellular": network.get("cellular", "Unavailable"),
        "internet": network.get("internet", "Unknown"),
    }


def _hardware_view(audio, hdmi, system):
    return {
        "mic": audio.get("mic", "Unknown"),
        "speaker": audio.get("speaker", "Unknown"),
        "sink": audio.get("sink", "Unknown"),
        "port": audio.get("port", "Unknown"),
        "hdmi_status": hdmi.get("status", "Unknown"),
        "hdmi_device": hdmi.get("device"),
        "cpu": system.get("cpu", 0.0),
        "temp": system.get("temp", 0.0),
        "battery": "Unknown",
        "charging": "Unknown",
    }
