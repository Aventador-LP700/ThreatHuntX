FROM node:26.13.0-alpine@sha256:8996bb5821d62a8fd9bb27c1cb07462f3fdce6e47d640c6a881ead0b064ce216 AS build
WORKDIR /opt/web
COPY frontend/package.json frontend/package-lock.json ./
RUN --mount=type=secret,id=threathuntx_build_ca,mode=0444 \
    if [ -s /run/secrets/threathuntx_build_ca ]; then \
        export NODE_EXTRA_CA_CERTS=/run/secrets/threathuntx_build_ca; \
    fi \
    && npm ci --no-audit --no-fund
COPY frontend/ ./
RUN npm run build

FROM nginx:1.30.5-alpine@sha256:0985e772fb9f729e6fa0980da05fca5d9c468e870eed43071545afa9d2e27d94
COPY --chown=101:101 infra/docker/nginx.conf /etc/nginx/nginx.conf
COPY --from=build --chown=101:101 /opt/web/dist /usr/share/nginx/html
COPY --chown=101:101 LICENSE THIRD_PARTY_NOTICES.md docs/licenses/*.txt /usr/share/nginx/html/licenses/
USER 101:101
EXPOSE 8080
ENTRYPOINT ["nginx", "-g", "daemon off;"]
