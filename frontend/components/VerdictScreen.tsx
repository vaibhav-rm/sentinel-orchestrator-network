import React from "react";
import { motion } from "framer-motion";
import { ShieldCheck, ShieldAlert, FileText, RefreshCw } from "lucide-react";
import { Button } from "./ui/Button";
import { Card } from "./ui/Card";

interface VerdictScreenProps {
    status: "SAFE" | "DANGER";
    onReset: () => void;
    onViewProof: () => void;
}

export const VerdictScreen: React.FC<VerdictScreenProps> = ({ status, onReset, onViewProof }) => {
    const isSafe = status === "SAFE";

    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-obsidian-core/90 backdrop-blur-md p-4"
        >
            <Card className={`w-full max-w-2xl border-2 ${isSafe ? "border-electric-cyan" : "border-red-500"} relative overflow-hidden`}>
                {/* Background Glow */}
                <div className={`absolute inset-0 opacity-20 ${isSafe ? "bg-electric-cyan" : "bg-red-600"} blur-3xl`} />

                <div className="relative z-10 flex flex-col items-center text-center space-y-8 py-8">
                    <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ type: "spring", stiffness: 200, damping: 15 }}
                        className={`p-6 rounded-full ${isSafe ? "bg-electric-cyan/20" : "bg-red-500/20"}`}
                    >
                        {isSafe ? (
                            <ShieldCheck className="w-24 h-24 text-electric-cyan" />
                        ) : (
                            <ShieldAlert className="w-24 h-24 text-red-500 animate-pulse" />
                        )}
                    </motion.div>

                    <div className="space-y-2">
                        <h2 className={`text-4xl font-orbitron font-bold ${isSafe ? "text-electric-cyan" : "text-red-500"}`}>
                            {isSafe ? "TRANSACTION VERIFIED" : "GOVERNANCE SPLIT DETECTED"}
                        </h2>
                        <p className="text-ghost-white/80 text-lg max-w-md mx-auto">
                            {isSafe
                                ? "Canonical chain confirmed. Protocol V3 compliant. Safe to sign."
                                : "Your node is on a ghost chain. Threat type: Replay Attack Vector."}
                        </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full max-w-md">
                        <div className="bg-void-gray/50 p-4 rounded-lg border border-white/5">
                            <div className="text-xs text-white/40 uppercase tracking-wider mb-1">Consensus</div>
                            <div className={`font-mono font-bold ${isSafe ? "text-green-400" : "text-red-400"}`}>
                                {isSafe ? "Mainnet (99.2%)" : "Minority Fork (30%)"}
                            </div>
                        </div>
                        <div className="bg-void-gray/50 p-4 rounded-lg border border-white/5">
                            <div className="text-xs text-white/40 uppercase tracking-wider mb-1">Risk Level</div>
                            <div className={`font-mono font-bold ${isSafe ? "text-green-400" : "text-red-500"}`}>
                                {isSafe ? "LOW" : "CRITICAL"}
                            </div>
                        </div>
                    </div>

                    <div className="flex gap-4 pt-4">
                        <Button variant={isSafe ? "primary" : "secondary"} onClick={onViewProof}>
                            <FileText className="w-4 h-4 mr-2" />
                            View Proof
                        </Button>
                        <Button variant={isSafe ? "secondary" : "primary"} onClick={onReset}>
                            <RefreshCw className="w-4 h-4 mr-2" />
                            {isSafe ? "New Scan" : "Switch Node"}
                        </Button>
                    </div>
                </div>
            </Card>
        </motion.div>
    );
};
