'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { motion } from 'framer-motion';
import { useAuth } from '@/context/AuthContext';
import {
  RiDashboardLine, RiUploadCloud2Line, RiFileTextLine,
  RiCalendarLine, RiMicLine, RiUserLine, RiSettings3Line,
  RiSparklingLine, RiLogoutBoxLine,
} from 'react-icons/ri';

const navItems = [
  { href: '/dashboard', icon: RiDashboardLine, label: 'Dashboard' },
  { href: '/upload', icon: RiUploadCloud2Line, label: 'Upload Material' },
  { href: '/notes', icon: RiFileTextLine, label: 'AI Notes' },
  { href: '/planner', icon: RiCalendarLine, label: 'Study Planner' },
  { href: '/oral-exam', icon: RiMicLine, label: 'Oral Exam' },
  { href: '/profile', icon: RiUserLine, label: 'Profile' },
  { href: '/settings', icon: RiSettings3Line, label: 'Settings' },
];

export default function Sidebar() {
  const pathname = usePathname();
  const { user, logout } = useAuth();

  return (
    <aside className="sidebar flex flex-col py-6">
      {/* Logo */}
      <div className="px-6 mb-8">
        <Link href="/dashboard" className="flex items-center gap-3 group">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center shadow-glow-sm">
            <RiSparklingLine className="text-white text-lg" />
          </div>
          <div>
            <p className="font-orbitron font-bold text-sm glow-text">Notevera</p>
            <p className="text-[10px] text-gray-500 -mt-0.5">AI Learning OS</p>
          </div>
        </Link>
      </div>

      {/* Nav Items */}
      <nav className="flex-1 px-3 space-y-1">
        {navItems.map((item, i) => {
          const active = pathname === item.href;
          return (
            <motion.div key={item.href} initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.05 }}>
              <Link
                href={item.href}
                className={`flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 group
                  ${active
                    ? 'bg-gradient-to-r from-purple-500/20 to-blue-500/10 border border-purple-500/30 text-purple-300'
                    : 'text-gray-400 hover:bg-white/5 hover:text-white'
                  }`}
              >
                <item.icon className={`text-lg flex-shrink-0 ${active ? 'text-purple-400' : 'text-gray-500 group-hover:text-purple-400'} transition-colors`} />
                <span>{item.label}</span>
                {active && (
                  <motion.div layoutId="sidebar-indicator" className="ml-auto w-1.5 h-1.5 rounded-full bg-purple-400" />
                )}
              </Link>
            </motion.div>
          );
        })}
      </nav>

      {/* User Footer */}
      <div className="px-4 mt-4 pt-4 border-t border-white/5">
        {user && (
          <div className="flex items-center gap-3 mb-3 px-2">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center text-white text-xs font-bold">
              {user.name?.[0]?.toUpperCase() || 'U'}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-xs font-medium text-white truncate">{user.name}</p>
              <p className="text-[10px] text-gray-500 truncate">{user.email}</p>
            </div>
          </div>
        )}
        <button
          onClick={logout}
          className="w-full flex items-center gap-3 px-4 py-2.5 rounded-xl text-sm text-gray-500 hover:text-red-400 hover:bg-red-500/10 transition-all"
        >
          <RiLogoutBoxLine className="text-lg" />
          Sign Out
        </button>
      </div>
    </aside>
  );
}
