"use client";

import { motion, AnimatePresence } from "framer-motion";
import { usePathname } from "next/navigation";
import { ReactNode } from "react";

export const PageTransition = ({ children }: { children: ReactNode }) => {
    const pathname = usePathname();

    return (
        <AnimatePresence mode="wait">
            <motion.div
                key={pathname}
                initial={{ opacity: 0, filter: "blur(10px)" }}
                animate={{ opacity: 1, filter: "blur(0px)" }}
                exit={{ opacity: 0, filter: "blur(10px)" }}
                transition={{ duration: 0.5, ease: "easeInOut" }}
                className="w-full"
            >
                {children}

                {/* Cyber Shutter Effect */}
                <motion.div
                    className="fixed inset-0 bg-neon-orchid/10 z-[100] pointer-events-none"
                    initial={{ scaleY: 1 }}
                    animate={{ scaleY: 0 }}
                    exit={{ scaleY: 1 }}
                    transition={{ duration: 0.5, ease: "circInOut" }}
                    style={{ originY: 0 }}
                />
            </motion.div>
        </AnimatePresence>
    );
};
