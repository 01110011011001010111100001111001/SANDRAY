# Changelog

All notable changes to SANDRAY will be documented in this file.

---

## v2.0-alpha2

### Added

- Rich terminal interface
- External YAML configuration
- Modular project structure
- Git and GitHub integration
- SSH authentication
- Configurable conversation memory
- Configurable AI response behaviour

### Refactored

- Extracted Whisper into `speech/whisper.py`
- Extracted Piper into `speech/piper.py`
- Extracted recorder into `audio/recorder.py`
- Extracted AI interface into `ai/chat.py`
- Extracted conversation memory into `ai/memory.py`

---

## v2.0-alpha1

### Added

- Initial project structure
- Git repository
- GitHub repository

---

## v2.0-alpha2 (continued)

### Added (post-initial alpha2 stabilization)

- Introduced centralized subprocess execution layer (`core.process.run_process`)
- Structured AI memory model using role/content objects
- Refactored prompt builder into section-based composition system
- Added configuration validation layer (`config/loader.py`)
- Clarified UI ownership: Display now fully responsible for rendering
- Decoupled logging from UI rendering responsibilities

### Internal Improvements

- Standardized external process execution (Whisper, Piper, AI backend)
- Improved module isolation and testability
- Strengthened separation between AI logic, memory, and prompt construction
- Improved runtime logging consistency through centralized process layer

