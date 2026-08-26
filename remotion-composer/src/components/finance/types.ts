import type { ThemeConfig } from "../../theme";

export type FinanceValue = string | number;

export type FinanceBrand = {
  label?: string;
  series?: string;
  issue?: string;
};

export type FinanceLayoutVariant = "hero-number" | "comparison" | "document" | "table";

export type SupportingMetric = {
  label: string;
  value: FinanceValue;
  direction?: "up" | "down" | "flat";
};

export type SourceContext = {
  sourceLabel?: string;
  sourceDate?: string;
  period?: string;
  sampleData?: boolean;
};

export type FinanceRenderContext = SourceContext & {
  theme?: ThemeConfig;
  brand?: FinanceBrand;
};

export type FlowNode = {
  id: string;
  label: string;
  value?: FinanceValue;
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
