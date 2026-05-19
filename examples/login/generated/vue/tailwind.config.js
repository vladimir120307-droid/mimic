/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,vue}'],
  theme:   {
    extend: {
      colors: {
        primary: '#6E56CF',
        surface: '#F8FAFC',
        on_surface: '#0F172A',
        background: '#F8FAFC',
      },
    },
  },
  plugins: [],
};
