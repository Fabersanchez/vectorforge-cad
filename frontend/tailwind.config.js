/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#070a11",
        surface: "#0d1322",
        "surface-border": "#1a243a",
        card: "rgba(15, 23, 42, 0.75)",
        accent: {
          cyan: "#00f0ff",
          purple: "#7000ff",
          pink: "#ff007f",
          emerald: "#00ff9d"
        }
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'glass-gradient': 'linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.01) 100%)',
      },
      boxShadow: {
        'glow-cyan': '0 0 25px rgba(0, 240, 255, 0.25)',
        'glow-purple': '0 0 25px rgba(112, 0, 255, 0.25)',
      }
    },
  },
  plugins: [],
};
