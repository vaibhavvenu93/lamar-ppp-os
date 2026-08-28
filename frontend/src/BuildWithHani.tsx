import {
  ArrowDown,
  ArrowRight,
  Bot,
  BrainCircuit,
  Calculator,
  Code2,
  FileSearch,
  GitBranch,
  ShieldCheck,
  UserCheck,
  X,
} from "lucide-react";


type BuildWithHaniProps = {
  onClose: () => void;
  onOpenFinancialTwin: () => void;
};


const systemFlow = [
  {
    number: "01",
    label: "LIVE PROBLEM",
    title: "Project signal appears",
    description:
      "A project event, obligation, bid issue or operating signal enters the system.",
    icon: FileSearch,
  },
  {
    number: "02",
    label: "AI INTERPRETS",
    title: "Context becomes structure",
    description:
      "AI extracts meaning, evidence, obligations and possible risks from unstructured information.",
    icon: Bot,
  },
  {
    number: "03",
    label: "RULES QUANTIFY",
    title: "Risk becomes explicit",
    description:
      "Defined rules classify severity, allocation, probability and whether escalation is required.",
    icon: GitBranch,
  },
  {
    number: "04",
    label: "PYTHON CALCULATES",
    title: "Risk becomes economics",
    description:
      "Deterministic engines recalculate CAPEX, cash flows, debt service, DSCR, NPV and equity IRR.",
    icon: Calculator,
  },
  {
    number: "05",
    label: "EXECUTIVE ENGINE",
    title: "Attention gets ranked",
    description:
      "Financial exposure, urgency and decision requirements determine what reaches the executive brief.",
    icon: BrainCircuit,
  },
  {
    number: "06",
    label: "HUMAN DECIDES",
    title: "Authority stays human",
    description:
      "The system recommends and explains. Consequential project decisions remain with Lamar's people.",
    icon: UserCheck,
  },
];


const responsibilityLayers = [
  {
    title: "AI",
    subtitle: "Interpretation",
    icon: Bot,
    items: [
      "Document interpretation",
      "Clause and obligation extraction",
      "Risk identification",
      "Evidence synthesis",
    ],
  },
  {
    title: "DETERMINISTIC CODE",
    subtitle: "Calculation",
    icon: Calculator,
    items: [
      "IRR and NPV",
      "DSCR",
      "Debt service",
      "Scenario calculations",
    ],
  },
  {
    title: "RULES",
    subtitle: "Governance",
    icon: GitBranch,
    items: [
      "Approval gates",
      "Risk thresholds",
      "Escalation logic",
      "Compliance boundaries",
    ],
  },
  {
    title: "HUMAN",
    subtitle: "Authority",
    icon: ShieldCheck,
    items: [
      "Bid / no-bid",
      "Contract position",
      "Capital commitment",
      "Risk acceptance",
    ],
  },
];


const firstMonth = [
  {
    week: "WEEK 01",
    title: "Find the bottleneck",
    description:
      "Sit beside the PPP team on one live project and map where time actually disappears across bid review, structuring, financial analysis and execution.",
  },
  {
    week: "WEEK 02",
    title: "Build one thing",
    description:
      "Take the ugliest high-frequency workflow and ship a working internal tool against real Lamar documents, data and processes.",
  },
  {
    week: "WEEK 03",
    title: "Measure it",
    description:
      "Baseline time versus new time. Track accuracy, human corrections, decisions accelerated and hours returned to the team.",
  },
  {
    week: "WEEK 04",
    title: "Kill or scale",
    description:
      "If it does not materially improve the workflow, kill it. If it works, connect it to project memory and attack the next bottleneck.",
  },
];


export default function BuildWithHani({
  onClose,
  onOpenFinancialTwin,
}: BuildWithHaniProps) {
  return (
    <div className="build-hani-overlay">
      <section className="build-hani-panel">
        <header className="build-hani-header">
          <div>
            <div className="eyebrow">
              BUILD WITH HANI
            </div>

            <h2>
              Don't start with the strategy.
              <br />
              Open the system.
            </h2>

            <p>
              This prototype is an argument for a
              way of working: take a live PPP
              problem, build against it, measure
              what changes, and let what works
              become the strategy.
            </p>
          </div>

          <button
            className="icon-button"
            onClick={onClose}
            aria-label="Close Build With Hani"
          >
            <X size={18} />
          </button>
        </header>


        <div className="build-hani-body">
          <section className="build-hani-intro">
            <div className="build-hani-intro-mark">
              <Code2 size={23} />
            </div>

            <div>
              <span className="eyebrow">
                ONE WORKING EXAMPLE
              </span>

              <h3>
                How a project signal becomes an
                executive decision.
              </h3>

              <p>
                The important part is not the
                interface. It is the separation
                between interpretation,
                deterministic calculation,
                governance and human authority.
              </p>
            </div>
          </section>


          <section className="build-hani-section">
            <div className="build-hani-section-heading">
              <span>01</span>

              <div>
                <strong>
                  OPEN THE MACHINERY
                </strong>

                <p>
                  Follow the decision path.
                </p>
              </div>
            </div>

            <div className="build-system-flow">
              {systemFlow.map(
                (step, index) => {
                  const Icon = step.icon;

                  return (
                    <div
                      className="build-flow-wrapper"
                      key={step.number}
                    >
                      <article className="build-flow-card">
                        <div className="build-flow-top">
                          <span>
                            {step.number}
                          </span>

                          <Icon size={17} />
                        </div>

                        <div className="build-flow-label">
                          {step.label}
                        </div>

                        <h4>
                          {step.title}
                        </h4>

                        <p>
                          {step.description}
                        </p>
                      </article>

                      {index <
                        systemFlow.length - 1 && (
                        <div className="build-flow-arrow">
                          <ArrowDown size={15} />
                        </div>
                      )}
                    </div>
                  );
                },
              )}
            </div>
          </section>


          <section className="build-hani-section">
            <div className="build-hani-section-heading">
              <span>02</span>

              <div>
                <strong>
                  WHAT DOES WHAT?
                </strong>

                <p>
                  AI is deliberately not allowed
                  to do everything.
                </p>
              </div>
            </div>

            <div className="responsibility-grid">
              {responsibilityLayers.map(
                (layer) => {
                  const Icon = layer.icon;

                  return (
                    <article
                      className="responsibility-card"
                      key={layer.title}
                    >
                      <div className="responsibility-icon">
                        <Icon size={18} />
                      </div>

                      <span>
                        {layer.subtitle}
                      </span>

                      <h4>
                        {layer.title}
                      </h4>

                      <ul>
                        {layer.items.map(
                          (item) => (
                            <li key={item}>
                              {item}
                            </li>
                          ),
                        )}
                      </ul>
                    </article>
                  );
                },
              )}
            </div>
          </section>


          <section className="build-hani-section">
            <div className="build-hani-section-heading">
              <span>03</span>

              <div>
                <strong>
                  IF I JOINED LAMAR MONDAY
                </strong>

                <p>
                  First month: one workflow,
                  measurable proof.
                </p>
              </div>
            </div>

            <div className="first-month-grid">
              {firstMonth.map((step) => (
                <article
                  className="first-month-card"
                  key={step.week}
                >
                  <span>
                    {step.week}
                  </span>

                  <h4>
                    {step.title}
                  </h4>

                  <p>
                    {step.description}
                  </p>
                </article>
              ))}
            </div>
          </section>


          <section className="build-hani-thesis">
            <div>
              <span className="eyebrow">
                THE OPERATING THESIS
              </span>

              <h3>
                What works becomes the strategy.
              </h3>

              <p>
                Start with a real workflow.
                Ship. Measure. Keep the useful
                parts. Then compound what Lamar
                learns from every project.
              </p>
            </div>

            <button
              className="build-hani-action"
              onClick={onOpenFinancialTwin}
            >
              Try the working engine
              <ArrowRight size={15} />
            </button>
          </section>


          <footer className="build-hani-footer">
            <ShieldCheck size={15} />

            <span>
              Independent prototype using public
              context and synthetic project data.
              No Lamar internal information.
            </span>
          </footer>
        </div>
      </section>
    </div>
  );
}
