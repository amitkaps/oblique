import { defineConfig } from "vite";
import { matrixPage } from "./site/render.mjs";

// The page is zero-JS static HTML: matrixPage() renders the matrix into site/index.html at
// build time, Vite bundles the stylesheet. Output goes to dist/ and is deployed by CI.
export default defineConfig({
  root: "site",
  base: "/",
  plugins: [matrixPage()],
  build: { outDir: "../dist", emptyOutDir: true },
});
