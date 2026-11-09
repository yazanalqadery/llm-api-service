## Try it

Live API: https://llm-api-service.onrender.com (interactive docs at `/docs`)

The free tier sleeps after 15 minutes without traffic, so the first request can take up to a minute.

Health check:

```bash
curl https://llm-api-service.onrender.com/health
```

Send text (returns 200):

```bash
curl -X POST https://llm-api-service.onrender.com/extract \
  -H "Content-Type: application/json" \
  -d '{"text": "hello"}'
```

Text over the limit returns 413:

```bash
curl -i -X POST https://llm-api-service.onrender.com/extract \
  -H "Content-Type: application/json" \
  -d '{"text": "this text is way too long for the limit"}'
```