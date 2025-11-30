import React from "react";
import { motion } from "framer-motion";
import { Card } from "./ui/Card";

interface TreasuryRiskGaugeProps {
    riskScore: number; // 0-100
    label?: string;
}

export const TreasuryRiskGauge: React.FC<TreasuryRiskGaugeProps> = ({ riskScore, label = "RISK SCORE" }) => {
    // Determine color based on risk
    const getColor = (score: number) => {
        if (score < 30) return "#00F5FF"; // Cyan (Low Risk)
        if (score < 70) return "#FFB627"; // Amber (Medium Risk)
        return "#FF006E"; // Pink/Red (High Risk)
    };

    const color = getColor(riskScore);
    const radius = 80;
    const circumference = 2 * Math.PI * radius;
    const strokeDashoffset = circumference - (riskScore / 100) * circumference;

    return (
        <div className="relative flex flex-col items-center justify-center">
            <div className="relative w-48 h-48">
                {/* Background Circle */}
                <svg className="w-full h-full transform -rotate-90">
                    <circle
                        cx="96"
                        cy="96"
                        r={radius}
                        stroke="rgba(255,255,255,0.1)"
                        strokeWidth="12"
                        fill="transparent"
                    />
                    {/* Progress Circle */}
                    <motion.circle
                        cx="96"
                        cy="96"
                        r={radius}
                        stroke={color}
                        strokeWidth="12"
                        fill="transparent"
                        strokeDasharray={circumference}
                        initial={{ strokeDashoffset: circumference }}
                        animate={{ strokeDashoffset }}
                        transition={{ duration: 1.5, ease: "easeOut" }}
                        strokeLinecap="round"
                        className="drop-shadow-[0_0_10px_rgba(0,0,0,0.5)]"
                    />
                </svg>

                {/* Center Content */}
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <motion.div
                        initial={{ scale: 0, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        transition={{ delay: 0.5, type: "spring" }}
                        className="text-4xl font-orbitron font-bold"
                        style={{ color }}
                    >
                        {riskScore.toFixed(0)}
                    </motion.div>
                    <div className="text-[10px] text-white/50 font-mono tracking-widest mt-1">{label}</div>
                </div>
            </div>

            {/* Risk Level Text */}
            <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 1 }}
                className="mt-4 px-4 py-1 rounded-full bg-white/5 border border-white/10 text-xs font-mono tracking-wider"
                style={{ color }}
            >
                {riskScore < 30 ? "LOW RISK" : riskScore < 70 ? "MEDIUM RISK" : "HIGH RISK"}
            </motion.div>
        </div>
    );
};
