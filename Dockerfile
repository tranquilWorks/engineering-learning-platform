FROM node:22-alpine AS web-build
WORKDIR /src
COPY package.json ./
COPY apps/web/package.json apps/web/package.json
RUN npm install
COPY apps/web apps/web
RUN npm run build --workspace @elp/web

FROM python:3.12-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ELP_HOST=0.0.0.0 \
    ELP_PORT=8080 \
    ELP_COURSE_PATHS=/app/courses \
    ELP_WEB_DIST=/app/web
WORKDIR /app
COPY apps/api /app/apps/api
RUN pip install --no-cache-dir /app/apps/api
COPY courses /app/courses
COPY --from=web-build /src/apps/web/dist /app/web
USER 65532:65532
EXPOSE 8080
CMD ["python", "-m", "uvicorn", "elp_api.main:app", "--host", "0.0.0.0", "--port", "8080"]
