export type ExecutiveBriefItem = {
  rank: number;
  signal_id: string;
  project_id: string;
  title: string;
  summary: string;
  type: string;
  priority: string;
  attention_score: number;
  financial_exposure_usd: number | null;
  days_to_deadline: number | null;
  requires_decision: boolean;
  recommended_action: string | null;
  ranking_reason: string;
  traceability: string | null;
};


export type ExecutiveBriefResponse = {
  product: string;
  environment: string;
  data_notice: string;

  brief: {
    title: string;
    greeting: string;
    summary: string;
    total_signals_reviewed: number;
    critical_signal_count: number;
    items: ExecutiveBriefItem[];
  };

  governance: {
    calculation_policy: string;
    ai_policy: string;
    decision_policy: string;
  };
};


export type ScenarioRequest = {
  name?: string;
  capex_change_pct?: number;
  revenue_change_pct?: number;
  opex_change_pct?: number;
  interest_rate_change_pct?: number;
};


export type ScenarioMetrics = {
  equity_irr: number | null;
  project_npv_usd: number | null;
  minimum_dscr: number | null;
};


export type ScenarioResponse = {
  scenario_name: string;

  base: ScenarioMetrics;
  scenario: ScenarioMetrics;

  equity_irr_change: number | null;
  project_npv_change_usd: number | null;
  minimum_dscr_change: number | null;

  calculation_engine: string;
  data_notice: string;
  human_decision_required: boolean;
};


export type OpportunityScoreComponent = {
  name: string;
  score: number;
  weight: number;
  weighted_score: number;
  rationale: string;
  evidence: string | null;
};


export type OpportunityAssessment = {
  overall_score: number;
  priority: string;
  recommendation: string;
  recommendation_reason: string;

  strategic_fit: number;
  sector_fit: number;
  market_fit: number;
  delivery_fit: number;
  financing_fit: number;
  consortium_readiness: number;
  competitive_position: number;

  strengths: string[];
  concerns: string[];

  components: OpportunityScoreComponent[];

  human_decision_required: boolean;
};


export type OpportunitySummary = {
  opportunity_id: string;
  name: string;
  country: string;
  sector: string;
  authority: string;

  procurement_model: string;
  status: string;

  estimated_capex_usd: number | null;
  concession_years: number | null;
  submission_deadline: string | null;

  strategic_theme: string | null;
  project_location: string | null;

  overall_score: number | null;
  priority: string | null;
  recommendation: string | null;

  known_risk_count: number;
  known_requirement_count: number;

  is_demo: boolean;
  data_classification: string;
};


export type OpportunityDetail = {
  opportunity_id: string;
  name: string;
  country: string;
  sector: string;
  authority: string;

  description: string | null;

  procurement_model: string;
  status: string;

  estimated_capex_usd: number | null;
  concession_years: number | null;
  submission_deadline: string | null;

  expected_revenue_model: string | null;
  project_location: string | null;
  strategic_theme: string | null;

  consortium_required: boolean;
  financing_required: boolean;

  known_requirements: string[];
  known_risks: string[];
  tags: string[];

  assessment: OpportunityAssessment | null;

  data_notice: string;
  human_bid_decision_required: boolean;
};


export type OpportunityPortfolioResponse = {
  product: string;
  module: string;

  opportunity_count: number;
  total_pipeline_capex_usd: number;

  strategic_count: number;
  high_priority_count: number;

  opportunities: OpportunitySummary[];

  scoring_policy: string;
  data_notice: string;
};


export type DocumentPackageSummary = {
  project_id: string;
  opportunity_id: string | null;
  analysis_id: string;
  status: string;

  document_count: number;
  evidence_count: number;
  requirement_count: number;
  obligation_count: number;
  risk_count: number;
  clarification_count: number;
  pending_review_count: number;

  executive_summary: string | null;
  human_review_required: boolean;
};


export type DocumentEvidence = {
  evidence_id: string;
  document_id: string;
  document_name: string;
  page_number: number | null;
  clause_reference: string | null;
  section_title: string | null;
  source_text: string | null;
  confidence: number;
};


export type DocumentRequirement = {
  requirement_id: string;
  title: string;
  description: string;
  category: string;
  mandatory: boolean;
  responsible_party: string | null;
  due_date: string | null;
  evidence_ids: string[];
  confidence: number;
  review_status: string;
};


export type DocumentObligation = {
  obligation_id: string;
  title: string;
  description: string;
  category: string;
  obligated_party: string | null;
  beneficiary_party: string | null;
  trigger: string | null;
  deadline: string | null;
  financial_consequence_usd: number | null;
  consequence_description: string | null;
  evidence_ids: string[];
  confidence: number;
  review_status: string;
};


export type DocumentProjectDate = {
  date_id: string;
  title: string;
  event_date: string;
  description: string | null;
  critical: boolean;
  evidence_ids: string[];
  confidence: number;
  review_status: string;
};


export type DocumentRisk = {
  risk_id: string;
  title: string;
  description: string;
  category: string;
  potential_impact: string | null;
  estimated_impact_usd: number | null;
  evidence_ids: string[];
  confidence: number;
  review_status: string;
};


export type DocumentClarification = {
  clarification_id: string;
  title: string;
  question: string;
  rationale: string;
  related_document_ids: string[];
  evidence_ids: string[];
  priority: string;
  human_submission_required: boolean;
  review_status: string;
};


export type DocumentAgentRun = {
  run_id: string;
  project_id: string;
  agent_name: string;
  task: string;
  status: string;

  input_record_ids: string[];
  tools_used: string[];
  output_record_ids: string[];
  evidence_ids: string[];

  summary: string | null;

  started_at: string | null;
  completed_at: string | null;

  human_review_required: boolean;
  reviewed_by: string | null;
};


export type DocumentIntelligenceResponse = {
  summary: DocumentPackageSummary;

  requirements: DocumentRequirement[];
  obligations: DocumentObligation[];
  project_dates: DocumentProjectDate[];
  risks: DocumentRisk[];
  clarifications: DocumentClarification[];
  evidence: DocumentEvidence[];

  agent_run: DocumentAgentRun;

  data_notice: string;
  governance_notice: string;
};


export async function getExecutiveBrief():
  Promise<ExecutiveBriefResponse> {
  const response = await fetch(
    "/api/executive-brief"
  );

  if (!response.ok) {
    throw new Error(
      `Executive Brief request failed: ${response.status}`
    );
  }

  return response.json();
}


export async function runFinancialScenario(
  scenario: ScenarioRequest,
): Promise<ScenarioResponse> {
  const response = await fetch(
    "/api/scenario",
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify(scenario),
    },
  );

  if (!response.ok) {
    throw new Error(
      `Financial Twin request failed: ${response.status}`
    );
  }

  return response.json();
}


export async function getOpportunities():
  Promise<OpportunityPortfolioResponse> {
  const response = await fetch(
    "/api/opportunities"
  );

  if (!response.ok) {
    throw new Error(
      `Opportunity Radar request failed: ${response.status}`
    );
  }

  return response.json();
}


export async function getOpportunity(
  opportunityId: string,
): Promise<OpportunityDetail> {
  const response = await fetch(
    `/api/opportunities/${encodeURIComponent(
      opportunityId
    )}`
  );

  if (!response.ok) {
    throw new Error(
      `Opportunity investigation request failed: ${response.status}`
    );
  }

  return response.json();
}


export async function investigateOpportunity(
  opportunityId: string,
): Promise<DocumentIntelligenceResponse> {
  const response = await fetch(
    `/api/opportunities/${encodeURIComponent(
      opportunityId
    )}/investigate`,
    {
      method: "POST",
    },
  );

  if (!response.ok) {
    let detail = (
      `Document Intelligence request failed: ${response.status}`
    );

    try {
      const body = await response.json();

      if (
        typeof body?.detail === "string"
        && body.detail.length > 0
      ) {
        detail = body.detail;
      }
    } catch {
      // Preserve the HTTP status error when the response
      // does not contain a JSON error body.
    }

    throw new Error(detail);
  }

  return response.json();
}
