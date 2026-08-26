export type FinanceLayoutVariant = "hero-number" | "comparison" | "document" | "table";

export type SupportingMetric = {
  label: string;
  value: string;
  direction?: "up" | "down" | "flat";
};

export type SourceContext = {
  sourceLabel?: string;
  sourceDate?: string;
  period?: string;
  sampleData?: boolean;
};

export type FlowNode = {
  id: string;
  label: string;
  value?: string;
};

export type FlowEdge = {
  from: string;
  to: string;
  value?: number;
  label?: string;
};

export type CausalNode = {
  id: string;
  label: string;
  detail?: string;
};

export type CausalEdge = {
  from: string;
  to: string;
  relation?: "positive" | "negative" | "uncertain";
  label?: string;
};

export type ResearchTimelineEvent = {
  date: string;
  title: string;
  description?: string;
  source?: string;
};

export type Scenario = {
  name: string;
  title?: string;
  description: string;
  trigger: string;
  probability?: number;
  metrics?: string[];
};

export type ThesisBreakerCondition = {
  title: string;
  description?: string;
  evidenceToWatch?: string;
};
