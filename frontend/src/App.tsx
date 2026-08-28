import {
  Activity,
  ArrowRight,
  BookOpen,
  BrainCircuit,
  Building2,
  ChevronRight,
  CircleDollarSign,
  Code2,
  FileSearch,
  Landmark,
  LoaderCircle,
  Radar,
  ShieldAlert,
  Waves,
} from "lucide-react";
import {
  useEffect,
  useState,
} from "react";

import {
  ExecutiveBriefItem,
  ExecutiveBriefResponse,
  getExecutiveBrief,
} from "./api";


const lifecycle = [
  "Discover",
  "Bid",
  "Structure",
  "Finance",
  "Build",
  "Operate",
  "Learn",
];


const modules = [
  {
    label: "Executive Brief",
    icon: Activity,
    active: true,
  },
  {
    label: "Opportunity Radar",
    icon: Radar,
  },
  {
    label: "Bid Intelligence",
    icon: FileSearch,
  },
  {
    label: "Deal Room",
    icon: Building2,
  },
  {
    label: "Financial Twin",
    icon: CircleDollarSign,
  },
  {
    label: "Risk Intelligence",
    icon: ShieldAlert,
  },
  {
    label: "Construction",
    icon: Landmark,
  },
  {
    label: "Operations",
    icon: Waves,
  },
  {
    label: "Institutional Memory",
    icon: BrainCircuit,
  },
];


function formatMoney(
  value: number | null,
): string {
  if (value === null) {
    return "—";
  }

  if (value >= 1_000_000_000) {
    return `$${(
      value / 1_000_000_000
    ).toFixed(1)}B`;
  }

  if (value >= 1_000_000) {
    return `$${(
      value / 1_000_000
    ).toFixed(1)}M`;
  }

  if (value >= 1_000) {
    return `$${(
      value / 1_000
    ).toFixed(1)}K`;
  }

  return `$${value.toFixed(0)}`;
}


function priorityClass(
  priority: string,
): string {
  return priority.toLowerCase();
}


function SignalCard({
  item,
}: {
  item: ExecutiveBriefItem;
}) {
  return (
    <article
      className={
        item.rank === 1
          ? "signal-card primary-signal"
          : "signal-card compact"
      }
    >
      <div className="signal-number">
        {String(item.rank).padStart(2, "0")}
      </div>

      <div
        className={
          item.rank === 1
            ? "signal-content"
            : "compact-content"
        }
      >
        <div className="signal-tags">
          <span
            className={
              `tag ${priorityClass(
                item.priority,
              )}`
            }
          >
            {item.priority}
          </span>

          <span className="tag">
            {item.type}
          </span>

          <span className="project-id">
            {item.project_id}
          </span>
        </div>

        {item.rank === 1 ? (
          <>
            <div className="signal-header">
              <div>
                <h3>{item.title}</h3>
                <p>{item.summary}</p>
              </div>

              <div className="attention-score">
                <span>ATTENTION</span>

                <strong>
                  {item.attention_score}
                </strong>

                <small>/100</small>
              </div>
            </div>

            <div className="risk-grid">
              <div className="risk-stat">
                <span>
                  Expected exposure
                </span>

                <strong>
                  {formatMoney(
                    item.financial_exposure_usd,
                  )}
                </strong>
              </div>

              <div className="risk-stat">
                <span>
                  Decision required
                </span>

                <strong>
                  {item.requires_decision
                    ? "YES"
                    : "NO"}
                </strong>
              </div>

              <div className="risk-stat">
                <span>Signal type</span>
                <strong>{item.type}</strong>
              </div>

              <div className="risk-stat">
                <span>Priority</span>
                <strong>
                  {item.priority}
                </strong>
              </div>
            </div>

            <div className="financial-impact">
              <div className="financial-impact-title">
                <CircleDollarSign size={17} />
                ENGINE TRACE
              </div>

              <div className="financial-values">
                <div>
                  <span>
                    Financial translation
                  </span>
                  <strong>
                    Scenario modeled
                  </strong>
                </div>

                <div>
                  <span>
                    Executive ranking
                  </span>
                  <strong>
                    {item.attention_score}/100
                  </strong>
                </div>

                <div>
                  <span>
                    Human approval
                  </span>
                  <strong>
                    {item.requires_decision
                      ? "Required"
                      : "Not required"}
                  </strong>
                </div>
              </div>
            </div>

            <div className="signal-reason">
              <ShieldAlert size={17} />

              <div>
                <span>
                  WHY YOU'RE SEEING THIS
                </span>

                <p>
                  {item.ranking_reason}
                </p>
              </div>
            </div>

            <div className="signal-actions">
              <button className="primary-button">
                Open analysis
                <ArrowRight size={15} />
              </button>

              <button className="secondary-button">
                Run scenario
              </button>

              <button className="text-button">
                View calculation trace
              </button>
            </div>
          </>
        ) : (
          <>
            <h3>{item.title}</h3>

            <p>{item.summary}</p>

            <div className="compact-footer">
              <span>
                <CircleDollarSign size={15} />

                {item.financial_exposure_usd
                  ? `${formatMoney(
                      item.financial_exposure_usd,
                    )} exposure`
                  : item.days_to_deadline !== null
                    ? `${item.days_to_deadline} days`
                    : "Executive signal"}
              </span>

              <button className="text-button">
                Review signal
                <ArrowRight size={14} />
              </button>
            </div>
          </>
        )}
      </div>
    </article>
  );
}


function App() {
  const [
    data,
    setData,
  ] = useState<
    ExecutiveBriefResponse | null
  >(null);

  const [
    error,
    setError,
  ] = useState<string | null>(null);

  useEffect(() => {
    getExecutiveBrief()
      .then(setData)
      .catch((requestError: Error) => {
        setError(requestError.message);
      });
  }, []);

  const items = data?.brief.items ?? [];

  const totalExposure = items.reduce(
    (total, item) =>
      total +
      (item.financial_exposure_usd ?? 0),
    0,
  );

  const decisionsRequired = items.filter(
    (item) => item.requires_decision,
  ).length;

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">
            L
          </div>

          <div>
            <div className="brand-name">
              LAMAR OS
            </div>

            <div className="brand-subtitle">
              Infrastructure Intelligence
            </div>
          </div>
        </div>

        <div className="environment-badge">
          {data?.environment ??
            "DEMO ENVIRONMENT"}
        </div>

        <nav className="module-nav">
          <div className="nav-section-label">
            COMMAND CENTER
          </div>

          {modules.map((module) => {
            const Icon = module.icon;

            return (
              <button
                className={
                  module.active
                    ? "nav-item active"
                    : "nav-item"
                }
                key={module.label}
              >
                <Icon
                  size={17}
                  strokeWidth={1.8}
                />

                <span>
                  {module.label}
                </span>
              </button>
            );
          })}
        </nav>

        <div className="sidebar-bottom">
          <button className="build-with-hani">
            <Code2 size={18} />

            <div>
              <strong>
                Build With Hani
              </strong>

              <span>
                Open the system
              </span>
            </div>

            <ChevronRight size={16} />
          </button>

          <div className="demo-notice">
            {data?.data_notice ??
              "Public context + synthetic project data. No Lamar internal information."}
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div className="lifecycle">
            {lifecycle.map(
              (stage, index) => (
                <div
                  className="lifecycle-step"
                  key={stage}
                >
                  <span
                    className={
                      index === 0
                        ? "lifecycle-name current"
                        : "lifecycle-name"
                    }
                  >
                    {stage}
                  </span>

                  {index <
                    lifecycle.length - 1 && (
                    <ArrowRight
                      className="lifecycle-arrow"
                      size={13}
                    />
                  )}
                </div>
              ),
            )}
          </div>

          <div className="system-status">
            <span className="status-dot" />
            SYSTEM ONLINE
          </div>
        </header>

        <section className="workspace">
          <div className="page-intro">
            <div>
              <div className="eyebrow">
                EXECUTIVE COMMAND CENTER
              </div>

              <h1>
                {data?.brief.greeting ??
                  "Good morning, Hani."}
              </h1>

              <p>
                {data?.brief.summary ??
                  "Loading infrastructure intelligence..."}
              </p>
            </div>

            <div className="brief-meta">
              <span>
                LIVE ENGINE OUTPUT
              </span>
              <span>V0.1</span>
            </div>
          </div>

          <div className="portfolio-strip">
            <div className="metric">
              <span className="metric-label">
                SIGNALS REVIEWED
              </span>

              <strong>
                {data?.brief
                  .total_signals_reviewed ??
                  "—"}
              </strong>

              <span>
                intelligence pipeline
              </span>
            </div>

            <div className="metric">
              <span className="metric-label">
                TOP-3 EXPOSURE
              </span>

              <strong>
                {data
                  ? formatMoney(
                      totalExposure,
                    )
                  : "—"}
              </strong>

              <span>
                probability weighted
              </span>
            </div>

            <div className="metric">
              <span className="metric-label">
                DECISIONS REQUIRED
              </span>

              <strong>
                {data
                  ? decisionsRequired
                  : "—"}
              </strong>

              <span>
                human approval gates
              </span>
            </div>

            <div className="metric">
              <span className="metric-label">
                ENGINE STATUS
              </span>

              <strong className="healthy">
                40
              </strong>

              <span>
                automated tests passing
              </span>
            </div>
          </div>

          <div className="section-heading">
            <div>
              <span className="eyebrow">
                PRIORITY QUEUE
              </span>

              <h2>
                What needs attention
              </h2>
            </div>

            <span className="explainable-label">
              Explainable ranking
            </span>
          </div>

          {!data && !error && (
            <div className="system-card">
              <LoaderCircle size={20} />

              <div>
                <span className="eyebrow">
                  CONNECTING TO LAMAR OS
                </span>

                <h3>
                  Running Executive Brief...
                </h3>
              </div>
            </div>
          )}

          {error && (
            <div className="system-card">
              <ShieldAlert size={20} />

              <div>
                <span className="eyebrow">
                  API CONNECTION
                </span>

                <h3>
                  Executive Brief unavailable.
                </h3>

                <p>{error}</p>
              </div>
            </div>
          )}

          {items.length > 0 && (
            <>
              <SignalCard item={items[0]} />

              <div className="secondary-signals">
                {items
                  .slice(1)
                  .map((item) => (
                    <SignalCard
                      item={item}
                      key={item.signal_id}
                    />
                  ))}
              </div>
            </>
          )}

          <section className="system-section">
            <div className="system-card">
              <div className="system-icon">
                <BrainCircuit size={22} />
              </div>

              <div>
                <span className="eyebrow">
                  SYSTEM PRINCIPLE
                </span>

                <h3>
                  AI interprets. Engines
                  calculate. Humans decide.
                </h3>

                <p>
                  {data?.governance
                    .decision_policy ??
                    "Consequential project decisions remain with humans."}
                </p>
              </div>
            </div>

            <div className="system-card build-card">
              <div className="system-icon">
                <Code2 size={22} />
              </div>

              <div>
                <span className="eyebrow">
                  BUILD WITH HANI
                </span>

                <h3>
                  Open the machinery.
                </h3>

                <p>
                  See how a risk becomes a
                  financial scenario, inspect
                  the calculation, change an
                  assumption, and rerun it.
                </p>

                <button className="text-button">
                  Explore how this works
                  <ArrowRight size={14} />
                </button>
              </div>
            </div>
          </section>

          <footer className="product-footer">
            <div>
              <Landmark size={15} />
              LAMAR PPP OS — INDEPENDENT
              PROTOTYPE
            </div>

            <div>
              <BookOpen size={15} />
              PUBLIC CONTEXT + SYNTHETIC DATA
            </div>
          </footer>
        </section>
      </main>
    </div>
  );
}


export default App;
