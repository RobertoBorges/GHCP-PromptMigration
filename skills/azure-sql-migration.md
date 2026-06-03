# Azure SQL Migration

Use this skill when the source application uses SQL Server and the target data platform is Azure SQL Database.

## When to use

Apply this skill when the application uses SQL Server, LocalDB, or a compatible relational schema that can move to Azure SQL with minimal engine changes.

## Migration workflow

1. Assess compatibility level, CLR usage, SQL Agent dependencies, and unsupported features.
2. Choose migration mechanism: DACPAC, Azure Database Migration Service, backup/restore to Managed Instance, or application-driven schema deployment.
3. Update connection handling, firewall/private networking, and authentication.
4. Re-test performance, indexing, and retry behavior.

## Design defaults

- Prefer Azure SQL Database for standard app databases.
- Use Managed Instance only when SQL Server compatibility needs are substantial.
- Prefer Entra auth or managed identity where supported.
- Configure automatic backups, Defender, auditing, and alerting.

## Connection string pattern

```text
Server=tcp:<server>.database.windows.net,1433;Database=<db>;Authentication=Active Directory Default;Encrypt=True;TrustServerCertificate=False;
```

## Validation checklist

- Schema deploys cleanly.
- Required features are supported on the chosen tier.
- Application retries transient failures.
- Performance baselines are captured after migration.
