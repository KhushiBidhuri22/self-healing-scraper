import json

from app.repair_logger import log_repair


def test_log_repair(tmp_path, monkeypatch):
    log_directory = tmp_path / "logs"
    log_file = log_directory / "repairs.jsonl"

    monkeypatch.setattr(
        "app.repair_logger.LOG_DIRECTORY",
        log_directory,
    )

    monkeypatch.setattr(
        "app.repair_logger.LOG_FILE",
        log_file,
    )

    result = log_repair(
        field="name",
        old_selector=".product-name",
        new_selector="h2.title",
        score=100,
        evidence=["matched expected value"],
        new_version=2,
    )

    assert result["field"] == "name"
    assert result["old_selector"] == ".product-name"
    assert result["new_selector"] == "h2.title"
    assert result["score"] == 100
    assert result["new_version"] == 2

    assert log_file.exists()

    with log_file.open(encoding="utf-8") as file:
        saved = json.loads(file.readline())

    assert saved["new_selector"] == "h2.title"