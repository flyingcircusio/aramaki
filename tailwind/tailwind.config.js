/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["../src/**/*.{pt,html}",],
  theme: {
    fontFamily: {
      'sans': ['Fira Sans', 'ui-sans-serif', 'system-ui']
    },
    extend: {
      colors: {
        "fc-green": {
          300: "#badbc4",
          400: "#a9d2b6",
          500: "#75b689",
          DEFAULT: '#52a46c',
          600: '#52a46c'
        },
        "fc-midnight": {
          500: "#99a9bb",
          600: "#667e99",
          800: "#335377",
          DEFAULT: '#002855',
          950: '#002855'
        },
        "fc-cab": {
          100: "#ffeb98",
          200: "#ffe26f",
          DEFAULT: "#ffd631",
          300: "#ffd631"
        },
        "fc-purple": {
          400: "#b4acd1",
          500: "#867ab5",
          DEFAULT: "#6859A3",
          600: "#6859A3"
        },
        "fc-blue-gray": {
          200: "#f2f5f8",
          300: "#eef1f5",
          400: "#e6eaf1",
          500: "#dde3ec",
          DEFAULT: "#d5dce7",
          600: "#d5dce7",
          700: "#aab0b9",
          800: "#80848b",
          900: "#55585c",
          950: "#151617",
        },
        "fc-danger": {
          400: "#ed9096",
          500: "#e5646b",
          DEFAULT: "#da212c",
          600: "#da212c",
        },
        "fc-warning": {
          400: "#ffd199",
          500: "#ffae4d",
          DEFAULT: "#ff8b00",
          600: "#ff8b00",
        },
        "fc-info": {
          400: "#99c1da",
          500: "#4d92bf",
          DEFAULT: "#0063a3",
          600: "#0063a3",
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    // ...
  ],
}

