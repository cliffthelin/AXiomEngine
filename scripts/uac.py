#!/usr/bin/env python3
import re
import sys

DANGEROUS_PATTERNS = [
    r"rm\s+-rf",
    r"drop\s+(table|database)",
    r"truncate\s+table",
    r"mkfs",
    r"dd\s+if="
]

class UAC:
    """
    User Account Control (UAC) for AXiomEngine.
    Intercepts dangerous commands and requires explicit approval.
    """
    @staticmethod
    def is_dangerous(command: str) -> bool:
        for pattern in DANGEROUS_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                return True
        return False

    @staticmethod
    def request_approval(command: str, reason: str) -> bool:
        print(f"\n[UAC WARNING] The agent wants to execute a potentially destructive command:")
        print(f"Command: {command}")
        print(f"Reason:  {reason}")
        
        while True:
            response = input("Do you approve this action? (y/N): ").strip().lower()
            if response == 'y':
                return True
            elif response == 'n' or response == '':
                return False
            else:
                print("Please enter 'y' or 'n'.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if UAC.is_dangerous(cmd):
            approved = UAC.request_approval(cmd, "Manual check")
            if approved:
                print("Approved.")
            else:
                print("Denied.")
        else:
            print("Command is safe.")
