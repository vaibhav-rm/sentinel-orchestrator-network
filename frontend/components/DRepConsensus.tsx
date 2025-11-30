import React from "react";
import { motion } from "framer-motion";
import { Card } from "./ui/Card";
import { CheckCircle, XCircle, AlertCircle, MinusCircle } from "lucide-react";

interface AgentVote {
    agent: string;
    vote: "YES" | "NO" | "ABSTAIN";
    confidence: number;
    reason: string;
}

interface DRepConsensusProps {
    votes: AgentVote[];
    finalVerdict: "YES" | "NO" | "ABSTAIN";
}

export const DRepConsensus: React.FC<DRepConsensusProps> = ({ votes, finalVerdict }) => {
    const getIcon = (vote: string) => {
        switch (vote) {
            case "YES": return <CheckCircle className="w-5 h-5 text-green-400" />;
            case "NO": return <XCircle className="w-5 h-5 text-red-500" />;
            default: return <MinusCircle className="w-5 h-5 text-yellow-500" />;
        }
    };

    const getColor = (vote: string) => {
        switch (vote) {
            case "YES": return "text-green-400 border-green-400/30 bg-green-400/10";
            case "NO": return "text-red-500 border-red-500/30 bg-red-500/10";
            default: return "text-yellow-500 border-yellow-500/30 bg-yellow-500/10";
        }
    };

    return (
        <div className="space-y-6">
            {/* Individual Agent Votes */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {votes.map((vote, idx) => (
                    <motion.div
                        key={vote.agent}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: idx * 0.1 }}
                    >
                        <Card className={`p-4 border backdrop-blur-sm ${getColor(vote.vote)}`}>
                            <div className="flex justify-between items-start mb-2">
                                <span className="font-mono text-xs font-bold tracking-wider opacity-80">{vote.agent}</span>
                                {getIcon(vote.vote)}
                            </div>
                            <div className="text-lg font-orbitron font-bold mb-1">{vote.vote}</div>
                            <div className="text-[10px] opacity-70 font-mono leading-tight">{vote.reason}</div>
                            <div className="mt-2 w-full bg-black/20 h-1 rounded-full overflow-hidden">
                                <motion.div
                                    className="h-full bg-current opacity-50"
                                    initial={{ width: 0 }}
                                    animate={{ width: `${vote.confidence * 100}%` }}
                                    transition={{ delay: 0.5 + idx * 0.1, duration: 1 }}
                                />
                            </div>
                        </Card>
                    </motion.div>
                ))}
            </div>

            {/* Final Consensus Line */}
            <motion.div
                initial={{ scaleX: 0 }}
                animate={{ scaleX: 1 }}
                transition={{ delay: 0.8, duration: 0.5 }}
                className="h-px bg-gradient-to-r from-transparent via-white/20 to-transparent w-full"
            />

            {/* Final Verdict */}
            <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 1 }}
                className="text-center"
            >
                <div className="text-xs text-white/50 font-mono tracking-[0.3em] mb-2">DREP CONSENSUS REACHED</div>
                <div className={`text-4xl md:text-5xl font-orbitron font-black tracking-wider ${finalVerdict === "YES" ? "text-green-400 drop-shadow-[0_0_15px_rgba(74,222,128,0.5)]" :
                        finalVerdict === "NO" ? "text-red-500 drop-shadow-[0_0_15px_rgba(239,68,68,0.5)]" :
                            "text-yellow-500 drop-shadow-[0_0_15px_rgba(234,179,8,0.5)]"
                    }`}>
                    {finalVerdict}
                </div>
            </motion.div>
        </div>
    );
};
