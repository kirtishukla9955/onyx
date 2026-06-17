/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        void: {
          DEFAULT: '#050608',
          deep: '#030405',
          panel: '#0A0C10',
          card: '#0D1014',
          border: '#1A1F26'
        },
        cyan: {
          glow: '#00F0FF',
          dim: '#0891A8',
          soft: 'rgba(0, 240, 255, 0.12)'
        },
        violet: {
          glow: '#7B5CFF',
          dim: '#4C36A8',
          soft: 'rgba(123, 92, 255, 0.12)'
        },
        alert: {
          red: '#FF3B5C',
          soft: 'rgba(255, 59, 92, 0.12)'
        },
        ink: {
          DEFAULT: '#E8EDF2',
          dim: '#8A93A3',
          faint: '#4A5160'
        }
      },
      fontFamily: {
        display: ['"Chakra Petch"', 'sans-serif'],
        body: ['"Inter"', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace']
      },
      animation: {
        'glitch': 'glitch 0.4s steps(2) infinite',
        'scan': 'scan 3s linear infinite',
        'pulse-ring': 'pulse-ring 2.4s cubic-bezier(0.4,0,0.6,1) infinite',
        'float-slow': 'float-slow 8s ease-in-out infinite',
        'flicker': 'flicker 3s linear infinite',
        'marquee': 'marquee 30s linear infinite'
      },
      keyframes: {
        glitch: {
          '0%, 100%': { transform: 'translate(0,0)' },
          '50%': { transform: 'translate(-1px, 1px)' }
        },
        scan: {
          '0%': { transform: 'translateY(-100%)' },
          '100%': { transform: 'translateY(100%)' }
        },
        'pulse-ring': {
          '0%': { boxShadow: '0 0 0 0 rgba(0,240,255,0.5)' },
          '70%': { boxShadow: '0 0 0 14px rgba(0,240,255,0)' },
          '100%': { boxShadow: '0 0 0 0 rgba(0,240,255,0)' }
        },
        'float-slow': {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-12px)' }
        },
        flicker: {
          '0%, 100%': { opacity: 1 },
          '92%': { opacity: 1 },
          '93%': { opacity: 0.4 },
          '94%': { opacity: 1 }
        },
        marquee: {
          '0%': { transform: 'translateX(0)' },
          '100%': { transform: 'translateX(-50%)' }
        }
      }
    },
  },
  plugins: [],
}
