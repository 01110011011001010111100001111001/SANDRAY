import time

from core.process import add_verbose_line


class Logger:
    def __init__(self, level="INFO"):
        self.level = level
        self.starts = {}
        self.timings = {}
        self.stats = {}
        self.events = []

    def start(self, name):
        self.starts[name] = time.time()
        self.log(name, "started")

    def stop(self, name):
        if name not in self.starts:
            return

        self.timings[name] = time.time() - self.starts[name]
        self.log(
            name,
            f"completed in {self.timings[name]:.2f} s"
        )

    def log(self, name, message):
        event = {
            "time": time.strftime("%H:%M:%S"),
            "name": str(name),
            "message": str(message),
        }

        self.events.append(event)
        self.events = self.events[-50:]

        add_verbose_line(name, message)

    def stat(self, name, value):
        self.stats[str(name)] = str(value)

    def summary(self):
        # Compatibility method.
        # Rendering is owned by ui.display.Display.
        return {
            "timings": self.get_timings(),
            "stats": self.get_stats(),
            "events": self.get_events(),
        }

    def get_timings(self):
        return dict(self.timings)

    def get_stats(self):
        return dict(self.stats)

    def get_events(self):
        return list(self.events)
