# Azure Migration Squad — Starter Template

> **One-click template repo content.** Push this folder to a new GitHub repo to make it available as a "Use this template" starter for engagements.

This folder contains:
- A minimal `.squad/` skeleton
- A sample `Use-cases/sample-aspnet-app/` placeholder representing "the application being migrated"
- A `README.md` with the recommended onboarding flow
- A `.gitignore` tuned for the squad + sample workloads

## When you're ready to publish this as a GitHub template

```bash
# Option A — push as a brand-new GitHub repo and toggle the template flag
gh repo create azure-migration-squad-template --public --source=template-repo-starter --remote=origin --push
gh api repos/RobertoBorges/azure-migration-squad-template -X PATCH -F is_template=true

# Option B — manually
# 1. Create empty repo at github.com/RobertoBorges/azure-migration-squad-template
# 2. Copy this folder's content into it
# 3. Settings → General → Template repository → ON
# 4. Add the "Use this template" CTA link to the docs hub README
```

After publishing, end users can click **Use this template** on https://github.com/RobertoBorges/azure-migration-squad-template/generate to get an instant starter.

## What's inside

```
template-repo-starter/
├── README.md              ← onboarding instructions for new starter repos
├── .gitignore             ← squad-tuned gitignore
├── .squad/
│   └── team.md            ← minimal stub; replaced by `squad init`
└── Use-cases/
    └── sample-aspnet-app/
        └── README.md      ← placeholder representing the user's app
```

When a developer uses this template:

1. `squad init` populates `.squad/` with full team / routing / decisions structure
2. `npx @robertoborges/azure-migration-squad init` adds the 15 agents + skills + prompts
3. They replace `Use-cases/sample-aspnet-app/` with their actual application
4. `/assess-any-application` in Copilot Chat kicks off discovery
