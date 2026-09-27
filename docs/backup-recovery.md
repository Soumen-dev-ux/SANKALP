# Backup and Recovery Procedures

## Objective
To ensure that SANKALP data (Citizen Requests, Reviews, Infrastructure) can be recovered in the event of a catastrophic failure, PostgreSQL backups must be automated and periodically tested.

## Strategy
- **Frequency**: Full backups must run nightly (e.g., via a Cron job).
- **Retention**: Keep nightly backups for 30 days, and monthly backups for 1 year.
- **Storage**: Backups should be streamed or copied to off-site secure storage (e.g., AWS S3 with restricted IAM roles).

## Automated Backup (Example via pg_dump)
```bash
#!/bin/bash
TIMESTAMP=$(date +%F_%H-%M-%S)
pg_dump -h $DB_HOST -U sankalp_admin -F c -b -v -f "/backups/sankalp_$TIMESTAMP.backup" $DB_NAME
```

## Restoration Procedure
> **WARNING**: Restoring a database overwrites existing data. Verify you are running this against the correct environment.

1. Terminate running FastAPI application instances to prevent writes during restoration.
2. Drop/recreate the target database:
   ```bash
   dropdb -h $DB_HOST -U postgres $DB_NAME
   createdb -h $DB_HOST -U postgres $DB_NAME
   ```
3. Restore from the backup file:
   ```bash
   pg_restore -h $DB_HOST -U postgres -d $DB_NAME -1 "/backups/sankalp_$TIMESTAMP.backup"
   ```
4. Restart the FastAPI application instances.
5. Verify application connectivity via the `/api/v1/health/db` endpoint.
