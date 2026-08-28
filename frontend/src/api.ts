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
