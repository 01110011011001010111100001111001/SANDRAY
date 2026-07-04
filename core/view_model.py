
# SINGLE SOURCE OF TRUTH FOR UI

import core.system_state as ss

def build_view():
    return {
        "status": "READY",
        "conversation": "Ready for input",
        "assistant": "SANDRAY",
        "engine": {
            "cpu": ss.get_cpu(),
            "temp": ss.get_temp()
        },
        "performance": {
            "battery": ss.get_battery()
        },
        "network": {
            "wifi": ss.get_wifi(),
            "bluetooth": ss.get_bluetooth()
        }
    }
