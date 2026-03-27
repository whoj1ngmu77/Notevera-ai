'use client';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { RiSparklingLine, RiMenu3Line } from 'react-icons/ri';
import { useAuth } from '@/context/AuthContext';
import { useState } from 'react';

export default function Navbar() {
  const { user } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <motion.nav
      initial={{ y: -80, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6, ease: 'easeOut' }}
      className="fixed top-0 left-0 right-0 z-50 px-6 py-4"
      style={{ background: 'rgba(5,0,16,0.7)', backdropFilter: 'blur(20px)', borderBottom: '1px solid rgba(168,85,247,0.1)' }}
    >
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <Link href="/" className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center">
            <RiSparklingLine className="text-white" />
          </div>
          <span className="font-orbitron font-bold text-base glow-text">Notevera AI</span>
        </Link>

        <div className="hidden md:flex items-center gap-8 text-sm text-gray-400">
          {['Features', 'How it Works', 'Pricing'].map(item => (
            <a key={item} href={`#${item.toLowerCase().replace(' ', '-')}`}
              className="hover:text-purple-300 transition-colors">{item}</a>
          ))}
        </div>

        <div className="flex items-center gap-3">
          {user ? (
            <Link href="/dashboard">
              <button className="btn-neon text-sm py-2 px-5"><span>Dashboard</span></button>
            </Link>
          ) : (
            <>
              <Link href="/auth" className="text-sm text-gray-400 hover:text-white transition-colors hidden md:block">Sign In</Link>
              <Link href="/auth?mode=signup">
                <button className="btn-neon text-sm py-2 px-5"><span>Get Started</span></button>
              </Link>
            </>
          )}
          <button onClick={() => setMenuOpen(!menuOpen)} className="md:hidden text-gray-400 hover:text-white">
            <RiMenu3Line className="text-xl" />
          </button>
        </div>
      </div>
    </motion.nav>
  );
}
