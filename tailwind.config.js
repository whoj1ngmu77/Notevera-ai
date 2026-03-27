/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './context/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        mono: ['Fira Code', 'monospace'],
      },
      colors: {
        cosmic: {
          50: '#f0e8ff',
          100: '#d8c4ff',
          200: '#b896ff',
          300: '#9866ff',
          400: '#7c43fc',
          500: '#6020e8',
          600: '#4a10c5',
          700: '#3608a0',
          800: '#240378',
          900: '#14024f',
        },
        nebula: {
          50: '#e8f4ff',
          100: '#c0dcff',
          200: '#8abeff',
          300: '#5298ff',
          400: '#2176ff',
          500: '#0055e0',
          600: '#0041b5',
          700: '#002f88',
          800: '#001e5a',
          900: '#000f30',
        },
        neon: {
          purple: '#a855f7',
          blue: '#60a5fa',
          cyan: '#22d3ee',
          pink: '#f472b6',
          green: '#4ade80',
        },
      },
      backgroundImage: {
        'galaxy': 'radial-gradient(ellipse at top, #1a0533 0%, #0a0118 50%, #000000 100%)',
        'nebula-gradient': 'linear-gradient(135deg, #1a0533 0%, #0d1b4b 50%, #0a0118 100%)',
        'glow-purple': 'radial-gradient(circle, rgba(168,85,247,0.15) 0%, transparent 70%)',
        'glow-blue': 'radial-gradient(circle, rgba(96,165,250,0.15) 0%, transparent 70%)',
        'card-glass': 'linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%)',
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'glow-pulse': 'glowPulse 3s ease-in-out infinite',
        'star-twinkle': 'twinkle 2s ease-in-out infinite',
        'slide-up': 'slideUp 0.5s ease-out',
        'fade-in': 'fadeIn 0.6s ease-out',
        'spin-slow': 'spin 20s linear infinite',
        'shimmer': 'shimmer 2.5s linear infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' },
        },
        glowPulse: {
          '0%, 100%': { boxShadow: '0 0 20px rgba(168,85,247,0.3)' },
          '50%': { boxShadow: '0 0 40px rgba(168,85,247,0.7), 0 0 80px rgba(96,165,250,0.3)' },
        },
        twinkle: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.3' },
        },
        slideUp: {
          '0%': { transform: 'translateY(30px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
      },
      boxShadow: {
        'glow-sm': '0 0 10px rgba(168,85,247,0.4)',
        'glow-md': '0 0 20px rgba(168,85,247,0.5), 0 0 40px rgba(96,165,250,0.2)',
        'glow-lg': '0 0 30px rgba(168,85,247,0.6), 0 0 60px rgba(96,165,250,0.3)',
        'neon-blue': '0 0 20px rgba(96,165,250,0.6)',
        'neon-cyan': '0 0 20px rgba(34,211,238,0.6)',
        'glass': '0 8px 32px rgba(0,0,0,0.4)',
      },
      backdropBlur: {
        xs: '2px',
      },
    },
  },
  plugins: [],
};
