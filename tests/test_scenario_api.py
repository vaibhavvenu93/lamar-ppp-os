from fastapi.testclient import TestClient

from lamar_os.api.app import app


client = TestClient(app)


def test_scenario_endpoint_runs_capex_downside():
    """
    Financial Twin should run a deterministic CAPEX downside
    scenario through the API.
    """

    response = client.post(
        "/api/scenario",
        json={
            "name": "10% CAPEX overrun",
            "capex_change_pct": 0.10,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["scenario_name"] == "10% CAPEX overrun"
    assert data["scenario"]["equity_irr"] < data["base"]["equity_irr"]
    assert (
        data["scenario"]["project_npv_usd"]
        < data["base"]["project_npv_usd"]
    )


def test_scenario_endpoint_returns_financial_deltas():
    """Scenario API should expose calculated changes."""

    response = client.post(
        "/api/scenario",
        json={
            "capex_change_pct": 0.10,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["equity_irr_change"] < 0
    assert data["project_npv_change_usd"] < 0
    assert data["minimum_dscr_change"] is not None


def test_scenario_endpoint_preserves_base_case():
    """Running a scenario must not mutate the base assumptions."""

    first_response = client.post(
        "/api/scenario",
        json={
            "capex_change_pct": 0.10,
        },
    )

    second_response = client.post(
        "/api/scenario",
        json={
            "capex_change_pct": 0.20,
        },
    )

    first = first_response.json()
    second = second_response.json()

    assert first["base"] == second["base"]


def test_scenario_endpoint_rejects_extreme_capex_input():
    """Validated API contract should reject unsafe scenario ranges."""

    response = client.post(
        "/api/scenario",
        json={
            "capex_change_pct": 5.0,
        },
    )

    assert response.status_code == 422


def test_scenario_endpoint_labels_synthetic_data():
    """Financial Twin must disclose the demo-data boundary."""

    response = client.post(
        "/api/scenario",
        json={
            "capex_change_pct": 0.10,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "synthetic" in data["data_notice"].lower()
    assert data["human_decision_required"] is True
    assert (
        data["calculation_engine"]
        == "Lamar PPP OS deterministic Financial Twin"
    )
