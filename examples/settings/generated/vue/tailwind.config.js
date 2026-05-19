/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,vue}'],
  theme:   {
    extend: {
      colors: {
        primary: '#E11D48',
        surface: '#F1F5F9',
        on_surface: '#0F172A',
        background: '#FFFFFF',
      },
    },
  },
  plugins: [],
};
