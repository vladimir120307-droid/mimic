/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
  theme:   {
    extend: {
      colors: {
        primary: '#10B981',
        surface: '#FFFFFF',
        on_surface: '#0F172A',
        background: '#64748B',
      },
    },
  },
  plugins: [],
};
