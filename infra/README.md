# Local Infra

Start local dependencies:

```bash
docker compose -f infra/docker-compose.yml up -d
```

Services:
- Postgres: 5432
- MinIO: 9000 (console 9001)
- NATS JetStream: 4222 (monitoring 8222)
