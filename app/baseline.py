from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class FieldComparison:
    field: str
    expected: Any
    actual: Any
    matches: bool


@dataclass
class BaselineReport:
    comparisons: Dict[str, FieldComparison]
    drift_fields: List[str]


class BaselineComparator:

    def compare(
        self,
        actual: Dict[str, Any],
        expected: Dict[str, Any]
    ) -> BaselineReport:

        comparisons = {}
        drift_fields = []

        for field, expected_value in expected.items():

            actual_value = actual.get(field)

            matches = actual_value == expected_value

            comparison = FieldComparison(
                field=field,
                expected=expected_value,
                actual=actual_value,
                matches=matches
            )

            comparisons[field] = comparison

            if not matches:
                drift_fields.append(field)

        return BaselineReport(
            comparisons=comparisons,
            drift_fields=drift_fields
        )