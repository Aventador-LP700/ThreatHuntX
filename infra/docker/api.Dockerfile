FROM python:3.15.1-slim-bookworm@sha256:575f8bc12ec26542e0678bc6b60e385218248019d433157ec327264a78c3a853
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 THREATHUNTX_ROOT=/opt/threathuntx
WORKDIR /opt/threathuntx
COPY infra/docker/requirements.txt ./requirements.txt
RUN --mount=type=secret,id=threathuntx_build_ca,mode=0444 \
    if [ -s /run/secrets/threathuntx_build_ca ]; then \
        cat /etc/ssl/certs/ca-certificates.crt /run/secrets/threathuntx_build_ca > /tmp/build-ca.pem; \
        export PIP_CERT=/tmp/build-ca.pem; \
    fi \
    && pip install --disable-pip-version-check --no-cache-dir --require-hashes -r requirements.txt \
    && rm -f /tmp/build-ca.pem \
    && groupadd --gid 10001 lab \
    && useradd --uid 10001 --gid 10001 --no-create-home lab \
    && install -d -o lab -g lab /var/lib/threathuntx
COPY --chown=10001:10001 backend/app ./app
COPY --chown=10001:10001 scenarios ./scenarios
COPY --chown=10001:10001 detections ./detections
USER 10001:10001
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--no-proxy-headers", "--limit-concurrency", "64"]
