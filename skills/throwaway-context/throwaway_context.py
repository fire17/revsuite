#!/usr/bin/env python3
"""
Skill: /throwaway-context
Outputs a goal to fill context to a specified percentage threshold.

Usage: /throwaway-context 25
"""

import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: /throwaway-context <threshold_percent>")
        print("Example: /throwaway-context 25")
        sys.exit(1)

    threshold = sys.argv[1]

    # Validate threshold is a number
    try:
        pct = int(threshold)
        if pct < 1 or pct > 100:
            print(f"Error: threshold must be between 1 and 100 (got {pct})")
            sys.exit(1)
    except ValueError:
        print(f"Error: threshold must be a number (got '{threshold}')")
        sys.exit(1)

    # Output the goal text with substituted percentage
    goal_text = (
        f"i want to test context fill, can you produce some throwaway text in some file "
        f"in steps until your context window is over {pct} percent, then stop and cleanup any "
        f"of the throwaway texts until now/then"
    )

    print(goal_text)

if __name__ == "__main__":
    main()
