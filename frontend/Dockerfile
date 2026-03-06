
FROM node:20

WORKDIR /app
# Copier le dossier frontend et le fichier de config ESLint depuis la racine
COPY frontend/ /app/
COPY eslint.config.cjs /app/eslint.config.cjs

# Installer toutes les dépendances (prod + dev)
RUN npm install && npm install --save-dev stylelint stylelint-config-standard jest playwright eslint @eslint/js

# Linter JS
RUN npx eslint --config eslint.config.cjs app.js

# Linter CSS
RUN npx stylelint styles.css

# Tests unitaires (en ignorant e2e.spec.js)
RUN npx jest --ci --runInBand --testPathIgnorePatterns="e2e\\.spec\\.js"

# Installer les navigateurs Playwright
RUN npx playwright install

# Tests end-to-end Playwright
RUN npx playwright test e2e.spec.js

EXPOSE 8080
CMD ["npx", "http-server", ".", "-p", "8080"]
