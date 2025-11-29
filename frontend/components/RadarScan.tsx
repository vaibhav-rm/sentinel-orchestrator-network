import React from "react";
import { motion } from "framer-motion";

export const RadarScan = () => {
    return (
        <div className="relative w-full h-full flex items-center justify-center overflow-hidden rounded-full bg-obsidian-core/50 border border-electric-cyan/30">
            {/* Grid Lines */}
            <div className="absolute inset-0 bg-[linear-gradient(rgba(0,245,255,0.1)_1px,transparent_1px),linear-gradient(90deg,rgba(0,245,255,0.1)_1px,transparent_1px)] bg-[size:20px_20px]" />

            {/* Concentric Circles */}
            <div className="absolute inset-0 border border-electric-cyan/20 rounded-full scale-50" />
            <div className="absolute inset-0 border border-electric-cyan/20 rounded-full scale-75" />

            {/* Scanning Beam */}
            <div className="absolute inset-0 animate-radar-sweep origin-center">
                <div className="w-1/2 h-full bg-gradient-to-l from-electric-cyan/40 to-transparent blur-sm" />
            </div>

            {/* Blips */}
            <motion.div
                className="absolute w-2 h-2 bg-neon-orchid rounded-full shadow-[0_0_8px_#FF006E]"
                animate={{ opacity: [0, 1, 0], scale: [0.5, 1.5, 0.5] }}
                transition={{ duration: 2, repeat: Infinity, delay: 0.5 }}
                style={{ top: "30%", left: "60%" }}
            />
            <motion.div
                className="absolute w-2 h-2 bg-amber-warning rounded-full shadow-[0_0_8px_#FFB627]"
                animate={{ opacity: [0, 1, 0], scale: [0.5, 1.5, 0.5] }}
                transition={{ duration: 3, repeat: Infinity, delay: 1.2 }}
                style={{ top: "70%", left: "40%" }}
            />
        </div>
    );
};
