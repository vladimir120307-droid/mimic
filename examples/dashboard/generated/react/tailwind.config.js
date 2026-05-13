/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
  theme:   {
    extend: {
      colors: {
        primary: '#6E56CF',
        surface: '#FFFFFF',
        on_surface: '#0F172A',
        background: '#FFFFFF',
      },
    },
  },
  plugins: [],
};
