from typing import Union


class Constraint:
    """A helper class utilized for defining constraints when lexing regions."""

    def __init__(self, constraints: dict):
        self.constraints = [constraints]

    def __or__(self, other: "Has") -> "Constraint":
        self.constraints.append({"constraint": other.constraint, "occurrences": other.occurrences})
        return self


class Has:
    """A helper class used for lexing regions, and created for syntactic sugar."""

    def __init__(self, string_or_type: Union[str, type], *, occurrences: int = None):
        self.constraint = string_or_type
        self.occurrences = occurrences

    def __or__(self, other: "Has") -> Constraint:
        return Constraint({"constraint": other.constraint, "occurrences": other.occurrences})

