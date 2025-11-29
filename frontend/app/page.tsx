"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { MatrixTerminal } from "@/components/MatrixTerminal";
import { RadarScan } from "@/components/RadarScan";
import { VerdictScreen } from "@/components/VerdictScreen";
import { ThreatProofCard } from "@/components/ThreatProofCard";
import { AgentEconomy } from "@/components/AgentEconomy";
import { Shield, Activity, Globe } from "lucide-react";

// Mock Data
const MOCK_LOGS = [
  { id: "1", agent: "SENTINEL", message: "Analyzing OpCodes... Protocol V3 Compliant.", type: "info", timestamp: Date.now() },
  { id: "2", agent: "SENTINEL", message: "ALERT. Transaction lacks Validity Interval (TTL).", type: "warning", timestamp: Date.now() + 500 },
  { id: "3", agent: "SENTINEL", message: "@ORACLE, I need a Network Fork Check. Offer: 1.0 ADA.", type: "action", timestamp: Date.now() + 1000 },
  { id: "4", agent: "ORACLE", message: "Offer Accepted. Scanning 5 Nodes...", type: "info", timestamp: Date.now() + 2000 },
  { id: "5", agent: "ORACLE", message: "DANGER. User Node is on Minority Fork (30% Weight).", type: "error", timestamp: Date.now() + 3500 },
  { id: "6", agent: "MIDNIGHT", message: "Generating ZK-Proof of Threat...", type: "info", timestamp: Date.now() + 4000 },
  { id: "7", agent: "SENTINEL", message: "TRANSACTION BLOCKED.", type: "error", timestamp: Date.now() + 4500 },
] as const;

interface LogEntry {
  id: string;
  agent: "SENTINEL" | "ORACLE" | "MIDNIGHT";
  message: string;
  type: "info" | "warning" | "error" | "success" | "action";
  timestamp: number;
}

export default function Home() {
  const [scanState, setScanState] = useState<"IDLE" | "SCANNING" | "VERDICT">("IDLE");
  const [verdict] = useState<"SAFE" | "DANGER">("DANGER"); // Default to Danger for demo
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [showProof, setShowProof] = useState(false);

  const startScan = () => {
    setScanState("SCANNING");
    setLogs([]);

    // Simulate log stream
    let delay = 0;
    MOCK_LOGS.forEach((log) => {
      delay += (log.timestamp - MOCK_LOGS[0].timestamp) + Math.random() * 500;
      setTimeout(() => {
        setLogs((prev) => [...prev, { ...log, id: Math.random().toString(), timestamp: Date.now() }]);
      }, delay);
    });

    // Show verdict after logs
    setTimeout(() => {
      setScanState("VERDICT");
    }, delay + 1000);
  };

  const resetScan = () => {
    setScanState("IDLE");
    setLogs([]);
    setShowProof(false);
  };

  return (
    <main className="min-h-screen bg-obsidian-core text-ghost-white overflow-x-hidden relative selection:bg-neon-orchid/30">
      {/* Background Ambience */}
      <div className="fixed inset-0 bg-[radial-gradient(circle_at_50%_0%,#1E2738_0%,#0A0E1A_100%)] -z-20" />
      <div className="fixed inset-0 bg-[url('/grid.svg')] opacity-10 -z-10" />

      <div className="max-w-7xl mx-auto px-4 py-8 md:py-12 space-y-12">
        {/* Header */}
        <header className="flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-neon-orchid rounded-lg flex items-center justify-center shadow-[0_0_20px_rgba(255,0,110,0.5)]">
              <Shield className="text-white w-6 h-6" />
            </div>
            <div>
              <h1 className="font-orbitron font-bold text-2xl tracking-wider">SON</h1>
              <p className="text-xs text-white/50 tracking-[0.2em]">GOVERNANCE GUARD</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
              <span className="text-xs font-mono">MAINNET: ONLINE</span>
            </div>
          </div>
        </header>

        {/* Hero Section */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 min-h-[600px]">
          {/* Left Panel: Interaction */}
          <div className="lg:col-span-7 flex flex-col justify-center space-y-8">
            <div className="space-y-4">
              <motion.h2
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="text-5xl md:text-7xl font-orbitron font-black leading-tight bg-clip-text text-transparent bg-gradient-to-r from-white via-ghost-white to-white/50"
              >
                SECURE THE<br />
                <span className="text-neon-orchid drop-shadow-[0_0_15px_rgba(255,0,110,0.5)]">VOLTAIRE ERA</span>
              </motion.h2>
              <p className="text-lg text-white/60 max-w-xl">
                Autonomous agent swarm that detects governance forks, prevents replay attacks, and verifies consensus in real-time.
              </p>
            </div>

            <Card className="p-1 space-y-4 bg-white/5 border-white/10 backdrop-blur-sm">
              <div className="p-6 space-y-6">
                <div className="space-y-2">
                  <label className="text-xs font-mono text-electric-cyan uppercase tracking-wider">Transaction CBOR / Policy ID</label>
                  <div className="relative group">
                    <textarea
                      className="w-full h-32 bg-black/50 border border-white/10 rounded-lg p-4 font-mono text-sm text-white/80 focus:outline-none focus:border-neon-orchid/50 transition-colors resize-none"
                      placeholder="84a30081825820..."
                      disabled={scanState !== "IDLE"}
                    />
                    <div className="absolute inset-0 border border-neon-orchid/0 group-hover:border-neon-orchid/20 pointer-events-none rounded-lg transition-colors" />
                  </div>
                </div>

                <Button
                  className="w-full h-16 text-lg"
                  onClick={startScan}
                  disabled={scanState !== "IDLE"}
                  isLoading={scanState === "SCANNING"}
                >
                  {scanState === "IDLE" ? "INITIATE GOVERNANCE SCAN" : "SCANNING NETWORK..."}
                </Button>
              </div>
            </Card>
          </div>

          {/* Right Panel: Visualization */}
          <div className="lg:col-span-5 flex flex-col gap-6">
            {/* Status Cards */}
            <div className="grid grid-cols-2 gap-4">
              <Card className="p-4 flex items-center gap-4 bg-electric-cyan/5 border-electric-cyan/20">
                <div className="p-3 rounded-full bg-electric-cyan/10">
                  <Globe className="w-6 h-6 text-electric-cyan" />
                </div>
                <div>
                  <div className="text-2xl font-orbitron font-bold">98.7%</div>
                  <div className="text-xs text-white/50">Consensus Health</div>
                </div>
              </Card>
              <Card className="p-4 flex items-center gap-4 bg-plasma-pink/5 border-plasma-pink/20">
                <div className="p-3 rounded-full bg-plasma-pink/10">
                  <Activity className="w-6 h-6 text-plasma-pink" />
                </div>
                <div>
                  <div className="text-2xl font-orbitron font-bold">1,247</div>
                  <div className="text-xs text-white/50">Active Agents</div>
                </div>
              </Card>
            </div>

            {/* Dynamic Content Area */}
            <div className="flex-1 relative min-h-[400px]">
              <AnimatePresence mode="wait">
                {scanState === "IDLE" ? (
                  <motion.div
                    key="radar"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="h-full"
                  >
                    <RadarScan />
                  </motion.div>
                ) : (
                  <motion.div
                    key="terminal"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    className="h-full"
                  >
                    <MatrixTerminal logs={logs} isActive={true} />
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

            {/* Agent Economy Mini-Vis */}
            <AgentEconomy />
          </div>
        </div>
      </div>

      {/* Overlays */}
      <AnimatePresence>
        {scanState === "VERDICT" && !showProof && (
          <VerdictScreen
            status={verdict}
            onReset={resetScan}
            onViewProof={() => setShowProof(true)}
          />
        )}
        {showProof && (
          <ThreatProofCard
            verdict={verdict}
            onClose={() => setShowProof(false)}
          />
        )}
      </AnimatePresence>
    </main>
  );
}
