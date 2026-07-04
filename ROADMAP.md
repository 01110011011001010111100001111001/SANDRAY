# SANDRAY-v2 Design Rules

## Goal

SANDRAY is a local-first voice assistant designed for the uConsole.

It should feel reliable, calm, and appliance-like.

---

## Architecture

`assistant.py` is the entry point only.

Runtime flow:

assistant.py
↓
modules only

Modules:

- audio/ → recording and capture
- speech/ → wake word, Whisper, Piper
- ai/ → memory, prompt, chat
- ui/ → terminal rendering only
- core/ → execution + logging utilities

---

## Entry Point Rule

assistant.py must remain minimal and act only as a coordinator.

It should not contain:
- business logic
- UI rendering
- audio logic
- speech logic
- AI logic

---

## Current Phase

### M03 — COMPLETE
- AI chat subsystem
- memory system (structured model)
- prompt builder (section-based)

---

### M04 — PLATFORM HARDENING (ACTIVE)

Focus:
- configuration loader (`config/loader.py`)
- system startup stability
- execution consistency via core.process
- improved diagnostics and logging

---

### M05 — ADAPTIVE UI (DEFINED)

Focus:
- uConsole landscape-first layout
- portrait fallback (stacked layout)
- performance panel alignment (UI-006)
- engine header reduction (UI-005)
- open source footer panel (UI-007)
- terminal geometry adaptation (UI-008)

---

## Frozen Areas

The following subsystems should remain stable unless explicitly agreed:

- audio capture pipeline
- whisper integration
- piper synthesis

---

## UI Principles

- prioritize conversation visibility
- minimize vertical waste
- stable panel layout
- adaptive rendering based on terminal size
- designed for small handheld screens

---

## Working Rules

- think before changing architecture
- one change at a time
- no speculative refactors
- preserve backward compatibility
- prefer atomic commits
