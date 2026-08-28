import {
  AlertTriangle,
  ArrowLeft,
  Bot,
  BrainCircuit,
  CheckCircle2,
  CircleDollarSign,
  FileSearch,
  Gauge,
  GitBranch,
  LockKeyhole,
  ShieldAlert,
  Sparkles,
  Target,
  UserCheck,
  Workflow,
  X,
} from "lucide-react";
import { useState } from "react";

import DealRoom from "./DealRoom";

import {
  getProjectBrain,
} from "./api";

import type {
  BidFactor,
  BidIntelligenceResponse,
  BidIssue,
  BidWorkstream,
  ProjectBrainResponse,
} from "./api";


type BidIntelligenceProps = {
  opportunityName: string;
  intelligence: BidIntelligenceResponse;
  onBack: () => void;
  onClose: () => void;
};


function formatMoney(
  value: number | null | undefined,
): string {
  if (value === null || value === undefined) {
    return "—";
  }

  if (Math.abs(value) >= 1_000_000_000) {
    return `$${(value / 1_000_000_000).toFixed(1)}B`;
  }

  if (Math.abs(value) >= 1_000_000) {
    return `$${(value / 1_000_000).toFixed(1)}M`;
  }

  if (Math.abs(value) >= 1_000) {
    return `$${(value / 1_000).toFixed(0)}K`;
  }

  return `$${value.toFixed(0)}`;
}


function humanize(
  value: string | null | undefined,
): string {
  if (!value) {
    return "—";
  }

  return value
    .replaceAll("_", " ")
    .toLowerCase()
    .replace(
      /\b\w/g,
      (character) => character.toUpperCase(),
    );
}


function scoreBand(score: number): string {
  if (score >= 85) {
    return "strong";
  }

  if (score >= 70) {
    return "conditional";
  }

  return "weak";
}


function severityClass(
  severity: string,
): string {
  const normalized = severity.toLowerCase();

  if (
    normalized === "critical"
    || normalized === "high"
  ) {
    return "high";
  }

  if (normalized === "medium") {
    return "medium";
  }

  return "low";
}


function FactorRow({
  factor,
}: {
  factor: BidFactor;
}) {
  const band = scoreBand(factor.score);

  return (
    <article className="bid-factor-row">
      <div className="bid-factor-heading">
        <div>
          <span className="bid-factor-name">
            {factor.name}
          </span>

          <span className="bid-factor-weight">
            {(factor.weight * 100).toFixed(0)}% weight
          </span>
        </div>

        <strong
          className={`bid-factor-score ${band}`}
        >
          {factor.score.toFixed(0)}
        </strong>
      </div>

      <div className="bid-score-track">
        <span
          className={`bid-score-fill ${band}`}
          style={{
            width: `${Math.max(
              0,
              Math.min(100, factor.score),
            )}%`,
          }}
        />
      </div>

      <p>{factor.rationale}</p>

      {factor.evidence_ids.length > 0 && (
        <div className="bid-evidence-links">
          {factor.evidence_ids.map(
            (evidenceId) => (
              <span key={evidenceId}>
                {evidenceId}
              </span>
            ),
          )}
        </div>
      )}
    </article>
  );
}


function IssueCard({
  issue,
}: {
  issue: BidIssue;
}) {
  const severity = severityClass(
    issue.severity,
  );

  return (
    <article
      className={`bid-issue-card ${severity}`}
    >
      <div className="bid-issue-topline">
        <div className="bid-issue-labels">
          <span
            className={`bid-severity ${severity}`}
          >
            {humanize(issue.severity)}
          </span>

          <span className="bid-issue-type">
            {humanize(issue.issue_type)}
          </span>

          {issue.blocking && (
            <span className="bid-blocker-badge">
              <LockKeyhole size={12} />
              Bid blocker
            </span>
          )}
        </div>

        {issue.estimated_exposure_usd !== null && (
          <strong className="bid-issue-exposure">
            {formatMoney(
              issue.estimated_exposure_usd,
            )}
          </strong>
        )}
      </div>

      <h4>{issue.title}</h4>

      <p>{issue.description}</p>

      {issue.resolution_required && (
        <div className="bid-recommended-action">
          <span>Resolution required</span>

          <strong>
            {issue.resolution_required}
          </strong>
        </div>
      )}

      {issue.owner && (
        <div className="bid-workstream-owner">
          Owner
          <strong>{issue.owner}</strong>
        </div>
      )}

      {issue.evidence_ids.length > 0 && (
        <div className="bid-evidence-links">
          {issue.evidence_ids.map(
            (evidenceId) => (
              <span key={evidenceId}>
                {evidenceId}
              </span>
            ),
          )}
        </div>
      )}
    </article>
  );
}


function WorkstreamCard({
  workstream,
  index,
}: {
  workstream: BidWorkstream;
  index: number;
}) {
  return (
    <article className="bid-workstream-card">
      <div className="bid-workstream-number">
        {String(index + 1).padStart(2, "0")}
      </div>

      <div className="bid-workstream-content">
        <div className="bid-workstream-heading">
          <div>
            <span>
              {humanize(workstream.priority)} priority
            </span>

            <h4>{workstream.name}</h4>
          </div>

          <Workflow size={19} />
        </div>

        <p>{workstream.objective}</p>

        <div className="bid-workstream-owner">
          Owner
          <strong>{workstream.owner}</strong>
        </div>

        {workstream.dependencies.length > 0 && (
          <div className="bid-dependency-row">
            <span>Depends on</span>

            {workstream.dependencies.map(
              (dependencyId) => (
                <strong key={dependencyId}>
                  {dependencyId}
                </strong>
              ),
            )}
          </div>
        )}

        {workstream.evidence_ids.length > 0 && (
          <div className="bid-evidence-links">
            {workstream.evidence_ids.map(
              (evidenceId) => (
                <span key={evidenceId}>
                  {evidenceId}
                </span>
              ),
            )}
          </div>
        )}
      </div>
    </article>
  );
}


export default function BidIntelligence({
  opportunityName,
  intelligence,
  onBack,
  onClose,
}: BidIntelligenceProps) {
  const [
    projectBrain,
    setProjectBrain,
  ] = useState<ProjectBrainResponse | null>(
    null,
  );

  const [
    projectBrainLoading,
    setProjectBrainLoading,
  ] = useState(false);

  const [
    projectBrainError,
    setProjectBrainError,
  ] = useState<string | null>(null);

  const recommendation = humanize(
    intelligence.recommendation,
  );

  const readiness = humanize(
    intelligence.readiness,
  );

  const readinessBand = scoreBand(
    intelligence.readiness_score,
  );

  async function openDealRoom() {
    setProjectBrainLoading(true);
    setProjectBrainError(null);

    try {
      const response = await getProjectBrain(
        intelligence.opportunity_id,
      );

      setProjectBrain(response);
    } catch (error) {
      setProjectBrainError(
        error instanceof Error
          ? error.message
          : "Unable to open the Project Brain.",
      );
    } finally {
      setProjectBrainLoading(false);
    }
  }

  if (projectBrain) {
    return (
      <DealRoom
        opportunityName={opportunityName}
        intelligence={projectBrain}
        onBack={() => setProjectBrain(null)}
        onClose={onClose}
      />
    );
  }

  return (
    <div className="bid-overlay">
      <div className="bid-shell">
        <header className="bid-topbar">
          <div className="bid-topbar-left">
            <button
              className="bid-icon-button"
              type="button"
              onClick={onBack}
              aria-label="Back to Document Intelligence"
            >
              <ArrowLeft size={18} />
            </button>

            <div>
              <div className="bid-product-mark">
                <span className="bid-product-symbol">
                  L
                </span>

                <span>Lamar PPP OS</span>

                <span className="bid-module-divider">
                  /
                </span>

                <strong>Bid Intelligence</strong>
              </div>

              <p>{opportunityName}</p>
            </div>
          </div>

          <div className="bid-topbar-right">
            <span className="bid-demo-pill">
              Demo environment
            </span>

            <button
              className="bid-icon-button"
              type="button"
              onClick={onClose}
              aria-label="Close Bid Intelligence"
            >
              <X size={18} />
            </button>
          </div>
        </header>

        <main className="bid-workspace">
          <section className="bid-hero">
            <div className="bid-hero-copy">
              <div className="bid-eyebrow">
                <Bot size={15} />
                BID AGENT · DETERMINISTIC DECISION SUPPORT
              </div>

              <h1>
                Pursue the opportunity.
                <span>
                  {" "}Resolve the blockers first.
                </span>
              </h1>

              <p className="bid-hero-summary">
                {intelligence.executive_thesis}
              </p>

              <div className="bid-agent-path">
                <div className="complete">
                  <FileSearch size={16} />

                  <span>
                    Document Agent
                    <small>
                      Evidence structured
                    </small>
                  </span>

                  <CheckCircle2 size={15} />
                </div>

                <GitBranch size={17} />

                <div className="active">
                  <Bot size={16} />

                  <span>
                    Bid Agent
                    <small>
                      Decision modeled
                    </small>
                  </span>

                  <CheckCircle2 size={15} />
                </div>

                <GitBranch size={17} />

                <div>
                  <UserCheck size={16} />

                  <span>
                    Human
                    <small>
                      Approval required
                    </small>
                  </span>

                  <LockKeyhole size={15} />
                </div>
              </div>

              <div className="bid-deal-room-entry">
                <button
                  type="button"
                  onClick={openDealRoom}
                  disabled={projectBrainLoading}
                >
                  <BrainCircuit size={17} />

                  {projectBrainLoading
                    ? "Opening Project Brain..."
                    : "Open Project Brain · Deal Room"}
                </button>

                <span>
                  Inspect the shared state behind this
                  recommendation
                </span>
              </div>

              {projectBrainError && (
                <div className="bid-deal-room-error">
                  <AlertTriangle size={15} />
                  {projectBrainError}
                </div>
              )}
            </div>

            <div className="bid-decision-card">
              <span className="bid-decision-label">
                Bid Agent recommendation
              </span>

              <div
                className={
                  `bid-readiness-ring ${readinessBand}`
                }
              >
                <strong>
                  {intelligence.readiness_score.toFixed(1)}
                </strong>

                <span>/ 100</span>
              </div>

              <div className="bid-recommendation">
                <Sparkles size={17} />

                <strong>
                  {recommendation}
                </strong>
              </div>

              <span className="bid-readiness-label">
                {readiness} readiness
              </span>

              <div className="bid-human-gate">
                <LockKeyhole size={15} />

                <span>
                  HUMAN DECISION GATE

                  <strong>
                    Agent cannot approve its own
                    recommendation
                  </strong>
                </span>
              </div>
            </div>
          </section>

          <section className="bid-metric-grid">
            <article>
              <div className="bid-metric-icon">
                <Gauge size={19} />
              </div>

              <span>Readiness</span>

              <strong>
                {intelligence.readiness_score.toFixed(1)}
              </strong>

              <small>
                Deterministic weighted score
              </small>
            </article>

            <article>
              <div className="bid-metric-icon">
                <ShieldAlert size={19} />
              </div>

              <span>Bid blockers</span>

              <strong>
                {intelligence.blocking_issue_count}
              </strong>

              <small>
                Must be resolved before approval
              </small>
            </article>

            <article>
              <div className="bid-metric-icon">
                <CircleDollarSign size={19} />
              </div>

              <span>Quantified exposure</span>

              <strong>
                {formatMoney(
                  intelligence.total_estimated_exposure_usd,
                )}
              </strong>

              <small>
                Known modeled issue exposure
              </small>
            </article>

            <article>
              <div className="bid-metric-icon">
                <Target size={19} />
              </div>

              <span>Required workstreams</span>

              <strong>
                {intelligence.workstreams.length}
              </strong>

              <small>
                Actions generated from decision gaps
              </small>
            </article>
          </section>

          <section className="bid-main-grid">
            <div className="bid-primary-column">
              <section className="bid-panel">
                <div className="bid-section-heading">
                  <div>
                    <span>DECISION LOGIC</span>

                    <h2>
                      Why the Bid Agent reached this
                      recommendation
                    </h2>
                  </div>

                  <span className="bid-inspectable-pill">
                    Inspectable scoring
                  </span>
                </div>

                <p className="bid-hero-summary">
                  {intelligence.decision_rationale}
                </p>

                <div className="bid-factor-list">
                  {intelligence.factors.map(
                    (factor) => (
                      <FactorRow
                        key={factor.factor_id}
                        factor={factor}
                      />
                    ),
                  )}
                </div>
              </section>

              <section className="bid-panel">
                <div className="bid-section-heading">
                  <div>
                    <span>ISSUE REGISTER</span>

                    <h2>
                      What prevents an unconditional bid
                    </h2>
                  </div>

                  <span className="bid-count-pill">
                    {intelligence.issues.length} issues
                  </span>
                </div>

                <div className="bid-issue-grid">
                  {intelligence.issues.map(
                    (issue) => (
                      <IssueCard
                        key={issue.issue_id}
                        issue={issue}
                      />
                    ),
                  )}
                </div>
              </section>

              <section className="bid-panel">
                <div className="bid-section-heading">
                  <div>
                    <span>ACTION PLAN</span>

                    <h2>
                      Workstreams required to reach
                      Bid-ready
                    </h2>
                  </div>

                  <span className="bid-count-pill">
                    {intelligence.workstreams.length}
                    {" "}workstreams
                  </span>
                </div>

                <div className="bid-workstream-list">
                  {intelligence.workstreams.map(
                    (workstream, index) => (
                      <WorkstreamCard
                        key={workstream.workstream_id}
                        workstream={workstream}
                        index={index}
                      />
                    ),
                  )}
                </div>
              </section>
            </div>

            <aside className="bid-side-column">
              <section className="bid-side-card">
                <div className="bid-side-heading">
                  <CheckCircle2 size={18} />

                  <div>
                    <span>WHY PURSUE</span>

                    <h3>
                      Strategic strengths
                    </h3>
                  </div>
                </div>

                <div className="bid-strength-list">
                  {intelligence.strengths.map(
                    (strength) => (
                      <article
                        key={strength.strength_id}
                      >
                        <CheckCircle2 size={15} />

                        <div>
                          <strong>
                            {strength.title}
                          </strong>

                          <p>
                            {strength.description}
                          </p>

                          {strength.evidence_ids.length > 0 && (
                            <div className="bid-evidence-links">
                              {strength.evidence_ids.map(
                                (evidenceId) => (
                                  <span
                                    key={evidenceId}
                                  >
                                    {evidenceId}
                                  </span>
                                ),
                              )}
                            </div>
                          )}
                        </div>
                      </article>
                    ),
                  )}
                </div>
              </section>

              <section className="bid-side-card">
                <div className="bid-side-heading">
                  <Bot size={18} />

                  <div>
                    <span>AGENT CHAIN</span>

                    <h3>
                      How this decision was produced
                    </h3>
                  </div>
                </div>

                <div className="bid-chain">
                  <div>
                    <span
                      className={
                        "bid-chain-status complete"
                      }
                    >
                      <CheckCircle2 size={13} />
                    </span>

                    <div>
                      <strong>
                        {
                          intelligence.agent_chain
                            .document_agent.agent_name
                        }
                      </strong>

                      <p>
                        {
                          intelligence.agent_chain
                            .document_agent.evidence_count
                        }{" "}
                        evidence records supplied
                      </p>
                    </div>
                  </div>

                  <span className="bid-chain-line" />

                  <div>
                    <span
                      className={
                        "bid-chain-status active"
                      }
                    >
                      <Bot size={13} />
                    </span>

                    <div>
                      <strong>
                        {
                          intelligence.agent_chain
                            .bid_agent.agent_name
                        }
                      </strong>

                      <p>
                        {
                          intelligence.agent_chain
                            .bid_agent.mode
                        }{" "}
                        decision engine
                      </p>
                    </div>
                  </div>

                  <span className="bid-chain-line" />

                  <div>
                    <span
                      className={
                        "bid-chain-status locked"
                      }
                    >
                      <LockKeyhole size={13} />
                    </span>

                    <div>
                      <strong>
                        Human Investment Gate
                      </strong>

                      <p>
                        Consequential Bid / No-Bid
                        approval
                      </p>
                    </div>
                  </div>
                </div>
              </section>

              <section
                className={
                  "bid-side-card bid-governance-card"
                }
              >
                <div className="bid-side-heading">
                  <ShieldAlert size={18} />

                  <div>
                    <span>GOVERNANCE</span>

                    <h3>
                      Agent authority boundary
                    </h3>
                  </div>
                </div>

                <p>
                  {
                    intelligence.governance
                      .recommendation_policy
                  }
                </p>

                <p>
                  {
                    intelligence.governance
                      .calculation_policy
                  }
                </p>

                {intelligence.governance
                  .state_policy && (
                  <p>
                    {
                      intelligence.governance
                        .state_policy
                    }
                  </p>
                )}

                <div className="bid-governance-lock">
                  <LockKeyhole size={16} />

                  <strong>
                    {
                      intelligence.governance
                        .approval_policy
                    }
                  </strong>
                </div>
              </section>

              <section
                className={
                  "bid-side-card bid-decision-gate"
                }
              >
                <span>EXECUTIVE DECISION</span>

                <h3>
                  Bid / No-Bid approval
                </h3>

                <p>
                  The system has completed its
                  recommendation. Approval remains
                  intentionally outside the agent's
                  authority.
                </p>

                <button
                  type="button"
                  disabled
                >
                  <LockKeyhole size={16} />
                  Awaiting human decision
                </button>

                <small>
                  No autonomous approval permitted
                </small>
              </section>
            </aside>
          </section>

          <footer className="bid-footer">
            <div>
              <AlertTriangle size={14} />

              <span>
                {intelligence.data_notice}
              </span>
            </div>

            <span>
              Project · {intelligence.project_id}
            </span>
          </footer>
        </main>
      </div>
    </div>
  );
}
