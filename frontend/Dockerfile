

FROM node:20

# Installer les dépendances système nécessaires à Playwright/Chromium
RUN apt-get update && apt-get install -y \
	libnss3 \
	libatk-bridge2.0-0 \
	libgtk-3-0 \
	libxss1 \
	libasound2 \
	libgbm-dev \
	libnspr4 \
	libxshmfence1 \
	libxcomposite1 \
	libxrandr2 \
	libu2f-udev \
	libdrm2 \
	libxdamage1 \
	libpango-1.0-0 \
	libpangocairo-1.0-0 \
	libcups2 \
	libxinerama1 \
	fonts-liberation \
	libappindicator3-1 \
	libnss3-tools \
	wget \
	ca-certificates \
	--no-install-recommends && \
	rm -rf /var/lib/apt/lists/*

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
