# Display System TODOs

This file is the UI implementation backlog.

It does not approve new features by itself. UI work must map to `ROADMAP.md`.

## UI-001 — ViewModel UI Contract

- Ensure UI panels consume structured ViewModel data.
- Prevent panels from calling system probes directly.
- Preserve existing visible behaviour during migration.

## UI-003 — Layout Stabilization

- Ensure all panels have consistent alignment.
- Prevent duplicated rendering of panels.
- Prevent nested panel structures.
- Preserve clean multi-column layout when terminal width allows.
- Avoid full-width override unless explicitly required.

## UI-004 — NETWORKS Panel

- Display WiFi SSID.
- Display WiFi signal strength.
- Display Bluetooth connection status.
- Display cellular availability.
- Display internet connectivity state.

## UI-005 — HARDWARE Panel

- Show exact microphone device in use.
- Show exact speaker/output device in use.
- Detect and display audio routing state.
- Detect audio jack usage status.
- Detect HDMI status and connected display device.
- Show CPU usage correctly.
- Show system temperature accurately.
- Show battery percentage and charging state.

## UI-006 — ENGINE Panel

- Display real runtime state.
- Reflect actual CPU/system activity where appropriate.
- Avoid empty or placeholder-only output when real data exists.

## UI-007 — PERFORMANCE Panel

- Show reliable timing data.
- Show process statistics from the logger.
- Preserve completed turn timing visibility.

## Theme Consistency

- Ensure all panel borders use defined theme values.
- Prevent missing theme keys causing crashes.
- Ensure fallback styles exist for all UI elements.

## Debugging Visibility

- Maintain ability to see system errors clearly.
- Ensure errors are not hidden inside panel rendering.
- Ensure system status remains visible when other panels fail.
