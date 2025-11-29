import React, { useRef } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { Stars } from "@react-three/drei";
import { motion } from "framer-motion";
import * as THREE from "three";

function WarpStars() {
    const ref = useRef<THREE.Group>(null);

    useFrame((state, delta) => {
        if (ref.current) {
            ref.current.rotation.z += delta * 0.1;
            ref.current.position.z += delta * 20; // Move forward
            if (ref.current.position.z > 50) {
                ref.current.position.z = 0;
            }
        }
    });

    return (
        <group ref={ref}>
            <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade speed={2} />
        </group>
    );
}

export const HyperspaceTransition = ({ isActive }: { isActive: boolean }) => {
    if (!isActive) return null;

    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-[100] bg-black pointer-events-none"
        >
            <Canvas camera={{ position: [0, 0, 0], fov: 75 }}>
                <WarpStars />
            </Canvas>
            <motion.div
                initial={{ scaleX: 0 }}
                animate={{ scaleX: 1 }}
                transition={{ duration: 0.2, delay: 1 }}
                className="absolute inset-0 bg-white mix-blend-difference origin-center"
            />
        </motion.div>
    );
};
