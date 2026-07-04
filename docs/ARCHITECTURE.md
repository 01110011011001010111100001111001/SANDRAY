# SANDRAY Architecture

## Overview

SANDRAY is a modular, handheld AI assistant designed for the uConsole.

It is built around a central coordinator (`assistant.py`) and a set of independent modules with clearly defined responsibilities.

The system is not a linear pipeline. It is a coordinated execution model with shared services.

---

## System Coordination Model

assistant.py
    │
    ├── config (config.loader)
    ├── memory (ai.memory)
    ├── prompt builder (ai.prompt)
    ├── AI execution (ai.chat)
    ├── audio input (audio.recorder)
    ├── speech-to-text (speech.whisper)
    ├── text-to-speech (speech.piper)
    ├── UI rendering (ui.display)
    └── logging + metrics (core.logger + core.process)

---

## Core Execution Layer

### core.process

All external system calls are executed through `core.process.run_process()`.

This includes:

- AI backend execution
- Whisper transcription
- Piper speech synthesis
- system subprocess calls

Purpose:
- Standardise subprocess execution
- Centralise error handling
- Capture runtime output for diagnostics
- Provide unified logging integration

---

## Configuration System

Configuration is loaded from:

- `config/config.yaml`
- `config/loader.py` (validation layer introduced in M04)

This enables:
- centralised configuration management
- future deployment profiles
- separation of config definition and runtime behavior

---

## AI Subsystem

### ai.memory

Stores conversation state as structured records:

{ role: "user" | "assistant", content: string }

Features:
- bounded history
- automatic pruning
- session continuity

---

### ai.prompt

Builds structured prompts from sections:

- personality
- response rules
- memory context

No direct string concatenation pipeline.

---

### ai.chat

Executes AI backend only.

- no memory logic
- no prompt logic
- no UI logic
- uses core.process for execution

---

## Audio Pipeline

Microphone → recorder → whisper → AI → piper → Speaker

Each stage is isolated and independently testable.

---

## UI System

Terminal UI rendered via Rich.

Panels:
- ASSISTANT
- STATUS
- CONVERSATION
- ENGINE
- PERFORMANCE
- OPEN SOURCE

Design principles:
- uConsole-first layout
- minimal visual noise
- stable panel structure
- adaptive behavior (M05 direction)

---

## Design Principles

- single responsibility per module
- strict separation of concerns
- execution centralized in core.process
- UI isolated from logic
- configuration isolated
- system designed for constrained devices
