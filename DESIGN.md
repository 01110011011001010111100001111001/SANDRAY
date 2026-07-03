# SANDRAY-v2 Design Rules

## Goal

SANDRAY is a local-first voice assistant for Raspberry Pi 4.

It should feel reliable, calm, and appliance-like.

## Architecture

`assistant.py` is the entry point only.

Runtime flow:

assistant.py
↓
modules only

Modules:

- `audio/` handles recording and audio capture
- `speech/` handles wake word, Whisper, and Piper
- `ai/` handles prompts, memory, and model calls
- `ui/` handles terminal presentation only
- `core/` handles logging and shared control utilities

## Entry Point Rule

`assistant.py` should eventually be under 100 lines.

It should not contain business logic, UI formatting, audio logic, speech logic, or AI logic.

## Frozen Areas

Do not change these unless explicitly agreed:

- audio playback
- microphone capture
- Piper
- Whisper
- wake-word architecture

## Current Priority

Improve only the Rich terminal UI.

## UI Principles

The interface should be:

- full-width
- left-aligned
- calm and professional
- colour-coded but not noisy
- readable at different terminal widths
- suitable for daily use
- clear about system state

## Working Rules

- Think first, code second
- One complete change at a time
- No speculative fixes
- Preserve backwards compatibility
- Minimise file changes
- Do not redesign architecture without agreement
- Prefer terminal commands over manual edits
