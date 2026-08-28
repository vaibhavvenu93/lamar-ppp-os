import {
  ArrowRight,
  CircleDollarSign,
  FileText,
  ShieldAlert,
  ShieldCheck,
  X,
} from "lucide-react";

import {
  ExecutiveBriefItem,
} from "./api";


type RiskAnalysisProps = {
  item: ExecutiveBriefItem;
  onClose: () => void;
  onRunScenario: () => void;
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
    ).toFixed(1)}B`;
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


export default function RiskAnalysis({
  item,
  onClose,
  onRunScenario,
}: RiskAnalysisProps) {
  return (
    <div className="risk-analysis-overlay">
      <section className="risk-analysis-panel">
        <header className="risk-analysis-header">
          <div>
            <div className="eyebrow">
              EXECUTIVE RISK ANALYSIS
            </div>

            <h2>
              {item.title}
            </h2>

            <p>
              Trace the signal from detected
              project risk to financial
              consequence and executive
              attention.
            </p>
          </div>

          <button
            className="icon-button"
            onClick={onClose}
            aria-label="Close risk analysis"
          >
            <X size={18} />
          </button>
        </header>


        <div className="risk-analysis-body">
          <section className="analysis-summary">
            <div className="analysis-tags">
              <span className="tag high">
                {item.priority}
              </span>

              <span className="tag">
                {item.type}
              </span>

              <span className="project-id">
                {item.project_id}
              </span>
            </div>

            <p className="analysis-description">
              {item.summary}
            </p>


            <div className="analysis-metrics">
              <div>
                <span>
                  EXPECTED EXPOSURE
                </span>

                <strong>
                  {formatMoney(
                    item.financial_exposure_usd,
                  )}
                </strong>
              </div>

              <div>
                <span>
                  ATTENTION SCORE
                </span>

                <strong>
                  {item.attention_score}/100
                </strong>
              </div>

              <div>
                <span>
                  DECISION REQUIRED
                </span>

                <strong>
                  {item.requires_decision
                    ? "YES"
                    : "NO"}
                </strong>
              </div>
            </div>
          </section>


          <section className="analysis-section">
            <div className="analysis-section-title">
              <ShieldAlert size={17} />

              <div>
                <span>01</span>
                <strong>
                  WHY EXECUTIVE ATTENTION
                </strong>
              </div>
            </div>

            <div className="analysis-content-card">
              <p>
                {item.ranking_reason}
              </p>

              <div className="analysis-rule">
                <span>
                  PRIORITY
                </span>

                <strong>
                  {item.priority}
                </strong>
              </div>

              <div className="analysis-rule">
                <span>
                  FINANCIAL EXPOSURE
                </span>

                <strong>
                  {formatMoney(
                    item.financial_exposure_usd,
                  )}
                </strong>
              </div>

              <div className="analysis-rule">
                <span>
                  HUMAN GATE
                </span>

                <strong>
                  {item.requires_decision
                    ? "Required"
                    : "Not required"}
                </strong>
              </div>
            </div>
          </section>


          <section className="analysis-section">
            <div className="analysis-section-title">
              <CircleDollarSign size={17} />

              <div>
                <span>02</span>
                <strong>
                  FINANCIAL TRANSLATION
                </strong>
              </div>
            </div>

            <div className="analysis-flow">
              <div className="analysis-node">
                <span>
                  PROJECT SIGNAL
                </span>

                <strong>
                  {item.title}
                </strong>
              </div>

              <ArrowRight size={16} />

              <div className="analysis-node">
                <span>
                  RISK ENGINE
                </span>

                <strong>
                  Exposure quantified
                </strong>
              </div>

              <ArrowRight size={16} />

              <div className="analysis-node">
                <span>
                  FINANCIAL TWIN
                </span>

                <strong>
                  Scenario modeled
                </strong>
              </div>

              <ArrowRight size={16} />

              <div className="analysis-node">
                <span>
                  EXECUTIVE ENGINE
                </span>

                <strong>
                  {item.attention_score}/100
                </strong>
              </div>
            </div>

            <div className="analysis-trace">
              <span>
                ENGINE TRACE
              </span>

              <p>
                {item.traceability ??
                  "Structured project risk translated into a deterministic financial scenario before executive prioritization."}
              </p>
            </div>
          </section>


          <section className="analysis-section">
            <div className="analysis-section-title">
              <ShieldCheck size={17} />

              <div>
                <span>03</span>
                <strong>
                  RECOMMENDED ACTION
                </strong>
              </div>
            </div>

            <div className="recommended-action-card">
              <p>
                {item.recommended_action ??
                  "Review the modeled exposure and mitigation before approving the next consequential project decision."}
              </p>

              <button
                className="primary-action"
                onClick={onRunScenario}
              >
                Run this scenario
                <ArrowRight size={15} />
              </button>
            </div>
          </section>


          <section className="analysis-section">
            <div className="analysis-section-title">
              <FileText size={17} />

              <div>
                <span>04</span>
                <strong>
                  EVIDENCE & DATA BOUNDARY
                </strong>
              </div>
            </div>

            <div className="evidence-card">
              <div>
                <span>
                  DEMONSTRATION RECORD
                </span>

                <strong>
                  Synthetic project data
                </strong>
              </div>

              <p>
                This prototype uses
                public-information-inspired
                context and synthetic project
                records. No Lamar internal
                information is used.
              </p>
            </div>
          </section>


          <footer className="analysis-footer">
            <ShieldCheck size={15} />

            <span>
              AI may interpret and explain.
              Deterministic engines calculate.
              Humans authorize consequential
              project decisions.
            </span>
          </footer>
        </div>
      </section>
    </div>
  );
}
