/** @type {import('tailwindcss').Config} */
module.exports = {
    experimental: {
        optimizeUniversalDefaults: true,
    },
    content: [
        "./templates/**/*.html",
        "./templates/*.html",
        "./static/js/*.js"
    ],
    theme: {
        extend: {
            colors: {
                "regal-blue": "#13233A",
            },
        },
    },
    plugins: [
        function ({ addVariant }) {
            addVariant("child", "& > *");
            addVariant("grand-child", "& > * > *");
        },
    ],
    corePlugins: {
        preflight: false,
    },
};

