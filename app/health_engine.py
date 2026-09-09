from dataclasses import dataclass
from typing import Dict, List, Any

from app.validator import invalid_name, invalid_price


@dataclass
class FieldHealth:
    field: str
    total: int
    valid: int
    missing: int
    health_score: float


@dataclass
class HealthReport:
    overall_score: float
    status: str
    fields: Dict[str, FieldHealth]
    drift_fields: List[str]


class HealthEngine:

    def __init__(self, threshold: float = 90.0):
        self.threshold = threshold

    def evaluate(
        self,
        records: List[Dict[str, Any]],
        required_fields: List[str]
    ) -> HealthReport:

        field_results = {}
        drift_fields = []

        for field in required_fields:

            total = len(records)

            valid = sum(
                1
                for record in records
                if self._is_valid_field(
                    field,
                    record.get(field)
                )
            )

            missing = total - valid

            health_score = (
                (valid / total) * 100
                if total > 0
                else 0
            )

            result = FieldHealth(
                field=field,
                total=total,
                valid=valid,
                missing=missing,
                health_score=round(health_score, 2)
            )

            field_results[field] = result

            if health_score < self.threshold:
                drift_fields.append(field)

        if field_results:
            overall_score = sum(
                field.health_score
                for field in field_results.values()
            ) / len(field_results)
        else:
            overall_score = 0

        if overall_score >= self.threshold:
            status = "healthy"
        elif overall_score >= 50:
            status = "degraded"
        else:
            status = "critical"

        return HealthReport(
            overall_score=round(overall_score, 2),
            status=status,
            fields=field_results,
            drift_fields=drift_fields
        )

    @staticmethod
    def _is_valid_field(field: str, value: Any) -> bool:

        if field == "name":
            return not invalid_name(value)

        if field == "price":
            return not invalid_price(value)

        if field == "rating":
            return HealthEngine._valid_rating(value)

        if field == "review_count":
            return HealthEngine._valid_review_count(value)

        if value is None:
            return False

        if isinstance(value, str) and not value.strip():
            return False

        return True

    @staticmethod
    def _valid_rating(value: Any) -> bool:

        try:
            rating = float(value)
            return 0 <= rating <= 5
        except (TypeError, ValueError):
            return False

    @staticmethod
    def _valid_review_count(value: Any) -> bool:

        if isinstance(value, int):
            return value >= 0

        if not isinstance(value, str):
            return False

        cleaned = value.replace(",", "").strip()

        try:
            return int(cleaned) >= 0
        except ValueError:
            return False