# SANDRAY Architecture

## Principles

- Keep assistant.py small and focused.
- Separate presentation from business logic.
- Prefer small, reversible changes.
- Minimise dependencies between modules.

## High-Level Components

assistant.py
    |
    +-- Engine
    +-- Conversation
    +-- UI
    +-- Configuration
    +-- Services

Each component should have a single responsibility and communicate through well-defined interfaces.
