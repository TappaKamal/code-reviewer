"""
Good Example File
-----------------
This file is intentionally clean and well-structured
to verify that the analyzer does not report false positives.
"""

from typing import List

def greet_user(name: str) -> str:
    """Return a polite greeting for a given user name."""
    return f"Hello, {name}!"

def add_numbers(numbers: List[int]) -> int:
    """Add a list of numbers safely."""
    return sum(numbers)

class Greeter:
    """Example class using best practices."""

    def __init__(self, prefix: str = "Hello"):
        self.prefix = prefix

    def greet(self, user: str) -> str:
        return f"{self.prefix}, {user}!"

if __name__ == "__main__":
    greeter = Greeter()
    print(greeter.greet("Hello COder! "))
