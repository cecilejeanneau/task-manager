FROM node:20

WORKDIR /app
COPY . /app/

RUN npm install --omit=dev && npm install --save-dev jest playwright

# Lint (si présent)
RUN if [ -f eslint.config.cjs ]; then npx eslint app.js; fi

# Tests unitaires
RUN npx jest --ci --runInBand

# Tests end-to-end
RUN npx playwright install && npx playwright test e2e.spec.js

EXPOSE 8080
CMD ["npx", "http-server", ".", "-p", "8080"]
