'use client';
import { motion, HTMLMotionProps } from 'framer-motion';
import { ReactNode } from 'react';

interface GlowCardProps extends HTMLMotionProps<'div'> {
  children: ReactNode;
  className?: string;
  glowColor?: 'purple' | 'blue' | 'cyan' | 'pink';
  delay?: number;
}

const glowMap = {
  purple: 'rgba(168,85,247,0.4)',
  blue: 'rgba(96,165,250,0.4)',
  cyan: 'rgba(34,211,238,0.4)',
  pink: 'rgba(244,114,182,0.4)',
};

export default function GlowCard({ children, className = '', glowColor = 'purple', delay = 0, ...rest }: GlowCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 24 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay, ease: 'easeOut' }}
      whileHover={{
        scale: 1.02,
        boxShadow: `0 0 30px ${glowMap[glowColor]}, 0 0 60px ${glowMap[glowColor]}40`,
      }}
      className={`glass-card ${className}`}
      {...rest}
    >
      {children}
    </motion.div>
  );
}
