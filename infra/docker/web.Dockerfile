FROM node:22.21.1-bookworm-slim@sha256:25b3eb23a00590b7499f2a2ce939322727fcce1b15fdd69754fcd09536a3ae2c AS build
WORKDIR /opt/web
COPY frontend/package.json frontend/package-lock.json ./
RUN --mount=type=secret,id=threathuntx_build_ca,mode=0444 \
    if [ -s /run/secrets/threathuntx_build_ca ]; then \
        export NODE_EXTRA_CA_CERTS=/run/secrets/threathuntx_build_ca; \
    fi \
    && npm ci --no-audit --no-fund
COPY frontend/ ./
RUN npm run build

FROM nginx:1.28.0-alpine@sha256:30f1c0d78e0ad60901648be663a710bdadf19e4c10ac6782c235200619158284
COPY --chown=101:101 infra/docker/nginx.conf /etc/nginx/nginx.conf
COPY --from=build --chown=101:101 /opt/web/dist /usr/share/nginx/html
USER 101:101
EXPOSE 8080
ENTRYPOINT ["nginx", "-g", "daemon off;"]
