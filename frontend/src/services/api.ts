export interface AnalysisResult {
  repo_meta: {
    name: string;
    owner: string;
    stars: number;
    forks: number;
    open_issues: number;
    language: string | null;
  };
  analyzed_commits: number;
  metrics: {
    code_churn: any;
    commit_hygiene: any;
    cadence: any;
    author_distribution: any;
    anomaly_risk: any;
  };
  anomaly_flags: string[];
  health_score: number;
  risk_level: string;
  executive_report: string;
}

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const analyzeRepo = async (repoUrl: string): Promise<AnalysisResult> => {
  const response = await fetch(`${API_URL}/api/analyze`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ repo_url: repoUrl }),
  });

  if (!response.ok) {
    let errorMsg = "An error occurred";
    try {
      const data = await response.json();
      errorMsg = data.detail || errorMsg;
    } catch (e) {
      errorMsg = response.statusText;
    }
    throw new Error(errorMsg);
  }

  return response.json();
};
