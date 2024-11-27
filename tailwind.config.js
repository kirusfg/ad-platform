/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./templates/**/*.html",
        "./apps/**/templates/**/*.html",
        "./apps/core/templates/**/*.html",
    ],
    theme: {
        extend: {},
    },
    plugins: [require("daisyui")],
    daisyui: {
        themes: ["cupcake", "forest"],
    },
}