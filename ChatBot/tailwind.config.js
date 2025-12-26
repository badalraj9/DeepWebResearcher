/** @type {import('tailwindcss').Config} */
export default {
    darkMode: ["class"],
    content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
	extend: {
		colors: {
            "primary": "#06e8f9", // Bioluminescent Cyan
            "secondary": "#ff00d4", // Plasma Pink
            "alchemy": "#ffd700", // Alchemical Gold
            "plasma": "#ff00cc", // Alias for secondary in some contexts
            "gold": "#ffd700",   // Alias for alchemy
            "background-light": "#f5f8f8",
            "background-dark": "#050a14", // Deep void blue/black
            "void": "#050608",
            "glass-surface": "rgba(16, 34, 35, 0.4)",
            "glass-border": "rgba(6, 232, 249, 0.2)",
            "card-surface": "rgba(20, 40, 50, 0.3)",
			sidebar: {
				DEFAULT: 'hsl(var(--sidebar-background))',
				foreground: 'hsl(var(--sidebar-foreground))',
				primary: 'hsl(var(--sidebar-primary))',
				'primary-foreground': 'hsl(var(--sidebar-primary-foreground))',
				accent: 'hsl(var(--sidebar-accent))',
				'accent-foreground': 'hsl(var(--sidebar-accent-foreground))',
				border: 'hsl(var(--sidebar-border))',
				ring: 'hsl(var(--sidebar-ring))'
			}
		},
        fontFamily: {
            "display": ["Space Grotesk", "sans-serif"],
            "body": ["Noto Sans", "sans-serif"],
            "sans": ["Inter", "sans-serif"],
        },
		borderRadius: {
			lg: 'var(--radius)',
			md: 'calc(var(--radius) - 2px)',
			sm: 'calc(var(--radius) - 4px)'
		},
        boxShadow: {
            "neon": "0 0 20px rgba(6, 232, 249, 0.3), 0 0 60px rgba(6, 232, 249, 0.1)",
            "neon-strong": "0 0 50px rgba(6, 232, 249, 0.4), 0 0 100px rgba(6, 232, 249, 0.2)",
            "alchemy-glow": "0 0 25px rgba(255, 215, 0, 0.3)",
            "void-glow": "0 0 100px rgba(6, 232, 249, 0.15)",
            "glass": "0 8px 32px 0 rgba(0, 0, 0, 0.37)",
        },
        backgroundImage: {
            'void-gradient': 'radial-gradient(circle at 50% 50%, #0d1b2a 0%, #050a14 60%, #000000 100%)',
            'spark-gradient': 'radial-gradient(circle, rgba(255,255,255,0.8) 0%, rgba(6,232,249,0.5) 30%, transparent 70%)',
            'nebula': "radial-gradient(circle at center, #1e293b 0%, #0f172a 40%, #020617 100%)",
            'glass': "linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.01) 100%)",
            'card-gradient': 'linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.01) 100%)',
        },
        animation: {
            'spin-slow': 'spin 60s linear infinite',
            'spin-reverse-slow': 'spin 40s linear infinite reverse',
            'float': 'float 25s infinite ease-in-out',
        },
        keyframes: {
            float: {
                '0%, 100%': { transform: 'translate(0, 0)' },
                '50%': { transform: 'translate(-30px, 30px)' },
            }
        }
	}
  },
  plugins: [require("tailwindcss-animate"), require("@tailwindcss/typography")],
}
