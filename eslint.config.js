import js from "@eslint/js";

export default [
  js.configs.recommended,
  {
    languageOptions: {
      ecmaVersion: 2021,
      sourceType: "module",
      globals: {
        window: "readonly",
        document: "readonly",
        fetch: "readonly",
        confirm: "readonly"
      }
    },
    files: ["frontend/**/*.test.js", "frontend/**/*.spec.js"],
    linterOptions: {
      globals: {
        test: "readonly",
        expect: "readonly",
        require: "readonly",
        describe: "readonly",
        it: "readonly",
        beforeEach: "readonly",
        afterEach: "readonly"
      }
    }
    },
    rules: {
      "no-unused-vars": "warn",
      "no-console": "off"
    }
  }
];
