# Icon placeholder

VS Code expects `media/icon.png` (128×128 PNG) for the marketplace listing.

This file is a placeholder — replace with a real icon before publishing to the marketplace. See [VS Code docs](https://code.visualstudio.com/api/references/extension-manifest#fields) for icon requirements.

For local development and CI builds, the missing icon is **non-fatal**. `vsce package` only warns about it; publishing without one is allowed (the marketplace shows a generic icon).
