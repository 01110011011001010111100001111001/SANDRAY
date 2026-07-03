"""
SANDRAY

Developer logger.
"""

import time


class Logger:

    def __init__(self, level="normal"):
        self.level = level
        self.timers = {}
        self.results = {}
        self.stats = {}

    def log(self, module, message):
        if self.level != "developer":
            return

        print(f"[{module:<9}] {message}")

    def start(self, name):
        if self.level != "developer":
            return

        self.timers[name] = time.perf_counter()

    def stop(self, name):
        if self.level != "developer":
            return

        if name not in self.timers:
            return

        self.results[name] = time.perf_counter() - self.timers[name]
        del self.timers[name]

    def stat(self, name, value):
        if self.level != "developer":
            return

        self.stats[name] = value

    def summary(self):
        if self.level != "developer":
            return

        print()
        print("-" * 60)
        print("PERFORMANCE")
        print()

        measured_total = self.results.get("TOTAL")

        for name, value in self.results.items():
            if name == "TOTAL":
                continue

            print(f"{name:<10} {value:7.2f} s")

        if self.stats:
            print()

            for name, value in self.stats.items():
                print(f"{name:<10} {value}")

        print()

        if measured_total is not None:
            print(f"{'TOTAL':<10} {measured_total:7.2f} s")
        else:
            total = sum(self.results.values())
            print(f"{'TOTAL':<10} {total:7.2f} s")

        print("-" * 60)

        self.timers.clear()
        self.results.clear()
        self.stats.clear()
