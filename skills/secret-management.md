# Secret Management

Use this skill when handling secrets across application code, infrastructure, and CI/CD.

## Core policy

- Never commit secrets.
- Prefer managed identity over secrets.
- Use Key Vault for production secret storage.
- Use environment variables or local secret stores for development.
- Rotate secrets and certificates intentionally.

## Secret placement guide

| Secret type | Recommended store |
|---|---|
| app runtime secrets | Azure Key Vault |
| CI/CD credentials | OIDC where possible, otherwise pipeline secret store |
| local dev secrets | user secrets / `.env` outside source control |

## Validation checklist

- Repo history and config files contain no secret values.
- Secret names, not values, appear in docs and templates.
- Rotation owner and process are known.
