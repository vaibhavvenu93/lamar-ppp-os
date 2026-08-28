import {
  Activity,
  ArrowDownRight,
  ArrowRight,
  BookOpen,
  BrainCircuit,
  Building2,
  ChevronRight,
  CircleDollarSign,
  Code2,
  FileSearch,
  Landmark,
  Radar,
  ShieldAlert,
  Timer,
  Waves,
} from "lucide-react";


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


function App() {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">L</div>

          <div>
            <div className="brand-name">LAMAR OS</div>
            <div className="brand-subtitle">
              Infrastructure Intelligence
            </div>
          </div>
        </div>

        <div className="environment-badge">
          DEMO ENVIRONMENT
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
                <Icon size={17} strokeWidth={1.8} />
                <span>{module.label}</span>
              </button>
            );
          })}
        </nav>

        <div className="sidebar-bottom">
          <button className="build-with-hani">
            <Code2 size={18} />
            <div>
              <strong>Build With Hani</strong>
              <span>Open the system</span>
            </div>
            <ChevronRight size={16} />
          </button>

          <div className="demo-notice">
            Public context + synthetic project data.
            No Lamar internal information.
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div className="lifecycle">
            {lifecycle.map((stage, index) => (
              <div className="lifecycle-step" key={stage}>
                <span
                  className={
                    index === 0
                      ? "lifecycle-name current"
                      : "lifecycle-name"
                  }
                >
                  {stage}
                </span>

                {index < lifecycle.length - 1 && (
                  <ArrowRight
                    className="lifecycle-arrow"
                    size={13}
                  />
                )}
              </div>
            ))}
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

              <h1>Good morning, Hani.</h1>

              <p>
                Three things need your attention across
                the infrastructure portfolio.
              </p>
            </div>

            <div className="brief-meta">
              <span>28 AUG 2026</span>
              <span>07:30 GCC</span>
            </div>
          </div>

          <div className="portfolio-strip">
            <div className="metric">
              <span className="metric-label">
                SIGNALS REVIEWED
              </span>
              <strong>5</strong>
              <span>across demo projects</span>
            </div>

            <div className="metric">
              <span className="metric-label">
                EXPECTED EXPOSURE
              </span>
              <strong>$12.0M</strong>
              <span>highest ranked risk</span>
            </div>

            <div className="metric">
              <span className="metric-label">
                DECISIONS REQUIRED
              </span>
              <strong>2</strong>
              <span>executive attention</span>
            </div>

            <div className="metric">
              <span className="metric-label">
                ENGINE STATUS
              </span>
              <strong className="healthy">
                40
              </strong>
              <span>automated tests passing</span>
            </div>
          </div>

          <div className="section-heading">
            <div>
              <span className="eyebrow">
                PRIORITY QUEUE
              </span>
              <h2>What needs attention</h2>
            </div>

            <span className="explainable-label">
              Explainable ranking
            </span>
          </div>

          <article className="signal-card primary-signal">
            <div className="signal-number">
              01
            </div>

            <div className="signal-content">
              <div className="signal-header">
                <div>
                  <div className="signal-tags">
                    <span className="tag high">
                      HIGH
                    </span>
                    <span className="tag">
                      RISK
                    </span>
                    <span className="project-id">
                      DEMO-WATER-001
                    </span>
                  </div>

                  <h3>Construction Cost Exposure</h3>

                  <p>
                    A modeled construction event could
                    increase project CAPEX by $30M.
                  </p>
                </div>

                <div className="attention-score">
                  <span>ATTENTION</span>
                  <strong>70</strong>
                  <small>/100</small>
                </div>
              </div>

              <div className="risk-grid">
                <div className="risk-stat">
                  <span>Potential impact</span>
                  <strong>$30.0M</strong>
                </div>

                <div className="risk-stat">
                  <span>Probability</span>
                  <strong>40%</strong>
                </div>

                <div className="risk-stat">
                  <span>Expected exposure</span>
                  <strong>$12.0M</strong>
                </div>

                <div className="risk-stat">
                  <span>CAPEX scenario</span>
                  <strong>+4.29%</strong>
                </div>
              </div>

              <div className="financial-impact">
                <div className="financial-impact-title">
                  <CircleDollarSign size={17} />
                  FINANCIAL TWIN IMPACT
                </div>

                <div className="financial-values">
                  <div>
                    <span>Equity IRR</span>
                    <strong>
                      Modeled downside
                      <ArrowDownRight size={16} />
                    </strong>
                  </div>

                  <div>
                    <span>Project NPV</span>
                    <strong>
                      Modeled downside
                      <ArrowDownRight size={16} />
                    </strong>
                  </div>

                  <div>
                    <span>Risk allocation</span>
                    <strong>Private</strong>
                  </div>
                </div>
              </div>

              <div className="signal-reason">
                <ShieldAlert size={17} />

                <div>
                  <span>WHY YOU'RE SEEING THIS</span>
                  <p>
                    High priority; $12M expected financial
                    exposure; executive decision required.
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
            </div>
          </article>

          <div className="secondary-signals">
            <article className="signal-card compact">
              <div className="signal-number">
                02
              </div>

              <div className="compact-content">
                <div className="signal-tags">
                  <span className="tag high">
                    HIGH
                  </span>
                  <span className="tag">
                    OBLIGATION
                  </span>
                </div>

                <h3>
                  Consortium Submission Approaching
                </h3>

                <p>
                  Synthetic bid package requires final
                  consortium approval within three days.
                </p>

                <div className="compact-footer">
                  <span>
                    <Timer size={15} />
                    3 days
                  </span>

                  <button className="text-button">
                    Review obligation
                    <ArrowRight size={14} />
                  </button>
                </div>
              </div>
            </article>

            <article className="signal-card compact">
              <div className="signal-number">
                03
              </div>

              <div className="compact-content">
                <div className="signal-tags">
                  <span className="tag medium">
                    MEDIUM
                  </span>
                  <span className="tag">
                    FINANCIAL
                  </span>
                </div>

                <h3>
                  Debt-Service Coverage Watch
                </h3>

                <p>
                  Downside scenarios should be reviewed
                  before the next financing discussion.
                </p>

                <div className="compact-footer">
                  <span>
                    <CircleDollarSign size={15} />
                    $2.0M exposure
                  </span>

                  <button className="text-button">
                    Open Financial Twin
                    <ArrowRight size={14} />
                  </button>
                </div>
              </div>
            </article>
          </div>

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
                  AI interprets. Engines calculate.
                  Humans decide.
                </h3>
                <p>
                  Every consequential number is produced
                  by deterministic logic and can be traced
                  back to its assumptions.
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
                <h3>Open the machinery.</h3>
                <p>
                  See how a risk becomes a scenario,
                  inspect the calculation, change an
                  assumption, and rerun the system.
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
              LAMAR PPP OS — INDEPENDENT PROTOTYPE
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
