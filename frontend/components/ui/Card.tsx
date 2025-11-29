import React from "react";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
}

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
    variant?: "default" | "glass";
}

export const Card = React.forwardRef<HTMLDivElement, CardProps>(
    ({ className, variant = "glass", children, ...props }, ref) => {
        return (
            <div
                ref={ref}
                className={cn(
                    "rounded-2xl p-6 transition-all duration-300",
                    variant === "glass" &&
                    "bg-gradient-to-br from-void-gray/80 to-obsidian-core/90 border border-neon-orchid/20 backdrop-blur-xl shadow-[0_4px_16px_rgba(0,0,0,0.3),inset_0_1px_0_rgba(255,255,255,0.05)]",
                    className
                )}
                {...props}
            >
                {children}
            </div>
        );
    }
);
Card.displayName = "Card";
