import React, { useState } from "react";
import { Search, AlertTriangle, GitBranch, Activity, Users, GitCommit, FileWarning } from "lucide-react";
import { analyzeRepo, type AnalysisResult } from "../services/api";
import { ScoreGauge } from "./ScoreGauge";
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from "recharts";

export const Dashboard = () => {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AnalysisResult | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!url) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await analyzeRepo(url);
      setResult(data);
    } catch (err: any) {
      setError(err.message || "Failed to analyze repository");
    } finally {
      setLoading(false);
    }
  };

  const radarData = result ? [
    { subject: "Churn", A: result.metrics.code_churn.score, fullMark: 20 },
    { subject: "Hygiene", A: result.metrics.commit_hygiene.score, fullMark: 25 },
    { subject: "Cadence", A: result.metrics.cadence.score, fullMark: 15 },
    { subject: "Entropy", A: result.metrics.author_distribution.score, fullMark: 20 },
    { subject: "Stability", A: result.metrics.anomaly_risk.score, fullMark: 20 },
  ] : [];

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 p-8 font-sans">
      <div className="max-w-6xl mx-auto">
        <header className="mb-12 text-center">
          <h1 className="text-4xl font-extrabold flex items-center justify-center gap-3 mb-4">
            <Activity className="w-10 h-10 text-blue-600" />
            RepoPulse Lite
          </h1>
          <p className="text-lg text-gray-600">Deterministic GitHub Repository Health & Risk Analysis</p>
        </header>

        <form onSubmit={handleSearch} className="max-w-2xl mx-auto mb-12 relative">
          <input
            type="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://github.com/owner/repository"
            className="w-full px-6 py-4 rounded-xl shadow-md border-transparent focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none text-lg pr-32"
            required
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading}
            className="absolute right-2 top-2 bottom-2 px-6 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg flex items-center gap-2 transition-colors disabled:opacity-50"
          >
            {loading ? "Analyzing..." : <><Search className="w-5 h-5" /> Analyze</>}
          </button>
        </form>

        {error && (
          <div className="max-w-2xl mx-auto mb-8 p-4 bg-red-50 text-red-700 rounded-lg flex items-start gap-3 border border-red-200">
            <AlertTriangle className="w-6 h-6 shrink-0" />
            <p>{error}</p>
          </div>
        )}

        {loading && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 animate-pulse">
            <div className="h-64 bg-gray-200 rounded-2xl col-span-1 md:col-span-2"></div>
            <div className="h-64 bg-gray-200 rounded-2xl"></div>
            <div className="h-48 bg-gray-200 rounded-2xl"></div>
            <div className="h-48 bg-gray-200 rounded-2xl"></div>
            <div className="h-48 bg-gray-200 rounded-2xl"></div>
          </div>
        )}

        {result && !loading && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              
              {/* Overview Card */}
              <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 lg:col-span-2 flex flex-col justify-between">
                <div>
                  <div className="flex items-center gap-3 mb-2">
                    <GitBranch className="w-8 h-8 text-gray-700" />
                    <h2 className="text-2xl font-bold">{result.repo_meta.owner} / {result.repo_meta.name}</h2>
                  </div>
                  <div className="flex gap-4 text-sm text-gray-500 mb-6">
                    <span className="flex items-center gap-1">⭐ {result.repo_meta.stars} stars</span>
                    <span className="flex items-center gap-1">🍴 {result.repo_meta.forks} forks</span>
                    <span className="flex items-center gap-1">⭕ {result.repo_meta.open_issues} issues</span>
                    {result.repo_meta.language && <span className="flex items-center gap-1">📝 {result.repo_meta.language}</span>}
                  </div>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6 border-t pt-6 border-gray-100">
                  <div className="text-center">
                    <p className="text-sm text-gray-500">Commits Analyzed</p>
                    <p className="text-xl font-semibold flex items-center justify-center gap-2"><GitCommit className="w-4 h-4 text-gray-400"/>{result.analyzed_commits}</p>
                  </div>
                  <div className="text-center">
                    <p className="text-sm text-gray-500">Contributors</p>
                    <p className="text-xl font-semibold flex items-center justify-center gap-2"><Users className="w-4 h-4 text-gray-400"/>{result.metrics.author_distribution.contributor_count}</p>
                  </div>
                  <div className="text-center">
                    <p className="text-sm text-gray-500">Additions</p>
                    <p className="text-xl font-semibold text-green-600">+{result.metrics.code_churn.additions}</p>
                  </div>
                  <div className="text-center">
                    <p className="text-sm text-gray-500">Deletions</p>
                    <p className="text-xl font-semibold text-red-600">-{result.metrics.code_churn.deletions}</p>
                  </div>
                </div>
              </div>

              {/* Score Card */}
              <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 flex flex-col items-center justify-center">
                <h3 className="text-lg font-semibold mb-4 text-center">Overall Health</h3>
                <ScoreGauge score={result.health_score} riskLevel={result.risk_level} />
              </div>

            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              
              {/* Radar Chart */}
              <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
                <h3 className="text-lg font-semibold mb-4">Dimension Breakdown</h3>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <RadarChart cx="50%" cy="50%" outerRadius="70%" data={radarData}>
                      <PolarGrid />
                      <PolarAngleAxis dataKey="subject" textAnchor="middle" />
                      <PolarRadiusAxis angle={30} domain={[0, 25]} tick={false} />
                      <Radar name="Score" dataKey="A" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.5} />
                    </RadarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* LLM Report */}
              <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 lg:col-span-2">
                <h3 className="text-lg font-semibold mb-4">Executive Summary</h3>
                <div className="prose prose-sm max-w-none text-gray-700 whitespace-pre-wrap">
                  {result.executive_report}
                </div>
              </div>

            </div>

            {/* Anomalies */}
            {result.anomaly_flags.length > 0 && (
              <div className="bg-red-50 rounded-2xl p-6 border border-red-100">
                <h3 className="text-lg font-semibold mb-4 text-red-900 flex items-center gap-2">
                  <FileWarning className="w-5 h-5" /> Risk Flags Detected
                </h3>
                <ul className="list-disc pl-5 space-y-2 text-red-800">
                  {result.anomaly_flags.map((flag, idx) => (
                    <li key={idx}>{flag}</li>
                  ))}
                </ul>
              </div>
            )}

          </div>
        )}
      </div>
    </div>
  );
};
