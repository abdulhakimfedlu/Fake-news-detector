/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#3b82f6',  // Blue for buttons
        accent: '#10b981',   // Green for real
        danger: '#ef4444',   // Red for fake
      },
    },
  },
  plugins: [],
}