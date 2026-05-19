/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,vue}'],
  theme:   {
    extend: {
      colors: {
        primary: '#0EA5E9',
        surface: '#FFFFFF',
        on_surface: '#0F172A',
        background: '#FFFFFF',
      },
    },
  },
  plugins: [],
};
