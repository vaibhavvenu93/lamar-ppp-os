import {
  AlertTriangle,
  ArrowLeft,
  Bot,
  CalendarDays,
  CheckCircle2,
  ChevronRight,
  CircleDollarSign,
  FileSearch,
  FileText,
  LoaderCircle,
  MessageSquareWarning,
  Network,
  ShieldCheck,
  Sparkles,
  Target,
  X,
} from "lucide-react";
import {
  useEffect,
  useMemo,
  useState,
} from "react";

import {
  DocumentEvidence,
  DocumentIntelligenceResponse,
  investigateOpportunity,
} from "./api";


type DocumentIntelligenceProps = {
  opportunityId: string;
  opportunityName: string;
  onClose: () => void;
  onBack: () => void;
};


type IntelligenceTab =
  | "requirements"
  | "obligations"
  | "risks"
  | "dates"
  | "clarifications";


type EvidenceSelection = {
  evidenceIds: string[];
  title: string;
};


function formatMoney(
  value: number | null,
): string {
  if (value === null) {
    return "—";
  }

  if (Math.abs(value) >= 1_000_000_000) {
    return `$${(value / 1_000_000_000).toFixed(1)}B`;
  }

  if (Math.abs(value) >= 1_000_000) {
    return `$${(value / 1_000_000).toFixed(1)}M`;
  }

  if (Math.abs(value) >= 1_000) {
    return `$${(value / 1_000).toFixed(1)}K`;
  }

  return `$${value.toFixed(0)}`;
}


function formatDate(
  value: string | null,
): string {
  if (!value) {
    return "—";
  }

  return new Intl.DateTimeFormat(
    "en",
    {
      day: "2-digit",
      month: "short",
      year: "numeric",
    },
  ).format(new Date(`${value}T00:00:00`));
}


function confidenceLabel(
  confidence: number,
): string {
  return `${Math.round(confidence * 100)}%`;
}


function EvidencePanel({
  selection,
  evidence,
  onClose,
}: {
  selection: EvidenceSelection;
  evidence: DocumentEvidence[];
  onClose: () => void;
}) {
  const selectedEvidence = evidence.filter(
    (item) => selection.evidenceIds.includes(
      item.evidence_id
    ),
  );

  return (
    <aside className="doc-evidence-panel">
      <div className="doc-evidence-header">
        <div>
          <span className="doc-eyebrow">
            SOURCE TRACE
          </span>

          <h3>{selection.title}</h3>
        </div>

        <button
          className="doc-icon-button"
          onClick={onClose}
          aria-label="Close evidence"
        >
          <X size={17} />
        </button>
      </div>

      <div className="doc-evidence-body">
        {selectedEvidence.map((item) => (
          <article
            className="doc-evidence-card"
            key={item.evidence_id}
          >
            <div className="doc-evidence-card-top">
              <FileText size={16} />

              <span>
                {item.document_name}
              </span>

              <strong>
                {confidenceLabel(item.confidence)}
              </strong>
            </div>

            <div className="doc-evidence-meta">
              <span>
                Page {item.page_number ?? "—"}
              </span>

              <span>
                Clause {item.clause_reference ?? "—"}
              </span>

              <span>
                {item.section_title ?? "Source section"}
              </span>
            </div>

            <blockquote>
              {item.source_text ?? (
                "Source text unavailable."
              )}
            </blockquote>

            <div className="doc-evidence-id">
              {item.evidence_id}
            </div>
          </article>
        ))}
      </div>

      <div className="doc-evidence-governance">
        <ShieldCheck size={16} />

        <p>
          Evidence supports the extraction. It does not
          constitute legal, technical or investment approval.
        </p>
      </div>
    </aside>
  );
}


function AgentTrace({
  data,
}: {
  data: DocumentIntelligenceResponse;
}) {
  const run = data.agent_run;

  return (
    <section className="doc-agent-trace">
      <div className="doc-section-title">
        <div>
          <span className="doc-section-number">
            05
          </span>

          <div>
            <span className="doc-eyebrow">
              AGENT EXECUTION
            </span>

            <h2>
              Inspect what the agent actually did
            </h2>
          </div>
        </div>

        <span className="doc-review-badge">
          HUMAN REVIEW REQUIRED
        </span>
      </div>

      <div className="doc-agent-run">
        <div className="doc-agent-identity">
          <div className="doc-agent-icon">
            <Bot size={22} />
          </div>

          <div>
            <strong>{run.agent_name}</strong>
            <span>{run.run_id}</span>
          </div>

          <div className="doc-agent-status">
            <CheckCircle2 size={15} />
            {run.status.replaceAll("_", " ")}
          </div>
        </div>

        <p className="doc-agent-task">
          {run.task}
        </p>

        <div className="doc-agent-flow">
          <div className="doc-agent-node">
            <span>INPUT</span>
            <strong>
              {run.input_record_ids.length}
            </strong>
            <small>document records</small>
          </div>

          <ChevronRight size={17} />

          <div className="doc-agent-node">
            <span>TOOLS</span>
            <strong>
              {run.tools_used.length}
            </strong>
            <small>extraction tools</small>
          </div>

          <ChevronRight size={17} />

          <div className="doc-agent-node">
            <span>EVIDENCE</span>
            <strong>
              {run.evidence_ids.length}
            </strong>
            <small>source traces</small>
          </div>

          <ChevronRight size={17} />

          <div className="doc-agent-node">
            <span>OUTPUT</span>
            <strong>
              {run.output_record_ids.length}
            </strong>
            <small>Project Brain record</small>
          </div>

          <ChevronRight size={17} />

          <div className="doc-agent-node doc-agent-human">
            <span>DECISION</span>
            <strong>HUMAN</strong>
            <small>approval boundary</small>
          </div>
        </div>

        <div className="doc-tools">
          {run.tools_used.map((tool) => (
            <span key={tool}>
              {tool.replaceAll("_", " ")}
            </span>
          ))}
        </div>

        {run.summary && (
          <div className="doc-agent-summary">
            <Sparkles size={16} />
            <p>{run.summary}</p>
          </div>
        )}
      </div>
    </section>
  );
}


export default function DocumentIntelligence({
  opportunityId,
  opportunityName,
  onClose,
  onBack,
}: DocumentIntelligenceProps) {
  const [
    data,
    setData,
  ] = useState<DocumentIntelligenceResponse | null>(
    null
  );

  const [
    loading,
    setLoading,
  ] = useState(true);

  const [
    error,
    setError,
  ] = useState<string | null>(null);

  const [
    activeTab,
    setActiveTab,
  ] = useState<IntelligenceTab>(
    "requirements"
  );

  const [
    evidenceSelection,
    setEvidenceSelection,
  ] = useState<EvidenceSelection | null>(
    null
  );

  useEffect(() => {
    let cancelled = false;

    async function runInvestigation() {
      setLoading(true);
      setError(null);

      try {
        const result = await investigateOpportunity(
          opportunityId
        );

        if (!cancelled) {
          setData(result);
        }
      } catch (requestError) {
        if (!cancelled) {
          setError(
            requestError instanceof Error
              ? requestError.message
              : "Document investigation failed."
          );
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    runInvestigation();

    return () => {
      cancelled = true;
    };
  }, [opportunityId]);

  const tabs = useMemo(
    () => [
      {
        id: "requirements" as const,
        label: "Requirements",
        count: data?.requirements.length ?? 0,
      },
      {
        id: "obligations" as const,
        label: "Obligations",
        count: data?.obligations.length ?? 0,
      },
      {
        id: "risks" as const,
        label: "Risks",
        count: data?.risks.length ?? 0,
      },
      {
        id: "dates" as const,
        label: "Critical Dates",
        count: data?.project_dates.length ?? 0,
      },
      {
        id: "clarifications" as const,
        label: "Clarifications",
        count: data?.clarifications.length ?? 0,
      },
    ],
    [data],
  );

  function openEvidence(
    evidenceIds: string[],
    title: string,
  ) {
    setEvidenceSelection({
      evidenceIds,
      title,
    });
  }

  if (loading) {
    return (
      <div className="doc-overlay">
        <div className="doc-loading">
          <LoaderCircle
            size={28}
            className="doc-spin"
          />

          <span className="doc-eyebrow">
            DOCUMENT AGENT RUNNING
          </span>

          <h2>
            Investigating tender package
          </h2>

          <p>
            Reading procurement documents, tracing clauses
            and structuring decision-relevant intelligence.
          </p>
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="doc-overlay">
        <div className="doc-error">
          <AlertTriangle size={26} />

          <span className="doc-eyebrow">
            INVESTIGATION FAILED
          </span>

          <h2>
            Document Agent could not complete the run
          </h2>

          <p>
            {error ?? "No intelligence response returned."}
          </p>

          <button
            className="doc-primary-button"
            onClick={onBack}
          >
            <ArrowLeft size={16} />
            Return to Opportunity Radar
          </button>
        </div>
      </div>
    );
  }

  const summary = data.summary;

  return (
    <div className="doc-overlay">
      <div className="doc-shell">
        <header className="doc-header">
          <div className="doc-header-left">
            <button
              className="doc-icon-button doc-back"
              onClick={onBack}
              aria-label="Back to Opportunity Radar"
            >
              <ArrowLeft size={18} />
            </button>

            <div className="doc-header-mark">
              <FileSearch size={20} />
            </div>

            <div>
              <span className="doc-eyebrow">
                DOCUMENT INTELLIGENCE
              </span>

              <h1>
                Tender Package Investigation
              </h1>
            </div>
          </div>

          <div className="doc-header-right">
            <div className="doc-project-context">
              <span>{summary.project_id}</span>
              <strong>{opportunityName}</strong>
            </div>

            <button
              className="doc-icon-button"
              onClick={onClose}
              aria-label="Close Document Intelligence"
            >
              <X size={18} />
            </button>
          </div>
        </header>

        <div className="doc-demo-banner">
          {data.data_notice}
        </div>

        <main className="doc-workspace">
          <section className="doc-hero">
            <div className="doc-hero-copy">
              <span className="doc-eyebrow">
                AGENT RUN COMPLETE
              </span>

              <h2>
                486 pages became a decision surface.
              </h2>

              <p>
                {summary.executive_summary}
              </p>

              <div className="doc-hero-tags">
                <span>
                  <CheckCircle2 size={14} />
                  {summary.status.replaceAll("_", " ")}
                </span>

                <span>
                  <Network size={14} />
                  Project Brain updated
                </span>

                <span>
                  <ShieldCheck size={14} />
                  Human review preserved
                </span>
              </div>
            </div>

            <div className="doc-hero-metrics">
              <div>
                <span>DOCUMENTS</span>
                <strong>
                  {summary.document_count}
                </strong>
              </div>

              <div>
                <span>EVIDENCE</span>
                <strong>
                  {summary.evidence_count}
                </strong>
              </div>

              <div>
                <span>PENDING REVIEW</span>
                <strong>
                  {summary.pending_review_count}
                </strong>
              </div>
            </div>
          </section>

          <section className="doc-summary-strip">
            <div>
              <Target size={17} />
              <span>Requirements</span>
              <strong>
                {summary.requirement_count}
              </strong>
            </div>

            <div>
              <FileText size={17} />
              <span>Obligations</span>
              <strong>
                {summary.obligation_count}
              </strong>
            </div>

            <div>
              <AlertTriangle size={17} />
              <span>Risks</span>
              <strong>
                {summary.risk_count}
              </strong>
            </div>

            <div>
              <CalendarDays size={17} />
              <span>Critical Dates</span>
              <strong>
                {data.project_dates.length}
              </strong>
            </div>

            <div>
              <MessageSquareWarning size={17} />
              <span>Clarifications</span>
              <strong>
                {summary.clarification_count}
              </strong>
            </div>
          </section>

          <section className="doc-intelligence-section">
            <div className="doc-section-title">
              <div>
                <span className="doc-section-number">
                  01
                </span>

                <div>
                  <span className="doc-eyebrow">
                    STRUCTURED EXTRACTION
                  </span>

                  <h2>
                    What the tender actually requires
                  </h2>
                </div>
              </div>

              <p>
                Every material item can be traced back to
                source evidence.
              </p>
            </div>

            <div className="doc-tabs">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  className={
                    activeTab === tab.id
                      ? "doc-tab doc-tab-active"
                      : "doc-tab"
                  }
                  onClick={() => setActiveTab(tab.id)}
                >
                  {tab.label}
                  <span>{tab.count}</span>
                </button>
              ))}
            </div>

            <div className="doc-items">
              {activeTab === "requirements" && (
                data.requirements.map((item) => (
                  <article
                    className="doc-intel-card"
                    key={item.requirement_id}
                  >
                    <div className="doc-intel-index">
                      {item.requirement_id}
                    </div>

                    <div className="doc-intel-content">
                      <div className="doc-intel-top">
                        <div>
                          <span className="doc-category">
                            {item.category}
                          </span>

                          <h3>{item.title}</h3>
                        </div>

                        <span className="doc-confidence">
                          {confidenceLabel(item.confidence)}
                          {" "}confidence
                        </span>
                      </div>

                      <p>{item.description}</p>

                      <div className="doc-intel-meta">
                        <span>
                          {item.mandatory
                            ? "MANDATORY"
                            : "OPTIONAL"}
                        </span>

                        {item.due_date && (
                          <span>
                            DUE {formatDate(item.due_date)}
                          </span>
                        )}

                        <span>
                          {item.review_status.replaceAll(
                            "_",
                            " "
                          )}
                        </span>
                      </div>
                    </div>

                    <button
                      className="doc-evidence-button"
                      onClick={() => openEvidence(
                        item.evidence_ids,
                        item.title,
                      )}
                    >
                      Evidence
                      <ChevronRight size={15} />
                    </button>
                  </article>
                ))
              )}

              {activeTab === "obligations" && (
                data.obligations.map((item) => (
                  <article
                    className="doc-intel-card"
                    key={item.obligation_id}
                  >
                    <div className="doc-intel-index">
                      {item.obligation_id}
                    </div>

                    <div className="doc-intel-content">
                      <div className="doc-intel-top">
                        <div>
                          <span className="doc-category">
                            {item.category}
                          </span>

                          <h3>{item.title}</h3>
                        </div>

                        <span className="doc-confidence">
                          {confidenceLabel(item.confidence)}
                          {" "}confidence
                        </span>
                      </div>

                      <p>{item.description}</p>

                      <div className="doc-intel-meta">
                        {item.obligated_party && (
                          <span>
                            OBLIGOR {item.obligated_party}
                          </span>
                        )}

                        {item.financial_consequence_usd !== null && (
                          <span>
                            EXPOSURE{" "}
                            {formatMoney(
                              item.financial_consequence_usd
                            )}
                          </span>
                        )}

                        <span>
                          {item.review_status.replaceAll(
                            "_",
                            " "
                          )}
                        </span>
                      </div>

                      {item.consequence_description && (
                        <div className="doc-consequence">
                          {item.consequence_description}
                        </div>
                      )}
                    </div>

                    <button
                      className="doc-evidence-button"
                      onClick={() => openEvidence(
                        item.evidence_ids,
                        item.title,
                      )}
                    >
                      Evidence
                      <ChevronRight size={15} />
                    </button>
                  </article>
                ))
              )}

              {activeTab === "risks" && (
                data.risks.map((item) => (
                  <article
                    className="doc-intel-card doc-risk-card"
                    key={item.risk_id}
                  >
                    <div className="doc-intel-index">
                      {item.risk_id}
                    </div>

                    <div className="doc-intel-content">
                      <div className="doc-intel-top">
                        <div>
                          <span className="doc-category">
                            {item.category}
                          </span>

                          <h3>{item.title}</h3>
                        </div>

                        {item.estimated_impact_usd !== null && (
                          <span className="doc-risk-exposure">
                            {formatMoney(
                              item.estimated_impact_usd
                            )}
                          </span>
                        )}
                      </div>

                      <p>{item.description}</p>

                      {item.potential_impact && (
                        <div className="doc-consequence">
                          <AlertTriangle size={14} />
                          {item.potential_impact}
                        </div>
                      )}

                      <div className="doc-intel-meta">
                        <span>
                          {confidenceLabel(item.confidence)}
                          {" "}CONFIDENCE
                        </span>

                        <span>
                          {item.review_status.replaceAll(
                            "_",
                            " "
                          )}
                        </span>
                      </div>
                    </div>

                    <button
                      className="doc-evidence-button"
                      onClick={() => openEvidence(
                        item.evidence_ids,
                        item.title,
                      )}
                    >
                      Trace risk
                      <ChevronRight size={15} />
                    </button>
                  </article>
                ))
              )}

              {activeTab === "dates" && (
                data.project_dates.map((item) => (
                  <article
                    className="doc-intel-card"
                    key={item.date_id}
                  >
                    <div className="doc-date-box">
                      <CalendarDays size={18} />
                      <strong>
                        {formatDate(item.event_date)}
                      </strong>
                    </div>

                    <div className="doc-intel-content">
                      <div className="doc-intel-top">
                        <div>
                          <span className="doc-category">
                            {item.critical
                              ? "CRITICAL DATE"
                              : "PROJECT DATE"}
                          </span>

                          <h3>{item.title}</h3>
                        </div>
                      </div>

                      <p>{item.description}</p>

                      <div className="doc-intel-meta">
                        <span>
                          {confidenceLabel(item.confidence)}
                          {" "}CONFIDENCE
                        </span>

                        <span>
                          {item.review_status.replaceAll(
                            "_",
                            " "
                          )}
                        </span>
                      </div>
                    </div>

                    <button
                      className="doc-evidence-button"
                      onClick={() => openEvidence(
                        item.evidence_ids,
                        item.title,
                      )}
                    >
                      Evidence
                      <ChevronRight size={15} />
                    </button>
                  </article>
                ))
              )}

              {activeTab === "clarifications" && (
                data.clarifications.map((item) => (
                  <article
                    className="doc-intel-card doc-clarification-card"
                    key={item.clarification_id}
                  >
                    <div className="doc-intel-index">
                      {item.clarification_id}
                    </div>

                    <div className="doc-intel-content">
                      <div className="doc-intel-top">
                        <div>
                          <span className="doc-category">
                            {item.priority} PRIORITY
                          </span>

                          <h3>{item.title}</h3>
                        </div>
                      </div>

                      <div className="doc-question">
                        “{item.question}”
                      </div>

                      <p>{item.rationale}</p>

                      <div className="doc-intel-meta">
                        <span>
                          HUMAN SUBMISSION REQUIRED
                        </span>

                        <span>
                          {item.review_status.replaceAll(
                            "_",
                            " "
                          )}
                        </span>
                      </div>
                    </div>

                    <button
                      className="doc-evidence-button"
                      onClick={() => openEvidence(
                        item.evidence_ids,
                        item.title,
                      )}
                    >
                      Why ask?
                      <ChevronRight size={15} />
                    </button>
                  </article>
                ))
              )}
            </div>
          </section>

          <section className="doc-risk-focus">
            <div className="doc-section-title">
              <div>
                <span className="doc-section-number">
                  02
                </span>

                <div>
                  <span className="doc-eyebrow">
                    COMMERCIAL ATTENTION
                  </span>

                  <h2>
                    What can change project economics?
                  </h2>
                </div>
              </div>
            </div>

            <div className="doc-risk-grid">
              {data.risks
                .filter(
                  (risk) => (
                    risk.estimated_impact_usd !== null
                    || risk.category === "REVENUE"
                    || risk.category === "OPERATIONS"
                  )
                )
                .slice(0, 4)
                .map((risk) => (
                  <button
                    key={risk.risk_id}
                    className="doc-risk-focus-card"
                    onClick={() => openEvidence(
                      risk.evidence_ids,
                      risk.title,
                    )}
                  >
                    <div>
                      <AlertTriangle size={17} />
                      <span>{risk.category}</span>
                    </div>

                    <h3>{risk.title}</h3>

                    <p>
                      {risk.potential_impact}
                    </p>

                    <strong>
                      {risk.estimated_impact_usd !== null
                        ? formatMoney(
                            risk.estimated_impact_usd
                          )
                        : "MODEL NEXT"}
                    </strong>
                  </button>
                ))}
            </div>
          </section>

          <section className="doc-decision-bridge">
            <div className="doc-section-title">
              <div>
                <span className="doc-section-number">
                  03
                </span>

                <div>
                  <span className="doc-eyebrow">
                    NEXT SYSTEM HANDOFF
                  </span>

                  <h2>
                    The Bid Agent should not read 486 pages.
                  </h2>
                </div>
              </div>
            </div>

            <div className="doc-handoff">
              <div className="doc-handoff-node">
                <FileSearch size={20} />
                <span>DOCUMENT AGENT</span>
                <strong>
                  Structures the tender
                </strong>
              </div>

              <ChevronRight size={20} />

              <div className="doc-handoff-node">
                <Network size={20} />
                <span>PROJECT BRAIN</span>
                <strong>
                  Stores evidence + state
                </strong>
              </div>

              <ChevronRight size={20} />

              <div className="doc-handoff-node doc-handoff-next">
                <Target size={20} />
                <span>BID AGENT</span>
                <strong>
                  Reasons over structured facts
                </strong>
              </div>

              <ChevronRight size={20} />

              <div className="doc-handoff-node doc-handoff-human">
                <ShieldCheck size={20} />
                <span>HUMAN</span>
                <strong>
                  Makes Bid / No-Bid decision
                </strong>
              </div>
            </div>

            <div className="doc-next-action">
              <div>
                <span className="doc-eyebrow">
                  READY FOR BID INTELLIGENCE
                </span>

                <h3>
                  {summary.requirement_count} requirements,
                  {" "}
                  {summary.risk_count} risks and
                  {" "}
                  {summary.clarification_count} clarifications
                  are now structured inputs.
                </h3>

                <p>
                  The next agent can evaluate pursuit readiness
                  without losing the source evidence behind each
                  conclusion.
                </p>
              </div>

              <button
                className="doc-primary-button"
                type="button"
                disabled
                title="Bid Agent will be connected in the next build step."
              >
                Run Bid Agent
                <ChevronRight size={16} />
              </button>
            </div>
          </section>

          <section className="doc-governance">
            <div className="doc-section-title">
              <div>
                <span className="doc-section-number">
                  04
                </span>

                <div>
                  <span className="doc-eyebrow">
                    GOVERNANCE
                  </span>

                  <h2>
                    AI interpretation is not approval.
                  </h2>
                </div>
              </div>
            </div>

            <div className="doc-governance-grid">
              <div>
                <Bot size={18} />
                <strong>Agent</strong>
                <p>
                  Finds, structures and connects
                  decision-relevant information.
                </p>
              </div>

              <div>
                <FileSearch size={18} />
                <strong>Evidence</strong>
                <p>
                  Preserves document, page, clause and
                  source text for inspection.
                </p>
              </div>

              <div>
                <CircleDollarSign size={18} />
                <strong>Engines</strong>
                <p>
                  Quantify approved assumptions and
                  modeled project consequences.
                </p>
              </div>

              <div>
                <ShieldCheck size={18} />
                <strong>Human</strong>
                <p>
                  Approves contractual, investment and
                  Bid / No-Bid decisions.
                </p>
              </div>
            </div>

            <p className="doc-governance-notice">
              {data.governance_notice}
            </p>
          </section>

          <AgentTrace data={data} />
        </main>

        <footer className="doc-footer">
          <span>
            LAMAR PPP OS · CONNECTED INTELLIGENCE
          </span>

          <span>
            SYNTHETIC DEMO · NO LAMAR INTERNAL DATA
          </span>
        </footer>

        {evidenceSelection && (
          <EvidencePanel
            selection={evidenceSelection}
            evidence={data.evidence}
            onClose={() => setEvidenceSelection(null)}
          />
        )}
      </div>
    </div>
  );
}
