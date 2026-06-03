"""Extract theme colors from the LATAM template."""

import os

from pptx import Presentation
from pptx.oxml.ns import qn

from latam_gcs_template import TEMPLATE_PATH

if not os.path.exists(TEMPLATE_PATH):
    raise FileNotFoundError(
        f"PPTX template not found: {TEMPLATE_PATH}\n"
        "Set LATAM_TEMPLATE_PATH environment variable to the correct path.\n"
        "See docs/pptx/README.md for setup instructions."
    )

prs = Presentation(TEMPLATE_PATH)
master = prs.slide_masters[0]

theme_el = master.element.find('.//' + qn('a:theme'))
if theme_el is not None:
    clrScheme = theme_el.find('.//' + qn('a:clrScheme'))
    if clrScheme is not None:
        name = clrScheme.get('name')
        print("Theme: " + str(name))
        for child in clrScheme:
            tag = child.tag.split('}')[-1]
            for color_el in child:
                color_tag = color_el.tag.split('}')[-1]
                val = color_el.get('val', '')
                lastClr = color_el.get('lastClr', '')
                if color_tag == 'srgbClr':
                    print("  " + tag + ": #" + val)
                elif color_tag == 'sysClr':
                    print("  " + tag + ": #" + lastClr)
