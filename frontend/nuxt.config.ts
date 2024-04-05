// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: ["@nuxtjs/tailwindcss"],
  build: {
    transpile: ["@heroicons/vue"],
  },
  tailwindcss: {
    exposeConfig: true,
    viewer: true,
  },
  runtimeConfig: {
    public: {
      baseURL: `${
        process.env.NUXT_BACKEND_BASE_URL || "http://localhost:8000/"
      }api`,
    },
  },
});
