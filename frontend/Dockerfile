

FROM node:20



WORKDIR /app
# Copier le dossier frontend (incluant eslint.config.cjs qui doit être présent dans frontend)
COPY . /app/


# Installer uniquement les dépendances de production
RUN npm install --omit=dev


EXPOSE 8080
CMD ["npx", "http-server", ".", "-p", "8080"]
