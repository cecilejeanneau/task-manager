
FROM node:20

WORKDIR /app
# Copier le dossier frontend (incluant eslint.config.cjs qui doit être présent dans frontend)
COPY . /app/

# Installer toutes les dépendances (prod + dev)
RUN npm install && npm install --save-dev stylelint stylelint-config-standard jest playwright eslint @eslint/js

# Linter JS
RUN npx eslint --config eslint.config.cjs app.js

# Linter CSS
RUN npx stylelint styles.css

# Tests unitaires (comme la CI, uniquement test_app.test.js)
RUN npx jest test_app.test.js

# Installer les navigateurs Playwright
RUN npx playwright install

# Tests end-to-end Playwright
RUN npx playwright test e2e.spec.js

EXPOSE 8080
CMD ["npx", "http-server", ".", "-p", "8080"]
