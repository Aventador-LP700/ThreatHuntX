FROM node:24.22.3-alpine@sha256:116b800c3754b440ee0aa3ed2f20f5bf3d99a554bfd9adeea09ea8017f6e85f5 AS build
WORKDIR /opt/web
COPY frontend/package.json frontend/package-lock.json ./
RUN --mount=type=secret,id=threathuntx_build_ca,mode=0444 \
    if [ -s /run/secrets/threathuntx_build_ca ]; then \
        export NODE_EXTRA_CA_CERTS=/run/secrets/threathuntx_build_ca; \
    fi \
    && npm ci --no-audit --no-fund
COPY frontend/ ./
RUN npm run build

FROM nginx:1.31.0-alpine@sha256:2f07d83bf561b506400dc183b1b2003803e39efbd22451f848adaba14d28c7c7
COPY --chown=101:101 infra/docker/nginx.conf /etc/nginx/nginx.conf
COPY --from=build --chown=101:101 /opt/web/dist /usr/share/nginx/html
COPY --chown=101:101 LICENSE THIRD_PARTY_NOTICES.md docs/licenses/*.txt /usr/share/nginx/html/licenses/
USER 101:101
EXPOSE 8080
ENTRYPOINT ["nginx", "-g", "daemon off;"]
