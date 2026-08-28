import {
  ArrowLeft,
  Bot,
  BrainCircuit,
  CheckCircle2,
  ChevronRight,
  CircleDot,
  FileSearch,
  GitBranch,
  LockKeyhole,
  Network,
  ShieldCheck,
  Workflow,
  X,
} from "lucide-react";

import type {
  ProjectBrainAgentRun,
  ProjectBrainRecord,
  ProjectBrainResponse,
} from "./api";


type DealRoomProps = {
  opportunityName: string;
  intelligence: ProjectBrainResponse;
  onBack: () => void;
  onClose: () => void;
};


function humanize(value: string | null | undefined) {
  if (!value) {
    return "—";
  }

  return value
    .replaceAll("_", " ")
    .toLowerCase()
    .replace(/\b\w/g, (character) =>
      character.toUpperCase()
    );
}


function recordTypeLabel(value: string) {
  const labels: Record<string, string> = {
    OPPORTUNITY: "Opportunity",
    DOCUMENT: "Document",
    REQUIREMENT: "Requirement",
    OBLIGATION: "Obligation",
    RISK: "Risk",
    FINANCIAL_ASSUMPTION: "Financial Assumption",
    MILESTONE: "Milestone",
    DECISION: "Decision",
    CONSTRUCTION_SIGNAL: "Construction Signal",
    OPERATIONS_SIGNAL: "Operations Signal",
    MEMORY: "Memory",
    EVIDENCE: "Evidence",
  };

  return labels[value] ?? humanize(value);
}


function priorityClass(
  priority: string | null,
) {
  if (!priority) {
    return "neutral";
  }

  const normalized = priority.toUpperCase();

  if (
    normalized === "CRITICAL"
    || normalized === "HIGH"
  ) {
    return "high";
  }

  if (normalized === "MEDIUM") {
    return "medium";
  }

  return "neutral";
}


function agentIcon(agentName: string) {
  if (
    agentName.toLowerCase().includes("document")
  ) {
    return <FileSearch size={17} />;
  }

  if (
    agentName.toLowerCase().includes("bid")
  ) {
    return <Workflow size={17} />;
  }

  return <Bot size={17} />;
}


function recordIcon(recordType: string) {
  if (recordType === "REQUIREMENT") {
    return <CheckCircle2 size={15} />;
  }

  if (recordType === "OBLIGATION") {
    return <ShieldCheck size={15} />;
  }

  if (recordType === "RISK") {
    return <CircleDot size={15} />;
  }

  if (recordType === "DECISION") {
    return <LockKeyhole size={15} />;
  }

  return <GitBranch size={15} />;
}


function AgentCard({
  run,
}: {
  run: ProjectBrainAgentRun;
}) {
  return (
    <article className="deal-agent-card">
      <div className="deal-agent-icon">
        {agentIcon(run.agent_name)}
      </div>

      <div className="deal-agent-copy">
        <div className="deal-agent-heading">
          <strong>{run.agent_name}</strong>

          <span className="deal-status-pill complete">
            {humanize(run.status)}
          </span>
        </div>

        <p>{run.task}</p>

        <div className="deal-agent-stats">
          <span>
            {run.input_record_ids.length} inputs
          </span>

          <span>
            {run.output_record_ids.length} outputs
          </span>

          <span>
            {run.evidence_ids.length} evidence refs
          </span>
        </div>
      </div>
    </article>
  );
}


function RecordCard({
  record,
}: {
  record: ProjectBrainRecord;
}) {
  return (
    <article className="deal-record-card">
      <div className="deal-record-topline">
        <span className="deal-record-type">
          {recordIcon(record.record_type)}
          {recordTypeLabel(record.record_type)}
        </span>

        <span
          className={
            `deal-priority ${priorityClass(
              record.priority
            )}`
          }
        >
          {record.priority
            ? humanize(record.priority)
            : humanize(record.status)}
        </span>
      </div>

      <h4>{record.title}</h4>

      {record.summary && (
        <p>{record.summary}</p>
      )}

      <div className="deal-record-meta">
        <span>
          Source · {humanize(record.source)}
        </span>

        {record.owner && (
          <span>
            Owner · {record.owner}
          </span>
        )}
      </div>

      <div className="deal-record-links">
        <span>
          {record.evidence_ids.length} evidence
        </span>

        <span>
          {record.related_record_ids.length} links
        </span>

        <span>
          {humanize(record.approval_status)}
        </span>
      </div>
    </article>
  );
}


export default function DealRoom({
  opportunityName,
  intelligence,
  onBack,
  onClose,
}: DealRoomProps) {
  const {
    snapshot,
    records,
    agent_runs: agentRuns,
    relationships,
    pending_approval_ids: pendingApprovalIds,
  } = intelligence;

  const bidRecords = records.filter(
    (record) =>
      record.tags.includes("bid")
      || record.record_id.startsWith("BID-")
  );

  const documentRecords = records.filter(
    (record) =>
      !bidRecords.some(
        (bidRecord) =>
          bidRecord.record_id === record.record_id
      )
  );

  const visibleBidRecords = bidRecords.slice(0, 8);
  const visibleDocumentRecords =
    documentRecords.slice(0, 8);

  return (
    <div className="deal-overlay">
      <main className="deal-shell">
        <header className="deal-topbar">
          <div className="deal-topbar-left">
            <button
              className="deal-icon-button"
              type="button"
              onClick={onBack}
              aria-label="Back"
            >
              <ArrowLeft size={18} />
            </button>

            <div className="deal-brand-mark">
              L
            </div>

            <div>
              <strong>Lamar PPP OS</strong>
              <span>Project Brain · Deal Room</span>
            </div>
          </div>

          <div className="deal-topbar-right">
            <span className="deal-demo-pill">
              Demo Environment
            </span>

            <button
              className="deal-icon-button"
              type="button"
              onClick={onClose}
              aria-label="Close Deal Room"
            >
              <X size={18} />
            </button>
          </div>
        </header>

        <section className="deal-hero">
          <div>
            <span className="deal-eyebrow">
              Connected project intelligence
            </span>

            <h1>{opportunityName}</h1>

            <p>
              One shared state connecting evidence,
              agent reasoning, bid blockers,
              workstreams and human decisions.
            </p>
          </div>

          <div className="deal-brain-badge">
            <BrainCircuit size={22} />

            <div>
              <strong>Project Brain</strong>
              <span>
                {snapshot.record_count} live records
              </span>
            </div>
          </div>
        </section>

        <section className="deal-metrics">
          <article>
            <span>Shared Records</span>
            <strong>{snapshot.record_count}</strong>
            <small>
              Across document and bid intelligence
            </small>
          </article>

          <article>
            <span>Evidence Graph</span>
            <strong>{snapshot.evidence_count}</strong>
            <small>
              Traceable source references
            </small>
          </article>

          <article>
            <span>Agent Runs</span>
            <strong>{snapshot.agent_run_count}</strong>
            <small>
              Inspectable specialist executions
            </small>
          </article>

          <article>
            <span>Human Gates</span>
            <strong>
              {snapshot.pending_approval_count}
            </strong>
            <small>
              Decisions AI cannot authorize
            </small>
          </article>
        </section>

        <section className="deal-section">
          <div className="deal-section-heading">
            <div>
              <span className="deal-eyebrow">
                Agent workspace
              </span>

              <h2>
                Specialists working on one brain
              </h2>
            </div>

            <span className="deal-section-stat">
              {snapshot.agents.length} active agents
            </span>
          </div>

          <div className="deal-agent-flow">
            {agentRuns.map((run, index) => (
              <div
                className="deal-agent-flow-item"
                key={run.run_id}
              >
                <AgentCard run={run} />

                {index < agentRuns.length - 1 && (
                  <div className="deal-agent-connector">
                    <ChevronRight size={18} />
                  </div>
                )}
              </div>
            ))}

            <div className="deal-agent-flow-item">
              <article className="deal-agent-card human">
                <div className="deal-agent-icon">
                  <LockKeyhole size={17} />
                </div>

                <div className="deal-agent-copy">
                  <div className="deal-agent-heading">
                    <strong>Human Decision Gate</strong>

                    <span className="deal-status-pill locked">
                      Locked
                    </span>
                  </div>

                  <p>
                    Consequential pursuit decisions
                    require explicit human authorization.
                  </p>

                  <div className="deal-agent-stats">
                    <span>
                      {pendingApprovalIds.length}
                      {" "}pending approvals
                    </span>
                  </div>
                </div>
              </article>
            </div>
          </div>
        </section>

        <section className="deal-main-grid">
          <div className="deal-panel">
            <div className="deal-panel-heading">
              <div>
                <span className="deal-eyebrow">
                  Document intelligence
                </span>

                <h3>
                  What the tender says
                </h3>
              </div>

              <FileSearch size={20} />
            </div>

            <div className="deal-record-list">
              {visibleDocumentRecords.map(
                (record) => (
                  <RecordCard
                    key={record.record_id}
                    record={record}
                  />
                )
              )}
            </div>
          </div>

          <div className="deal-panel">
            <div className="deal-panel-heading">
              <div>
                <span className="deal-eyebrow">
                  Bid intelligence
                </span>

                <h3>
                  What Lamar should do
                </h3>
              </div>

              <Workflow size={20} />
            </div>

            <div className="deal-record-list">
              {visibleBidRecords.map(
                (record) => (
                  <RecordCard
                    key={record.record_id}
                    record={record}
                  />
                )
              )}
            </div>
          </div>
        </section>

        <section className="deal-graph-section">
          <div className="deal-section-heading">
            <div>
              <span className="deal-eyebrow">
                Causal intelligence
              </span>

              <h2>
                The system remembers why
              </h2>
            </div>

            <div className="deal-graph-stat">
              <Network size={18} />
              {relationships.length} relationships
            </div>
          </div>

          <div className="deal-relationship-grid">
            {relationships
              .slice(0, 12)
              .map((relationship) => (
                <article
                  className="deal-relationship"
                  key={
                    `${relationship.source_record_id}-`
                    + `${relationship.target_record_id}-`
                    + relationship.relationship
                  }
                >
                  <div>
                    <span>FROM</span>
                    <strong>
                      {relationship.source_record_id}
                    </strong>
                  </div>

                  <div className="deal-relationship-arrow">
                    <span>
                      {humanize(
                        relationship.relationship
                      )}
                    </span>
                    <ChevronRight size={16} />
                  </div>

                  <div>
                    <span>TO</span>
                    <strong>
                      {relationship.target_record_id}
                    </strong>
                  </div>
                </article>
              ))}
          </div>
        </section>

        <section className="deal-governance">
          <ShieldCheck size={21} />

          <div>
            <strong>
              AI recommends. Humans authorize.
            </strong>

            <p>
              {intelligence.governance_notice}
            </p>
          </div>
        </section>

        <footer className="deal-footer">
          <span>
            Project · {intelligence.project_id}
          </span>

          <span>
            {intelligence.data_notice}
          </span>
        </footer>
      </main>
    </div>
  );
}
