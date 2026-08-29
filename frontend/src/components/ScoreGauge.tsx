import React from "react";
import { PieChart, Pie, Cell } from "recharts";

interface ScoreGaugeProps {
  score: number;
  riskLevel: string;
}

export const ScoreGauge: React.FC<ScoreGaugeProps> = ({ score, riskLevel }) => {
  const data = [
    { name: "Score", value: score },
    { name: "Remaining", value: 100 - score },
  ];

  let color = "#22c55e"; // green
  if (score < 50) color = "#ef4444"; // red
  else if (score < 80) color = "#eab308"; // yellow

  return (
    <div className="flex flex-col items-center justify-center relative w-48 h-48 mx-auto">
      <PieChart width={200} height={200}>
        <Pie
          data={data}
          cx={100}
          cy={100}
          startAngle={180}
          endAngle={0}
          innerRadius={70}
          outerRadius={90}
          paddingAngle={0}
          dataKey="value"
          stroke="none"
        >
          <Cell fill={color} />
          <Cell fill="#e5e7eb" />
        </Pie>
      </PieChart>
      <div className="absolute flex flex-col items-center justify-center top-20">
        <span className="text-4xl font-bold" style={{ color }}>{score}</span>
        <span className="text-sm font-medium text-gray-500">{riskLevel} Risk</span>
      </div>
    </div>
  );
};
