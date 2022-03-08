from collections import defaultdict
from collections.abc import Callable, Iterable

BASE_CASE = None  # Used for the base case of dispatching token kinds


class TooManyOccurrences(Exception):
    """When the amount of occurrences specified in the constraints goes 'overboard'."""


class Constraint:
    """A helper class utilized for defining constraints when lexing regions."""

    def __init__(self, *constraints):
        self.constraints = [*constraints]
        self.existing_occurrences = defaultdict(int)
        self._stop_at_next = False

    def __repr__(self):
        return f"Constraints({self.constraints})"

    def __or__(self, other: "Has") -> "Constraint":
        self.constraints.append({
            "constraint": other.constraint,
            "occurrences": other.occurrences,
            "enforce_occurrences": other.enforce_occurrences
        })
        return self

    def __contains__(self, item: str):
        if self._stop_at_next:
            return False

        all_conditions = []

        for constraint in self.constraints:
            if isinstance(constraint["constraint"], type):
                try:
                    constraint["constraint"](item)
                    all_conditions.append(True)
                except ValueError:
                    all_conditions.append(False)
            elif isinstance(constraint["constraint"], Callable):
                all_conditions.append(constraint["constraint"](item))
            else:
                all_conditions.append(item == constraint["constraint"])

            if constraint["occurrences"] is not None:
                if all_conditions[-1]:
                    self.existing_occurrences[constraint["constraint"]] += 1
                if constraint["occurrences"] < self.existing_occurrences[constraint["constraint"]]:
                    raise TooManyOccurrences(self.existing_occurrences[constraint["constraint"]])

            if constraint["enforce_occurrences"]:
                if constraint["occurrences"] == self.existing_occurrences[constraint["constraint"]]:
                    self._stop_at_next = True

        return any(all_conditions)

    def __eq__(self, other: "Constraint") -> bool:
        """__eq__ is defined for testing purposes."""
        return self.constraints == other


class Has:
    """A helper class used for lexing regions, and created for syntactic sugar."""

    def __init__(
        self,
        string_type_or_method: str | type | Callable,
        *,
        occurrences: int = None,
        enforce_occurrences: bool = False
    ):
        self.constraint = string_type_or_method
        self.occurrences = occurrences
        self.enforce_occurrences = enforce_occurrences

    def __or__(self, other: "Has") -> Constraint:
        return Constraint(
            {
                "constraint": self.constraint,
                "occurrences": self.occurrences,
                "enforce_occurrences": self.enforce_occurrences
            },
            {
                "constraint": other.constraint,
                "occurrences": other.occurrences,
                "enforce_occurrences": other.enforce_occurrences
            }
        )


class In:
    """Helper class for checking if the token value is in the iterable provided, for dispatching the token kind."""

    def __init__(self, iterable: Iterable):
        self.iterable = iterable
