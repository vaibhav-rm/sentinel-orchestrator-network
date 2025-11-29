import React, { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

interface Node {
    id: string;
    name: string;
    x: string;
    y: string;
    latency: number;
    status: "scanning" | "connected" | "divergent";
}

export const RadarScan = () => {
    const [nodes, setNodes] = useState<Node[]>([]);

    useEffect(() => {
        // Simulate finding nodes over time
        const timeouts = [
            setTimeout(() => setNodes(prev => [...prev, { id: "iog", name: "IOG (Mainnet)", x: "50%", y: "30%", latency: 45, status: "connected" }]), 1000),
            setTimeout(() => setNodes(prev => [...prev, { id: "emurgo", name: "Emurgo", x: "70%", y: "60%", latency: 52, status: "connected" }]), 2000),
            setTimeout(() => setNodes(prev => [...prev, { id: "cf", name: "Cardano Fdn", x: "30%", y: "60%", latency: 48, status: "connected" }]), 2500),
            setTimeout(() => setNodes(prev => [...prev, { id: "user", name: "User Node", x: "50%", y: "50%", latency: 120, status: "divergent" }]), 4000),
        ];

        return () => timeouts.forEach(clearTimeout);
    }, []);

    return (
        <div className="relative w-full h-full flex items-center justify-center overflow-hidden rounded-xl bg-obsidian-core/50 border border-electric-cyan/30">
            {/* Grid Lines */}
            <div className="absolute inset-0 bg-[linear-gradient(rgba(0,245,255,0.1)_1px,transparent_1px),linear-gradient(90deg,rgba(0,245,255,0.1)_1px,transparent_1px)] bg-[size:40px_40px]" />

            {/* Concentric Circles */}
            <div className="absolute inset-0 border border-electric-cyan/20 rounded-full scale-50" />
            <div className="absolute inset-0 border border-electric-cyan/20 rounded-full scale-75" />
            <div className="absolute inset-0 border border-electric-cyan/20 rounded-full scale-90" />

            {/* Scanning Beam */}
            <div className="absolute inset-0 animate-radar-sweep origin-center">
                <div className="w-1/2 h-full bg-gradient-to-l from-electric-cyan/20 to-transparent blur-sm" />
            </div>

            {/* Nodes */}
            <AnimatePresence>
                {nodes.map((node) => (
                    <motion.div
                        key={node.id}
                        initial={{ opacity: 0, scale: 0 }}
                        animate={{ opacity: 1, scale: 1 }}
                        className="absolute flex flex-col items-center"
                        style={{ top: node.y, left: node.x, transform: "translate(-50%, -50%)" }}
                    >
                        <div className={`w-3 h-3 rounded-full shadow-[0_0_10px_currentColor] ${node.status === "divergent" ? "bg-red-500 text-red-500" : "bg-electric-cyan text-electric-cyan"
                            }`} />

                        <motion.div
                            initial={{ opacity: 0, y: 5 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.2 }}
                            className="mt-2 bg-black/80 backdrop-blur px-2 py-1 rounded border border-white/10 text-[10px] font-mono whitespace-nowrap z-10"
                        >
                            <div className={node.status === "divergent" ? "text-red-400" : "text-electric-cyan"}>{node.name}</div>
                            <div className="text-white/50">{node.latency}ms</div>
                        </motion.div>

                        {/* Ping Ripple */}
                        <motion.div
                            className={`absolute inset-0 rounded-full border ${node.status === "divergent" ? "border-red-500" : "border-electric-cyan"
                                }`}
                            initial={{ width: "100%", height: "100%", opacity: 1 }}
                            animate={{ width: "300%", height: "300%", opacity: 0 }}
                            transition={{ duration: 1.5, repeat: Infinity }}
                        />
                    </motion.div>
                ))}
            </AnimatePresence>

            {/* HUD Overlay */}
            <div className="absolute top-4 left-4 text-xs font-mono text-electric-cyan/50">
                <div>NETWORK_MAP_ACTIVE</div>
                <div>NODES_DETECTED: {nodes.length}</div>
            </div>
        </div>
    );
};
