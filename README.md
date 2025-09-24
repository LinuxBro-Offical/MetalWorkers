# Metal Workers API (FastAPI + Docker)

A minimal FastAPI application for the Metal Workers project, with Docker support.

## Run locally

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Open `http://localhost:8000` and `http://localhost:8000/docs`.

## Docker

Build the image:

```bash
docker build -t metalworkers-api .
```

Run the container:

```bash
docker run --rm -p 8000:8000 metalworkers-api
```

Endpoints:
- `/` → Welcome message
- `/health` → Health check

## Quick test

```bash
curl -s http://localhost:8000/health | jq
```

## Docker (development auto-reload)

```bash
docker run --rm -it \
  -p 8000:8000 \
  -v /home/ananthu/Development/MetalWorkers/metalworkers-api:/app \
  metalworkers-api \
  uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Docker (detached background)

```bash
docker run -d --name metalworkers-api -p 8000:8000 metalworkers-api
```

## Docker (detached + auto-reload)

```bash
docker run -d --name metalworkers-api-dev \
  -p 8000:8000 \
  -v /home/ananthu/Development/MetalWorkers/metalworkers-api:/app \
  metalworkers-api \
  uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Stop background container

```bash
docker stop metalworkers-api
``` 