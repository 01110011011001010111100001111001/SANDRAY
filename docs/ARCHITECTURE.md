# SANDRAY Architecture

## Overview

SANDRAY is designed around a modular architecture.

The main application (`assistant.py`) coordinates the workflow while specialised modules perform individual tasks.

```
Microphone
    │
    ▼
audio.recorder
    │
    ▼
speech.whisper
    │
    ▼
ai.memory
    │
    ▼
ai.prompt
    │
    ▼
ai.chat
    │
    ▼
speech.piper
    │
    ▼
Speaker
```

## Directory Layout

```
assistant.py

ai/
    chat.py
    memory.py
    prompt.py

audio/
    recorder.py

speech/
    whisper.py
    piper.py

ui/
    display.py

config/
    config.yaml
```

## Design Principles

- One responsibility per module.
- Configuration lives in `config.yaml`.
- `assistant.py` coordinates modules and contains minimal business logic.
- Each module can be tested independently.
- Features should be configurable wherever practical.
