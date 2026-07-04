# SANDRAY

SANDRAY is a modular handheld AI assistant designed for the ClockworkPi uConsole.

It provides a voice-driven interface, but is built as a general-purpose local AI system with a clean modular architecture.

---

## Features

- Voice input using Whisper.cpp
- AI conversation via structured execution pipeline
- Speech synthesis using Piper
- Terminal-based Rich UI
- YAML-based configuration system
- Structured conversation memory
- Modular architecture with clear separation of concerns
- Centralized execution layer for external processes

---

## Core Architecture

SANDRAY is built around a modular system coordinated by `assistant.py`.

Key subsystems:

- ai/ → memory, prompt construction, AI execution
- audio/ → recording and input capture
- speech/ → Whisper transcription and Piper synthesis
- ui/ → terminal rendering (Rich-based display)
- core/ → execution and logging utilities
- config/ → configuration and validation layer

---

## Execution Model

SANDRAY is not a linear pipeline.

It uses a coordinated execution model:

assistant.py
→ modules
→ core.process (execution layer)

All external system calls are executed through a unified process abstraction layer.

---

## Project Structure

assistant.py          Main coordinator

ai/                   Memory, prompt, AI execution
audio/                Audio capture
speech/               Whisper + Piper pipeline
ui/                   Terminal interface
core/                 Execution + logging utilities
config/               Configuration system

---

## Status

Current version:

v2.0-alpha2

Architecture state:

- M03 completed (AI + memory + prompt refactor)
- M04 in progress (platform hardening, config loader)
- M05 defined (adaptive uConsole UI)

---

## Design Philosophy

- Modular by design
- Execution centralized through core.process
- UI separated from logic
- Configuration externalized
- Optimized for small handheld devices (uConsole)
