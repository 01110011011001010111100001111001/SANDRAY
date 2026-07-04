class Memory:
    def __init__(self, max_turns=20, enabled=True):
        self.enabled = enabled
        self.max_turns = max_turns
        self.history = []

    def add_user(self, text):
        self._add("user", text)

    def add_assistant(self, text):
        self._add("assistant", text)

    def prompt(self):
        if not self.enabled:
            return ""

        lines = []

        for message in self.history:
            role = message["role"].capitalize()
            content = message["content"]
            lines.append(f"{role}: {content}")

        return "\n".join(lines)

    def _add(self, role, content):
        if not self.enabled:
            return

        self.history.append(
            {
                "role": role,
                "content": str(content),
            }
        )

        self._prune()

    def _prune(self):
        max_messages = self.max_turns * 2

        if max_messages <= 0:
            self.history.clear()
            return

        self.history = self.history[-max_messages:]
