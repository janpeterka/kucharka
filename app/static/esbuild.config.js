const { sentryEsbuildPlugin } = require("@sentry/esbuild-plugin");

require("esbuild").build({
  entryPoints: ["./js/src/app.js"],
  outdir: "./js/dist",
  bundle: true,
  sourcemap: true, // Source map generation must be turned on
  plugins: [
    // Put the Sentry esbuild plugin after all other plugins
    sentryEsbuildPlugin({
      org: "scoutcook",
      project: "kucharka-javascript",

      // Specify the directory containing build artifacts
      include: "./js/dist",

      // Auth tokens can be obtained from https://sentry.io/settings/account/api/auth-tokens/
      // and need `project:releases` and `org:read` scopes
      authToken: process.env.SENTRY_AUTH_TOKEN,

      // Optionally uncomment the line below to override automatic release name detection
      // release: process.env.RELEASE,
    }),
  ],
});
