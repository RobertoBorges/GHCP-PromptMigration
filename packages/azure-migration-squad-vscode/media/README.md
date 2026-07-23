# Extension media assets

- **`icon.png`** — 128×128 marketplace icon. White "AMA" text on Azure blue (`#0078D4`) background. Generated from Arial Bold via `scripts/generate-icon.py` (see below). Regenerate if the initials change again.
- **`activity-bar-icon.svg`** — sidebar/activity-bar rocket icon (24×24 currentColor stroke).

## Regenerating `icon.png`

```powershell
python -c @"
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
OUT = Path('media/icon.png')
SIZE = 128
BLUE = (0, 120, 212, 255)  # Azure blue #0078D4
WHITE = (255, 255, 255, 255)
TEXT = 'AMA'
img = Image.new('RGBA', (SIZE, SIZE), BLUE)
draw = ImageDraw.Draw(img)
font = ImageFont.truetype('arialbd.ttf', 44)
bbox = draw.textbbox((0, 0), TEXT, font=font)
tw = bbox[2] - bbox[0]; th = bbox[3] - bbox[1]
x = (SIZE - tw) // 2 - bbox[0]
y = (SIZE - th) // 2 - bbox[1]
draw.text((x, y), TEXT, font=font, fill=WHITE)
img.save(OUT, 'PNG')
"@
```

See [VS Code docs](https://code.visualstudio.com/api/references/extension-manifest#fields) for icon requirements.
