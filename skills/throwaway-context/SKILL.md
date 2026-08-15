---
name: throwaway-context
description: Test context fill by producing throwaway text incrementally until the context window exceeds a specified percentage threshold, then clean up all temporary files. Use when the user types /throwaway-context or wants to fill/stress the context window to a target percent for testing.
argument-hint: "<threshold-percent>"
---

# throwaway-context

Test context fill by producing throwaway text incrementally until the context window exceeds a specified percentage threshold, then clean up all temporary files.

## Usage

```
/throwaway-context <threshold_percent>
```

Examples:
- `/throwaway-context 25` — Fill context to 25%
- `/throwaway-context 30` — Fill context to 30%

## What it does

When invoked, this skill:
1. Submits a goal via nexus that instructs the assistant to:
   - Create throwaway text files in the scratchpad directory
   - Monitor context window fill percentage incrementally
   - Stop when the threshold is exceeded
   - Clean up all temporary files created during the test

The goal executes asynchronously via nexus, respecting input-clear and idle conditions before delivery.

## Examples

```bash
/throwaway-context 25
/throwaway-context 35
/throwaway-context 15
```
