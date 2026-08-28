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
