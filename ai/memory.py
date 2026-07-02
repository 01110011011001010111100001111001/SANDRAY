class Memory:

    def __init__(self, max_turns=20, enabled=True):
        self.enabled = enabled
        self.history = []
        self.turns = 0
        self.max_turns = max_turns

    def add_user(self, text):
        if self.enabled:
            self.history.append("User: " + text)

    def add_assistant(self, text):
        if self.enabled:
            self.history.append("Assistant: " + text)
            self.turns += 1

            if self.turns > self.max_turns:
                self.history = []
                self.turns = 0

    def prompt(self):
        if not self.enabled:
            return ""

        return "\n".join(self.history)
