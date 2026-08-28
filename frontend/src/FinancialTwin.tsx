import {
  Activity,
  Calculator,
  LoaderCircle,
  RotateCcw,
  ShieldCheck,
  TrendingDown,
  X,
} from "lucide-react";
import {
  useState,
} from "react";

import {
  runFinancialScenario,
  ScenarioResponse,
} from "./api";


type FinancialTwinProps = {
  onClose: () => void;
};


function formatMoney(
  value: number | null,
): string {
  if (value === null) {
    return "—";
  }

  const absolute = Math.abs(value);
  const sign = value < 0 ? "-" : "";

  if (absolute >= 1_000_000_000) {
    return `${sign}$${(
      absolute / 1_000_000_000
    ).toFixed(2)}B`;
  }

  if (absolute >= 1_000_000) {
    return `${sign}$${(
      absolute / 1_000_000
    ).toFixed(1)}M`;
  }

  if (absolute >= 1_000) {
    return `${sign}$${(
      absolute / 1_000
    ).toFixed(1)}K`;
  }

  return `${sign}$${absolute.toFixed(0)}`;
}


function formatPercent(
  value: number | null,
): string {
  if (value === null) {
    return "—";
  }

  return `${(value * 100).toFixed(2)}%`;
}


function formatRatio(
  value: number | null,
): string {
  if (value === null) {
    return "—";
  }

  return `${value.toFixed(2)}x`;
}


function formatDeltaPercent(
  value: number | null,
): string {
  if (value === null) {
    return "—";
  }

  const percentagePoints = value * 100;
  const sign = percentagePoints > 0 ? "+" : "";

  return `${sign}${percentagePoints.toFixed(2)} pp`;
}


function formatDeltaRatio(
  value: number | null,
): string {
  if (value === null) {
    return "—";
  }

  const sign = value > 0 ? "+" : "";

  return `${sign}${value.toFixed(2)}x`;
}


export default function FinancialTwin({
  onClose,
}: FinancialTwinProps) {
  const [
    capexChange,
    setCapexChange,
  ] = useState(10);

  const [
    revenueChange,
    setRevenueChange,
  ] = useState(0);

  const [
    opexChange,
    setOpexChange,
  ] = useState(0);

  const [
    interestRateChange,
    setInterestRateChange,
  ] = useState(0);

  const [
    result,
    setResult,
  ] = useState<ScenarioResponse | null>(
    null,
  );

  const [
    loading,
    setLoading,
  ] = useState(false);

  const [
    error,
    setError,
  ] = useState<string | null>(
    null,
  );


  async function runScenario() {
    setLoading(true);
    setError(null);

    try {
      const response =
        await runFinancialScenario({
          name: "Executive downside scenario",
          capex_change_pct:
            capexChange / 100,
          revenue_change_pct:
            revenueChange / 100,
          opex_change_pct:
            opexChange / 100,
          interest_rate_change_pct:
            interestRateChange / 100,
        });

      setResult(response);
    } catch (scenarioError) {
      setError(
        scenarioError instanceof Error
          ? scenarioError.message
          : "Unable to run scenario.",
      );
    } finally {
      setLoading(false);
    }
  }


  function resetScenario() {
    setCapexChange(10);
    setRevenueChange(0);
    setOpexChange(0);
    setInterestRateChange(0);
    setResult(null);
    setError(null);
  }


  return (
    <div className="financial-twin-overlay">
      <section className="financial-twin-panel">
        <header className="financial-twin-header">
          <div>
            <div className="eyebrow">
              DETERMINISTIC ENGINE
            </div>

            <h2>
              PPP Financial Twin
            </h2>

            <p>
              Change project assumptions and
              recalculate the economics before
              the decision is made.
            </p>
          </div>

          <button
            className="icon-button"
            onClick={onClose}
            aria-label="Close Financial Twin"
          >
            <X size={18} />
          </button>
        </header>


        <div className="financial-twin-body">
          <section className="scenario-controls">
            <div className="section-heading">
              <Calculator size={17} />

              <span>
                Scenario assumptions
              </span>
            </div>


            <label className="scenario-field">
              <div className="scenario-label">
                <span>
                  CAPEX change
                </span>

                <strong>
                  {capexChange > 0 ? "+" : ""}
                  {capexChange}%
                </strong>
              </div>

              <input
                type="range"
                min="-20"
                max="50"
                step="1"
                value={capexChange}
                onChange={(event) =>
                  setCapexChange(
                    Number(event.target.value),
                  )
                }
              />
            </label>


            <label className="scenario-field">
              <div className="scenario-label">
                <span>
                  Revenue change
                </span>

                <strong>
                  {revenueChange > 0 ? "+" : ""}
                  {revenueChange}%
                </strong>
              </div>

              <input
                type="range"
                min="-30"
                max="30"
                step="1"
                value={revenueChange}
                onChange={(event) =>
                  setRevenueChange(
                    Number(event.target.value),
                  )
                }
              />
            </label>


            <label className="scenario-field">
              <div className="scenario-label">
                <span>
                  OPEX change
                </span>

                <strong>
                  {opexChange > 0 ? "+" : ""}
                  {opexChange}%
                </strong>
              </div>

              <input
                type="range"
                min="-20"
                max="50"
                step="1"
                value={opexChange}
                onChange={(event) =>
                  setOpexChange(
                    Number(event.target.value),
                  )
                }
              />
            </label>


            <label className="scenario-field">
              <div className="scenario-label">
                <span>
                  Interest rate change
                </span>

                <strong>
                  {interestRateChange > 0
                    ? "+"
                    : ""}
                  {interestRateChange.toFixed(1)}
                  {" pp"}
                </strong>
              </div>

              <input
                type="range"
                min="-2"
                max="5"
                step="0.25"
                value={interestRateChange}
                onChange={(event) =>
                  setInterestRateChange(
                    Number(event.target.value),
                  )
                }
              />
            </label>


            <div className="scenario-actions">
              <button
                className="primary-action"
                onClick={runScenario}
                disabled={loading}
              >
                {loading ? (
                  <LoaderCircle
                    size={16}
                    className="spin"
                  />
                ) : (
                  <Activity size={16} />
                )}

                {loading
                  ? "Recalculating..."
                  : "Run Financial Twin"}
              </button>

              <button
                className="secondary-action"
                onClick={resetScenario}
              >
                <RotateCcw size={15} />
                Reset
              </button>
            </div>


            <div className="scenario-governance">
              <ShieldCheck size={16} />

              <p>
                Financial calculations are
                deterministic. AI does not
                calculate IRR, NPV or DSCR.
              </p>
            </div>
          </section>


          <section className="scenario-results">
            {!result && !loading && (
              <div className="scenario-empty">
                <Calculator size={28} />

                <h3>
                  Model the decision
                </h3>

                <p>
                  Adjust the project assumptions,
                  then run the Financial Twin to
                  compare the modeled case against
                  the base project economics.
                </p>

                <div className="scenario-example">
                  TRY THIS
                  <strong>
                    CAPEX +15% · Revenue -5%
                  </strong>
                </div>
              </div>
            )}


            {loading && (
              <div className="scenario-empty">
                <LoaderCircle
                  size={30}
                  className="spin"
                />

                <h3>
                  Recalculating project economics
                </h3>

                <p>
                  Running the scenario through
                  the deterministic PPP financial
                  engine.
                </p>
              </div>
            )}


            {error && (
              <div className="scenario-error">
                {error}
              </div>
            )}


            {result && !loading && (
              <>
                <div className="section-heading">
                  <TrendingDown size={17} />

                  <span>
                    Modeled impact
                  </span>
                </div>


                <div className="twin-comparison">
                  <div className="comparison-header">
                    <span>
                      METRIC
                    </span>

                    <span>
                      BASE
                    </span>

                    <span>
                      SCENARIO
                    </span>

                    <span>
                      CHANGE
                    </span>
                  </div>


                  <div className="comparison-row">
                    <strong>
                      Equity IRR
                    </strong>

                    <span>
                      {formatPercent(
                        result.base.equity_irr,
                      )}
                    </span>

                    <span>
                      {formatPercent(
                        result.scenario.equity_irr,
                      )}
                    </span>

                    <span className="scenario-delta">
                      {formatDeltaPercent(
                        result.equity_irr_change,
                      )}
                    </span>
                  </div>


                  <div className="comparison-row">
                    <strong>
                      Project NPV
                    </strong>

                    <span>
                      {formatMoney(
                        result.base.project_npv_usd,
                      )}
                    </span>

                    <span>
                      {formatMoney(
                        result.scenario.project_npv_usd,
                      )}
                    </span>

                    <span className="scenario-delta">
                      {formatMoney(
                        result.project_npv_change_usd,
                      )}
                    </span>
                  </div>


                  <div className="comparison-row">
                    <strong>
                      Minimum DSCR
                    </strong>

                    <span>
                      {formatRatio(
                        result.base.minimum_dscr,
                      )}
                    </span>

                    <span>
                      {formatRatio(
                        result.scenario.minimum_dscr,
                      )}
                    </span>

                    <span className="scenario-delta">
                      {formatDeltaRatio(
                        result.minimum_dscr_change,
                      )}
                    </span>
                  </div>
                </div>


                <div className="scenario-engine-note">
                  <div>
                    CALCULATION ENGINE
                  </div>

                  <strong>
                    {result.calculation_engine}
                  </strong>

                  <p>
                    {result.data_notice}
                  </p>
                </div>


                {result.human_decision_required && (
                  <div className="human-gate">
                    <ShieldCheck size={17} />

                    <div>
                      <strong>
                        HUMAN APPROVAL GATE
                      </strong>

                      <p>
                        Model output informs the
                        decision. It does not
                        authorize the project
                        decision.
                      </p>
                    </div>
                  </div>
                )}
              </>
            )}
          </section>
        </div>
      </section>
    </div>
  );
}
