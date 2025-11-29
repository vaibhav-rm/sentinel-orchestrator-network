import React from "react";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
import { motion, HTMLMotionProps } from "framer-motion";

function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
}

interface ButtonProps extends HTMLMotionProps<"button"> {
    variant?: "primary" | "secondary" | "danger";
    isLoading?: boolean;
    children?: React.ReactNode;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
    ({ className, variant = "primary", isLoading, children, ...props }, ref) => {
        const variants = {
            primary:
                "bg-gradient-to-br from-neon-orchid to-plasma-pink text-white shadow-[0_8px_24px_rgba(255,0,110,0.4)] hover:shadow-[0_12px_32px_rgba(255,0,110,0.6)] border-none",
            secondary:
                "bg-transparent border-2 border-electric-cyan text-electric-cyan shadow-[0_0_12px_rgba(0,245,255,0.2)] hover:bg-electric-cyan/10",
            danger:
                "bg-red-600 text-white shadow-[0_8px_24px_rgba(220,38,38,0.4)] hover:shadow-[0_12px_32px_rgba(220,38,38,0.6)] border-none",
        };

        return (
            <motion.button
                ref={ref}
                whileHover={{ scale: 1.02, translateY: -2 }}
                whileTap={{ scale: 0.98 }}
                className={cn(
                    "relative px-8 py-4 rounded-lg font-space font-semibold uppercase tracking-widest transition-all duration-300 flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed",
                    variants[variant],
                    className
                )}
                disabled={isLoading || props.disabled}
                {...props}
            >
                {isLoading && (
                    <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                )}
                {children}
            </motion.button>
        );
    }
);
Button.displayName = "Button";
