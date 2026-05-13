#!/usr/bin/env python3
import sys

def prompt_user(question: str, options: list = None) -> str:
    """
    User Interrupt / Form utility.
    Pauses execution and prompts the user for structured input.
    """
    print("\n" + "="*50)
    print("🤖 AXIOMENGINE REQUIRES YOUR INPUT")
    print("="*50)
    print(f"❓ {question}")
    
    if options:
        for i, opt in enumerate(options, 1):
            print(f"  {i}. {opt}")
        
        while True:
            choice = input(f"\nSelect an option (1-{len(options)}): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(options):
                return options[int(choice)-1]
            print("Invalid selection.")
    else:
        return input("\nYour response: ").strip()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        q = sys.argv[1]
        opts = sys.argv[2].split(",") if len(sys.argv) > 2 else None
        res = prompt_user(q, opts)
        print(f"\n[RECEIVED]: {res}")
    else:
        print("Usage: python user_prompt.py 'Question' 'Option1,Option2'")
