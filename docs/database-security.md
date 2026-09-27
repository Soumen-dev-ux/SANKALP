# Database Security Guidelines

To ensure the production PostgreSQL instance remains secure, SANKALP enforces a **least privilege** architecture.

## Role Setup
The application must not use a PostgreSQL superuser in production. It is recommended to create two separate roles:

1. **`sankalp_admin`**
   - Has DDL privileges (CREATE, ALTER, DROP).
   - Should ONLY be used during deployment to run `alembic upgrade head`.

2. **`sankalp_app`**
   - Has DML privileges only (SELECT, INSERT, UPDATE, DELETE).
   - Used by the running FastAPI application.

## Best Practices
- **Connection Strings**: Never hardcode credentials in code. Always pass the `DATABASE_URL` via environment variables.
- **SSL**: Enable `sslmode=require` in the database URL if connecting over a non-private network.
- **Connection Pooling**: Use PgBouncer or similar tools in high-traffic deployments to prevent connection starvation.
- **Port Exposure**: Ensure port `5432` is not publicly exposed to the internet. Use VPC peering or strict firewall rules to allow access only from the API servers.
