from fastapi.testclient import TestClient

from lamar_os.api.app import app


client = TestClient(app)


def test_health_endpoint():
    """API should expose a healthy deployment status."""

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "healthy",
        "service": "lamar-ppp-os",
    }


def test_root_identifies_demo_environment():
    """Root endpoint should clearly identify the demo environment."""

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["product"] == "Lamar PPP OS"
    assert data["version"] == "0.1.0"
    assert data["environment"] == "DEMO"
    assert "synthetic" in data["data_policy"].lower()


def test_executive_brief_endpoint_returns_top_three():
    """Executive API should return the prioritized top three signals."""

    response = client.get("/api/executive-brief")

    assert response.status_code == 200

    data = response.json()
    brief = data["brief"]

    assert brief["title"] == "Lamar Executive Brief"
    assert brief["greeting"] == "Good morning, Hani."
    assert brief["total_signals_reviewed"] == 5
    assert len(brief["items"]) == 3


def test_top_executive_signal_contains_calculated_exposure():
    """
    The construction signal should preserve the calculated
    probability-weighted financial exposure.
    """

    response = client.get("/api/executive-brief")

    data = response.json()
    top_item = data["brief"]["items"][0]

    assert top_item["title"] == "Construction Cost Exposure"
    assert top_item["priority"] == "HIGH"
    assert top_item["financial_exposure_usd"] == 12_000_000
    assert top_item["requires_decision"] is True


def test_executive_signal_preserves_traceability():
    """Financial scenario translation should remain inspectable."""

    response = client.get("/api/executive-brief")

    data = response.json()
    top_item = data["brief"]["items"][0]

    assert top_item["traceability"] is not None
    assert "$30,000,000" in top_item["traceability"]
    assert "4.29%" in top_item["traceability"]


def test_api_exposes_governance_boundaries():
    """API should make calculation and decision boundaries explicit."""

    response = client.get("/api/executive-brief")

    data = response.json()
    governance = data["governance"]

    assert governance["calculation_policy"] == (
        "Deterministic engines calculate and rank."
    )

    assert governance["ai_policy"] == (
        "AI may interpret and explain."
    )

    assert governance["decision_policy"] == (
        "Consequential project decisions remain with humans."
    )


def test_executive_api_labels_synthetic_data():
    """Demo data must never be presented as Lamar internal data."""

    response = client.get("/api/executive-brief")

    data = response.json()

    assert data["environment"] == "DEMO"
    assert "synthetic" in data["data_notice"].lower()
