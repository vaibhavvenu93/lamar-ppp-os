import {
  AlertTriangle,
  ArrowRight,
  BriefcaseBusiness,
  Building2,
  CalendarDays,
  CheckCircle2,
  CircleDollarSign,
  LoaderCircle,
  MapPin,
  Radar,
  ShieldCheck,
  Target,
  X,
} from "lucide-react";
import {
  useEffect,
  useMemo,
  useState,
} from "react";

import {
  getOpportunities,
  getOpportunity,
  OpportunityDetail,
  OpportunityPortfolioResponse,
  OpportunitySummary,
} from "./api";


type OpportunityRadarProps = {
  onClose: () => void;
};


function formatMoney(
  value: number | null,
): string {
  if (value === null) {
    return "—";
  }

  if (Math.abs(value) >= 1_000_000_000) {
    return `$${(
      value / 1_000_000_000
    ).toFixed(2)}B`;
  }

  if (Math.abs(value) >= 1_000_000) {
    return `$${(
      value / 1_000_000
    ).toFixed(0)}M`;
  }

  return `$${value.toLocaleString()}`;
}


function formatDate(
  value: string | null,
): string {
  if (!value) {
    return "Not specified";
  }

  const date = new Date(
    `${value}T00:00:00`
  );

  return date.toLocaleDateString(
    "en-US",
    {
      day: "2-digit",
      month: "short",
      year: "numeric",
    },
  );
}


function scoreClass(
  score: number | null,
): string {
  if (score === null) {
    return "radar-score-neutral";
  }

  if (score >= 85) {
    return "radar-score-strategic";
  }

  if (score >= 70) {
    return "radar-score-high";
  }

  if (score >= 55) {
    return "radar-score-medium";
  }

  return "radar-score-low";
}


function OpportunityRow({
  opportunity,
  selected,
  onSelect,
}: {
  opportunity: OpportunitySummary;
  selected: boolean;
  onSelect: () => void;
}) {
  return (
    <button
      type="button"
      className={
        selected
          ? "radar-opportunity-row selected"
          : "radar-opportunity-row"
      }
      onClick={onSelect}
    >
      <div
        className={`radar-score ${scoreClass(
          opportunity.overall_score
        )}`}
      >
        <strong>
          {opportunity.overall_score?.toFixed(
            0
          ) ?? "—"}
        </strong>
        <span>FIT</span>
      </div>

      <div className="radar-opportunity-main">
        <div className="radar-opportunity-heading">
          <strong>{opportunity.name}</strong>

          <span>
            {opportunity.priority ?? "UNSCORED"}
          </span>
        </div>

        <div className="radar-opportunity-meta">
          <span>
            <MapPin size={13} />
            {opportunity.country}
          </span>

          <span>
            <Building2 size={13} />
            {opportunity.sector.replaceAll(
              "_",
              " "
            )}
          </span>

          <span>
            <CircleDollarSign size={13} />
            {formatMoney(
              opportunity.estimated_capex_usd
            )}
          </span>
        </div>
      </div>

      <div className="radar-opportunity-side">
        <span>
          {opportunity.procurement_model}
        </span>

        <strong>
          {opportunity.recommendation ?? "REVIEW"}
        </strong>

        <ArrowRight size={16} />
      </div>
    </button>
  );
}


function ScoreBreakdown({
  detail,
}: {
  detail: OpportunityDetail;
}) {
  const assessment = detail.assessment;

  if (!assessment) {
    return null;
  }

  return (
    <section className="radar-section">
      <div className="radar-section-heading">
        <span>02</span>

        <div>
          <strong>
            Why this opportunity scored{" "}
            {assessment.overall_score.toFixed(1)}
          </strong>

          <p>
            Seven explicit dimensions are
            weighted by deterministic rules.
          </p>
        </div>
      </div>

      <div className="radar-score-breakdown">
        {assessment.components.map(
          (component) => (
            <div
              className="radar-score-component"
              key={component.name}
            >
              <div className="radar-score-component-top">
                <span>{component.name}</span>

                <strong>
                  {component.score.toFixed(0)}
                </strong>
              </div>

              <div className="radar-score-track">
                <div
                  className="radar-score-fill"
                  style={{
                    width: `${component.score}%`,
                  }}
                />
              </div>

              <div className="radar-score-component-foot">
                <span>
                  Weight{" "}
                  {(component.weight * 100).toFixed(
                    0
                  )}
                  %
                </span>

                <span>
                  Contribution{" "}
                  {component.weighted_score.toFixed(
                    1
                  )}
                </span>
              </div>

              <p>{component.rationale}</p>
            </div>
          )
        )}
      </div>
    </section>
  );
}


function OpportunityInvestigation({
  detail,
}: {
  detail: OpportunityDetail;
}) {
  const assessment = detail.assessment;

  return (
    <div className="radar-investigation">
      <section className="radar-investigation-hero">
        <div>
          <div className="radar-kicker">
            OPPORTUNITY INVESTIGATION
          </div>

          <h2>{detail.name}</h2>

          <p>{detail.description}</p>
        </div>

        {assessment && (
          <div
            className={`radar-hero-score ${scoreClass(
              assessment.overall_score
            )}`}
          >
            <span>LAMAR FIT</span>

            <strong>
              {assessment.overall_score.toFixed(1)}
            </strong>

            <small>/ 100</small>
          </div>
        )}
      </section>

      <div className="radar-fact-strip">
        <div>
          <span>CAPEX</span>
          <strong>
            {formatMoney(
              detail.estimated_capex_usd
            )}
          </strong>
        </div>

        <div>
          <span>MODEL</span>
          <strong>
            {detail.procurement_model}
          </strong>
        </div>

        <div>
          <span>CONCESSION</span>
          <strong>
            {detail.concession_years
              ? `${detail.concession_years} years`
              : "—"}
          </strong>
        </div>

        <div>
          <span>DEADLINE</span>
          <strong>
            {formatDate(
              detail.submission_deadline
            )}
          </strong>
        </div>
      </div>

      <section className="radar-section">
        <div className="radar-section-heading">
          <span>01</span>

          <div>
            <strong>Opportunity thesis</strong>
            <p>
              What the system currently knows
              before bid diligence begins.
            </p>
          </div>
        </div>

        <div className="radar-thesis-grid">
          <div className="radar-thesis-card">
            <Target size={18} />

            <span>STRATEGIC THEME</span>

            <strong>
              {detail.strategic_theme ?? "—"}
            </strong>
          </div>

          <div className="radar-thesis-card">
            <MapPin size={18} />

            <span>LOCATION</span>

            <strong>
              {detail.project_location ?? "—"}
            </strong>
          </div>

          <div className="radar-thesis-card">
            <Building2 size={18} />

            <span>AUTHORITY</span>

            <strong>{detail.authority}</strong>
          </div>

          <div className="radar-thesis-card">
            <CircleDollarSign size={18} />

            <span>REVENUE MODEL</span>

            <strong>
              {detail.expected_revenue_model ??
                "—"}
            </strong>
          </div>
        </div>
      </section>

      <ScoreBreakdown detail={detail} />

      {assessment && (
        <section className="radar-section">
          <div className="radar-section-heading">
            <span>03</span>

            <div>
              <strong>
                Pursuit intelligence
              </strong>

              <p>
                Strongest reasons to pursue and
                issues requiring diligence.
              </p>
            </div>
          </div>

          <div className="radar-pursuit-grid">
            <div className="radar-intelligence-card positive">
              <div className="radar-intelligence-title">
                <CheckCircle2 size={17} />
                WHY PURSUE
              </div>

              {assessment.strengths.map(
                (strength) => (
                  <p key={strength}>
                    {strength}
                  </p>
                )
              )}
            </div>

            <div className="radar-intelligence-card warning">
              <div className="radar-intelligence-title">
                <AlertTriangle size={17} />
                WATCH BEFORE BID
              </div>

              {assessment.concerns.map(
                (concern) => (
                  <p key={concern}>
                    {concern}
                  </p>
                )
              )}
            </div>
          </div>
        </section>
      )}

      <section className="radar-section">
        <div className="radar-section-heading">
          <span>04</span>

          <div>
            <strong>
              Known bid surface
            </strong>

            <p>
              Initial requirements and risks
              discovered before document analysis.
            </p>
          </div>
        </div>

        <div className="radar-pursuit-grid">
          <div className="radar-list-card">
            <div className="radar-intelligence-title">
              <BriefcaseBusiness size={17} />
              KNOWN REQUIREMENTS
            </div>

            {detail.known_requirements.map(
              (requirement, index) => (
                <div
                  className="radar-list-item"
                  key={requirement}
                >
                  <span>
                    {String(index + 1).padStart(
                      2,
                      "0"
                    )}
                  </span>

                  <p>{requirement}</p>
                </div>
              )
            )}
          </div>

          <div className="radar-list-card">
            <div className="radar-intelligence-title">
              <AlertTriangle size={17} />
              KNOWN RISKS
            </div>

            {detail.known_risks.map(
              (risk, index) => (
                <div
                  className="radar-list-item"
                  key={risk}
                >
                  <span>
                    {String(index + 1).padStart(
                      2,
                      "0"
                    )}
                  </span>

                  <p>{risk}</p>
                </div>
              )
            )}
          </div>
        </div>
      </section>

      {assessment && (
        <section className="radar-decision-card">
          <div>
            <div className="radar-kicker">
              SYSTEM RECOMMENDATION
            </div>

            <h3>
              {assessment.recommendation}
            </h3>

            <p>
              {assessment.recommendation_reason}
            </p>
          </div>

          <div className="radar-decision-actions">
            <button
              type="button"
              className="radar-secondary-action"
            >
              Investigate deeper
            </button>

            <button
              type="button"
              className="radar-primary-action"
            >
              Run Bid / No-Bid
              <ArrowRight size={16} />
            </button>
          </div>
        </section>
      )}

      <section className="radar-governance">
        <ShieldCheck size={17} />

        <div>
          <strong>
            HUMAN DECISION BOUNDARY
          </strong>

          <p>
            Opportunity scoring prioritizes
            executive attention. It does not
            authorize pursuit, consortium
            commitments, capital allocation, or
            Bid / No-Bid decisions.
          </p>

          <small>{detail.data_notice}</small>
        </div>
      </section>
    </div>
  );
}


export default function OpportunityRadar({
  onClose,
}: OpportunityRadarProps) {
  const [
    portfolio,
    setPortfolio,
  ] = useState<
    OpportunityPortfolioResponse | null
  >(null);

  const [
    selectedId,
    setSelectedId,
  ] = useState<string | null>(null);

  const [
    detail,
    setDetail,
  ] = useState<OpportunityDetail | null>(
    null
  );

  const [
    loading,
    setLoading,
  ] = useState(true);

  const [
    detailLoading,
    setDetailLoading,
  ] = useState(false);

  const [
    error,
    setError,
  ] = useState<string | null>(null);


  useEffect(() => {
    async function loadPortfolio() {
      try {
        setLoading(true);

        const response =
          await getOpportunities();

        setPortfolio(response);

        if (
          response.opportunities.length > 0
        ) {
          setSelectedId(
            response.opportunities[0]
              .opportunity_id
          );
        }
      } catch (caughtError) {
        setError(
          caughtError instanceof Error
            ? caughtError.message
            : "Opportunity Radar failed."
        );
      } finally {
        setLoading(false);
      }
    }

    void loadPortfolio();
  }, []);


  useEffect(() => {
    if (!selectedId) {
      return;
    }

    async function loadDetail() {
      try {
        setDetailLoading(true);

        const response =
          await getOpportunity(selectedId);

        setDetail(response);
      } catch (caughtError) {
        setError(
          caughtError instanceof Error
            ? caughtError.message
            : "Opportunity investigation failed."
        );
      } finally {
        setDetailLoading(false);
      }
    }

    void loadDetail();
  }, [selectedId]);


  const selectedOpportunity =
    useMemo(
      () =>
        portfolio?.opportunities.find(
          (opportunity) =>
            opportunity.opportunity_id ===
            selectedId
        ) ?? null,
      [portfolio, selectedId],
    );


  return (
    <div className="radar-overlay">
      <div className="radar-shell">
        <header className="radar-header">
          <div>
            <div className="radar-kicker">
              PHASE 2 · DISCOVER
            </div>

            <h1>
              <Radar size={24} />
              Opportunity Radar
            </h1>

            <p>
              Find the infrastructure
              opportunities worth spending bid
              resources on before the expensive
              work begins.
            </p>
          </div>

          <button
            type="button"
            className="radar-close"
            onClick={onClose}
            aria-label="Close Opportunity Radar"
          >
            <X size={20} />
          </button>
        </header>

        {loading && (
          <div className="radar-loading">
            <LoaderCircle
              className="spin"
              size={24}
            />

            Loading opportunity pipeline…
          </div>
        )}

        {error && (
          <div className="radar-error">
            <AlertTriangle size={18} />
            {error}
          </div>
        )}

        {!loading && portfolio && (
          <>
            <section className="radar-portfolio-summary">
              <div>
                <span>OPPORTUNITIES</span>

                <strong>
                  {portfolio.opportunity_count}
                </strong>
              </div>

              <div>
                <span>PIPELINE CAPEX</span>

                <strong>
                  {formatMoney(
                    portfolio.total_pipeline_capex_usd
                  )}
                </strong>
              </div>

              <div>
                <span>STRATEGIC</span>

                <strong>
                  {portfolio.strategic_count}
                </strong>
              </div>

              <div>
                <span>HIGH PRIORITY</span>

                <strong>
                  {portfolio.high_priority_count}
                </strong>
              </div>

              <div>
                <span>SCORING</span>

                <strong>
                  DETERMINISTIC
                </strong>
              </div>
            </section>

            <div className="radar-workspace">
              <aside className="radar-pipeline">
                <div className="radar-pipeline-heading">
                  <div>
                    <span>
                      OPPORTUNITY PIPELINE
                    </span>

                    <strong>
                      Ranked by strategic fit
                    </strong>
                  </div>

                  <Target size={18} />
                </div>

                <div className="radar-pipeline-list">
                  {portfolio.opportunities.map(
                    (opportunity) => (
                      <OpportunityRow
                        key={
                          opportunity.opportunity_id
                        }
                        opportunity={opportunity}
                        selected={
                          opportunity.opportunity_id ===
                          selectedId
                        }
                        onSelect={() =>
                          setSelectedId(
                            opportunity.opportunity_id
                          )
                        }
                      />
                    )
                  )}
                </div>

                <div className="radar-policy">
                  <ShieldCheck size={15} />

                  <p>
                    {portfolio.scoring_policy}
                  </p>
                </div>
              </aside>

              <main className="radar-detail">
                {detailLoading && (
                  <div className="radar-loading">
                    <LoaderCircle
                      className="spin"
                      size={22}
                    />

                    Investigating{" "}
                    {selectedOpportunity?.name ??
                      "opportunity"}
                    …
                  </div>
                )}

                {!detailLoading && detail && (
                  <OpportunityInvestigation
                    detail={detail}
                  />
                )}
              </main>
            </div>

            <footer className="radar-footer">
              <div>
                <CalendarDays size={15} />

                Synthetic Phase 2 opportunity
                portfolio
              </div>

              <span>
                {portfolio.data_notice}
              </span>
            </footer>
          </>
        )}
      </div>
    </div>
  );
}
