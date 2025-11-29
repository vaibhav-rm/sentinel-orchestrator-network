import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { CheckCircle, AlertTriangle, Shield, Terminal, Activity } from "lucide-react";
import { Card } from "./ui/Card";

interface CheckItem {
    id: string;
    label: string;
    status: "PENDING" | "SCANNING" | "PASS" | "FAIL";
    details?: string;
}

interface ComplianceHUDProps {
    isActive: boolean;
    onComplete?: () => void;
}

export const ComplianceHUD: React.FC<ComplianceHUDProps> = ({ isActive, onComplete }) => {
    const [checks, setChecks] = useState<CheckItem[]>([
        { id: "protocol", label: "Protocol Compliance (V3)", status: "PENDING" },
        { id: "ttl", label: "Validity Interval (TTL)", status: "PENDING" },
        { id: "opcodes", label: "OpCode Analysis", status: "PENDING" },
        { id: "contracts", label: "Contract Parameters", status: "PENDING" },
    ]);

    useEffect(() => {
        if (!isActive) return;

        const runChecks = async () => {
            // Reset
            setChecks(prev => prev.map(c => ({ ...c, status: "PENDING" })));

            // Sequence
            for (let i = 0; i < 4; i++) { // Hardcoded length to avoid dependency
                // Scanning
                setChecks(prev => prev.map((c, idx) => idx === i ? { ...c, status: "SCANNING" } : c));
                await new Promise(r => setTimeout(r, 800)); // Scan duration

                // Result
                setChecks(prev => prev.map((c, idx) => {
                    if (idx === i) {
                        // Simulate failure for TTL (as per narrative)
                        if (c.id === "ttl") return { ...c, status: "FAIL", details: "Missing TTL" };
                        return { ...c, status: "PASS" };
                    }
                    return c;
                }));
                await new Promise(r => setTimeout(r, 200));
            }

            if (onComplete) onComplete();
        };

        runChecks();
    }, [isActive, onComplete]);

    return (
        <Card className="h-full bg-black/60 border-neon-orchid/30 backdrop-blur-xl p-4 flex flex-col relative overflow-hidden">
            {/* Header */}
            <div className="flex items-center justify-between mb-4 border-b border-white/10 pb-2">
                <div className="flex items-center gap-2">
                    <Shield className="w-4 h-4 text-neon-orchid" />
                    <span className="font-orbitron font-bold text-sm tracking-wider text-neon-orchid">COMPLIANCE HUD</span>
                </div>
                <Activity className={`w-4 h-4 ${isActive ? "text-neon-orchid animate-pulse" : "text-white/20"}`} />
            </div>

            {/* Checks List */}
            <div className="space-y-3 flex-1">
                {checks.map((check) => (
                    <div key={check.id} className="relative">
                        <div className="flex items-center justify-between p-2 rounded bg-white/5 border border-white/5">
                            <span className="text-xs font-mono text-white/70">{check.label}</span>

                            {check.status === "PENDING" && <span className="text-xs text-white/20">WAITING</span>}

                            {check.status === "SCANNING" && (
                                <span className="text-xs text-neon-orchid animate-pulse font-mono">SCANNING...</span>
                            )}

                            {check.status === "PASS" && (
                                <motion.div
                                    initial={{ scale: 0 }} animate={{ scale: 1 }}
                                    className="flex items-center gap-1 text-electric-cyan"
                                >
                                    <span className="text-xs font-bold">PASS</span>
                                    <CheckCircle className="w-3 h-3" />
                                </motion.div>
                            )}

                            {check.status === "FAIL" && (
                                <motion.div
                                    initial={{ scale: 0 }} animate={{ scale: 1 }}
                                    className="flex items-center gap-1 text-amber-warning"
                                >
                                    <span className="text-xs font-bold">WARN</span>
                                    <AlertTriangle className="w-3 h-3" />
                                </motion.div>
                            )}
                        </div>

                        {/* Scanning Bar Overlay */}
                        {check.status === "SCANNING" && (
                            <motion.div
                                layoutId="scanbar"
                                className="absolute bottom-0 left-0 h-[1px] bg-neon-orchid shadow-[0_0_10px_#FF006E]"
                                initial={{ width: "0%" }}
                                animate={{ width: "100%" }}
                                transition={{ duration: 0.8, ease: "linear" }}
                            />
                        )}
                    </div>
                ))}
            </div>

            {/* Footer Status */}
            <div className="mt-auto pt-4 border-t border-white/10">
                <div className="flex items-center gap-2 text-[10px] font-mono text-white/40">
                    <Terminal className="w-3 h-3" />
                    <span>SENTINEL_CORE_V3.1.0 ACTIVE</span>
                </div>
            </div>
        </Card>
    );
};
