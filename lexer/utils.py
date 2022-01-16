from typing import Union


class Constraint:
    """A helper class utilized for defining constraints when lexing regions."""

    def __init__(self, *constraints):
        self.constraints = [*constraints]

    def __repr__(self):
        return f"Constraints({self.constraints})"

    def __or__(self, other: "Has") -> "Constraint":
        self.constraints.append({"constraint": other.constraint, "occurrences": other.occurrences})
        return self

    def __eq__(self, other: "Constraint") -> bool:
        """__eq__ is defined for testing purposes."""
        return self.constraints == other.constraints


class Has:
    """A helper class used for lexing regions, and created for syntactic sugar."""

    def __init__(self, string_or_type: Union[str, type], *, occurrences: int = None):
        self.constraint = string_or_type
        self.occurrences = occurrences

    def __or__(self, other: "Has") -> Constraint:
        return Constraint(
            {"constraint": self.constraint, "occurrences": self.occurrences},
            {"constraint": other.constraint, "occurrences": other.occurrences}
        )

