import React, { useEffect, useState } from "react";

const CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&";

interface ScrambleTextProps {
    text: string;
    className?: string;
    delay?: number;
    speed?: number;
    reveal?: boolean;
}

export const ScrambleText: React.FC<ScrambleTextProps> = ({
    text,
    className = "",
    delay = 0,
    speed = 50,
    reveal = true
}) => {
    const [displayText, setDisplayText] = useState("");
    const [isScrambling, setIsScrambling] = useState(false);

    useEffect(() => {
        if (!reveal) return;

        const startScramble = () => {
            setIsScrambling(true);
            let iteration = 0;
            const maxIterations = text.length * 3;

            const interval = setInterval(() => {
                setDisplayText(() => {
                    return text
                        .split("")
                        .map((char, index) => {
                            if (index < iteration / 3) {
                                return text[index];
                            }
                            return CHARS[Math.floor(Math.random() * CHARS.length)];
                        })
                        .join("");
                });

                if (iteration >= maxIterations) {
                    clearInterval(interval);
                    setIsScrambling(false);
                    setDisplayText(text);
                }

                iteration += 1;
            }, speed);

            return interval;
        };

        const timer = setTimeout(() => {
            const interval = startScramble();
            return () => clearInterval(interval);
        }, delay);

        return () => clearTimeout(timer);
    }, [text, delay, speed, reveal]);

    return (
        <span className={`${className} ${isScrambling ? "font-mono" : ""}`}>
            {displayText || (reveal ? "" : text)}
        </span>
    );
};
