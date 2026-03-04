export default [
  {
    languageOptions: {
      ecmaVersion: 2021,
      sourceType: "module",
      globals: {
        window: "readonly",
        document: "readonly"
      }
    },
    linterOptions: {
      env: {
        browser: true,
        es2021: true
      }
    },
    extends: ["eslint:recommended"],
    rules: {
      "no-unused-vars": "warn",
      "no-console": "off"
    }
  }
];
