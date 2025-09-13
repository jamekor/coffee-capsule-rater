# coffee-capsule-rater

An app to rate coffee capsules.

## Development

The project uses only the Python standard library, so no additional
dependencies are required.

Run the application locally:

```bash
python app/main.py
```

Run tests and formatting:

```bash
black .
python -m flake8
pytest
```

## Deployment

The server can run using environment variables for easy deployment.  Build and
run the provided Docker image:

```bash
docker build -t coffee-capsule-rater .
docker run -p 8000:8000 coffee-capsule-rater
```

Set the ``PORT`` and ``HOST`` variables if different values are required.

## Logging & Monitoring

Logs are written to standard output by default.  Set ``LOG_FILE`` to also write
logs to a file, which can be collected by monitoring systems.

## API

All endpoints accept and return JSON.

- ``POST /users`` – create a user
- ``POST /login`` – login and receive user ID header
- ``PUT /users/<id>`` – update profile (requires ``X-User-ID`` header)
- ``GET /capsules`` – list capsules
- ``POST /capsules`` – add a capsule
- ``GET /capsules/<id>`` – capsule detail
- ``GET /capsules/<id>/ratings`` – list ratings for a capsule
- ``POST /capsules/<id>/ratings`` – submit rating for a capsule
