/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        mentra: {
          light: '#FDFCFB',
          soft: '#F3EFE0',
          sage: '#A7BEAE',
          clay: '#E7E2CC',
          warm: '#F2D0A9',
          rose: '#F1E3E4',
          text: '#2D2D2D',
        }
      }
    },
  },
  plugins: [],
}
