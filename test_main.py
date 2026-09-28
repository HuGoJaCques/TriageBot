import pytest
from pydantic import ValidationError

from main import TicketAnalysis, decide_escalation


def test_analyse_valide() -> None:
    analysis = TicketAnalysis.model_validate({
        "category": "bug",
        "severity": 3,
        "sentiment": "negative",
        "summary": "Le jeu plante.",
    })
    assert analysis.category == "bug"


@pytest.mark.parametrize("invalid_data", [
    {
        "category": "inconnue",
        "severity": 3,
        "sentiment": "negative",
        "summary": "Problème.",
    },
    {
        "category": "bug",
        "severity": 6,
        "sentiment": "negative",
        "summary": "Problème.",
    },
    {
        "category": "bug",
        "severity": 3,
        "sentiment": "negative",
    },
])
def test_analyse_invalide(invalid_data: dict) -> None:
    with pytest.raises(ValidationError):
        TicketAnalysis.model_validate(invalid_data)


@pytest.mark.parametrize(("status", "category", "severity", "expected"), [
    ("to_check", None, None, "relecture_humaine"),
    ("analyzed", "toxicity", 2, "moderation"),
    ("analyzed", "payment", 4, "responsable_support"),
    ("analyzed", "payment", 3, "traitement_standard"),
    ("analyzed", "bug", 5, "traitement_standard"),
])
def test_escalade(
    status: str,
    category: str | None,
    severity: int | None,
    expected: str,
) -> None:
    result = {
        "status": status,
        "analysis": (
            {"category": category, "severity": severity}
            if status == "analyzed" else None
        ),
    }
    assert decide_escalation(result) == expected