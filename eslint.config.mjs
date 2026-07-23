import security from "eslint-plugin-security";

export default [
  {
    files: ["**/*.js"],
    ignores: ["node_modules/**"],
    plugins: { security },
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: "script",
      globals: { document: "readonly", fetch: "readonly", alert: "readonly" },
    },
    rules: {
      ...security.configs.recommended.rules,
    },
  },
];
