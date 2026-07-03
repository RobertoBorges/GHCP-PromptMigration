"""
Export Migration Strategy HTML Report to PDF with full CSS fidelity.

Uses Chromium's native PDF renderer for crisp vector text, with DOM fixes
to ensure the title slide renders on page 1 and all backgrounds appear.

Usage:
    python export_to_pdf.py <input.html> [output.pdf]

Requirements:
    pip install playwright
    playwright install chromium
"""

import sys
import os
import re
from pathlib import Path


# Patterns that indicate dollar signs were stripped by PowerShell
# Each tuple: (regex_pattern, expected_replacement, description)
DOLLAR_FIXES = [
    # Cost figures like ".21M/mo" → "$1.21M/mo", "/mo" alone, "~.4M"
    (r'(?<=>)\.([\d]+M/(?:mo|yr))', r'$\1', 'cost with M'),
    (r'(?<=>)([\d,]+/mo)', r'$\1', 'raw number/mo'),
    (r'(?<=>)~\.([\d]+M)', r'~$\1', 'tilde cost'),
    (r'(?<=>)\.([\d]+M)', r'$\1', 'dot-start cost'),
    # Bare numbers that should have $ (inside <strong> or <td>)
    (r'<strong>,(\d{3},\d{3}(?:/mo)?)</strong>', r'<strong>$\1</strong>', 'strong-wrapped number'),
    (r'<strong>,(\d{3},\d{3},\d{3})</strong>', r'<strong>$\1</strong>', 'strong large number'),
    (r'<strong>,(\d{3})</strong>', r'<strong>$\1</strong>', 'strong small number'),
    (r'<td>\.([\d]+M)</td>', r'<td>$\1</td>', 'td cost M'),
    (r'<td>~\.([\d]+M)</td>', r'<td>~$\1</td>', 'td tilde cost'),
]


def validate_and_fix_dollars(html_path: Path) -> bool:
    """Check for missing $ signs (PowerShell variable interpolation damage).
    Returns True if fixes were applied."""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Quick check: does the file contain $ or &#36; at all?
    has_dollar = '$' in content or '&#36;' in content
    has_cost_patterns = bool(re.search(r'/mo|/yr|\d+M\b', content))

    if has_cost_patterns and not has_dollar:
        print(f"\n*** WARNING: No $ signs found but cost patterns detected! ***")
        print(f"*** This typically means PowerShell stripped $ as variables. ***")
        print(f"*** Attempting automatic fix... ***\n")

        fixed_count = 0
        for pattern, replacement, desc in DOLLAR_FIXES:
            matches = re.findall(pattern, content)
            if matches:
                content = re.sub(pattern, replacement, content)
                fixed_count += len(matches)
                print(f"  Fixed {len(matches)}x: {desc}")

        if fixed_count > 0:
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"\n*** Auto-fixed {fixed_count} missing $ signs ***")
            print(f"*** TIP: Write HTML files using Python, not PowerShell heredocs ***\n")
            return True
        else:
            print(f"\n*** Could not auto-fix. Please check the HTML manually. ***\n")

    return False


def export_pdf(html_path: str, pdf_path: str = None):
    from playwright.sync_api import sync_playwright

    html_path = Path(html_path).resolve()
    if not html_path.exists():
        print(f"Error: File not found: {html_path}")
        sys.exit(1)

    if pdf_path is None:
        pdf_path = html_path.with_suffix(".pdf")
    else:
        pdf_path = Path(pdf_path).resolve()

    print(f"Input:  {html_path}")
    print(f"Output: {pdf_path}")

    # Pre-flight: detect and fix PowerShell $ sign damage
    validate_and_fix_dollars(html_path)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 960})

        # Load the HTML file
        page.goto(f"file:///{html_path.as_posix()}", wait_until="networkidle")

        # Fix 1: Remove all text/comment nodes before first slide
        # (whitespace between <body> and first .slide causes blank page 1)
        # Fix 2: Set body background to transparent so the PDF renderer
        # doesn't paint a full gray page before the first slide content
        # Fix 3: Remove slide margins so content starts at page top
        # Fix 4: Convert CSS gradients to solid colors for PDF compatibility
        # Fix 5: Force -webkit-print-color-adjust: exact on all elements
        page.evaluate("""() => {
            // Remove whitespace/comment nodes before first slide
            const body = document.body;
            const firstSlide = body.querySelector('.slide');
            while (body.firstChild && body.firstChild !== firstSlide) {
                body.removeChild(body.firstChild);
            }
            // Also remove trailing nodes after last slide
            const lastSlide = body.querySelector('.slide:last-child');
            while (lastSlide && lastSlide.nextSibling) {
                body.removeChild(lastSlide.nextSibling);
            }
            // Force body to have no background (prevents blank first page)
            body.style.cssText = 'background: none !important; margin: 0 !important; padding: 0 !important;';
            // Remove margins from all slides
            document.querySelectorAll('.slide').forEach(slide => {
                slide.style.margin = '0 auto';
            });

            // Force print color rendering on all elements
            const printFix = document.createElement('style');
            printFix.textContent = `
                * {
                    -webkit-print-color-adjust: exact !important;
                    color-adjust: exact !important;
                    print-color-adjust: exact !important;
                }
            `;
            document.head.appendChild(printFix);

            // Convert gradient backgrounds to solid colors for PDF rendering.
            // Chromium's PDF renderer often strips linear-gradient() backgrounds.
            // We compute the actual rendered backgroundColor as fallback, then
            // replace the gradient with a solid color.
            const gradientMap = {
                'blue':   '#0078d4',
                'green':  '#107c10',
                'orange': '#ff8c00',
                'red':    '#d32f2f',
                'purple': '#6b21a8',
            };

            // Fix bar chart fills
            document.querySelectorAll('.bar-fill').forEach(el => {
                for (const [cls, color] of Object.entries(gradientMap)) {
                    if (el.classList.contains(cls)) {
                        el.style.background = color;
                        break;
                    }
                }
            });

            // Fix KPI cards that use gradients
            document.querySelectorAll('.kpi-card').forEach(el => {
                const bg = getComputedStyle(el).backgroundImage;
                if (bg && bg.includes('gradient')) {
                    if (el.classList.contains('highlight')) {
                        el.style.background = '#e6f2ff';
                    } else if (el.classList.contains('warning')) {
                        el.style.background = '#fff8e6';
                    } else if (el.classList.contains('success')) {
                        el.style.background = '#e6ffe6';
                    } else {
                        el.style.background = '#f0f2ff';
                    }
                }
            });

            // Fix title slide gradient
            document.querySelectorAll('.title-slide').forEach(el => {
                el.style.background = '#00497a';
            });

            // Fix slide ::before top-bar gradient — replace with solid color
            const barFix = document.createElement('style');
            barFix.textContent = `
                .slide::before {
                    background: #0078d4 !important;
                }
            `;
            document.head.appendChild(barFix);

            // Fix strategy cards
            document.querySelectorAll('.strategy-card').forEach(el => {
                const bg = getComputedStyle(el).backgroundImage;
                if (bg && bg.includes('gradient')) {
                    if (el.classList.contains('opt-a')) el.style.background = '#f0f8ff';
                    else if (el.classList.contains('opt-b')) el.style.background = '#f0fff0';
                    else if (el.classList.contains('opt-c')) el.style.background = '#faf5ff';
                }
            });

            // Fix risk badges
            document.querySelectorAll('.risk-badge').forEach(el => {
                const bg = getComputedStyle(el).backgroundImage;
                if (bg && bg.includes('gradient')) {
                    if (el.classList.contains('high')) el.style.background = '#d32f2f';
                    else if (el.classList.contains('medium')) el.style.background = '#ff8c00';
                }
            });

            // Fix dc-card backgrounds
            document.querySelectorAll('.dc-card').forEach(el => {
                const bg = getComputedStyle(el).backgroundImage;
                if (bg && bg.includes('gradient')) {
                    el.style.background = '#f8f9ff';
                }
            });
        }""")

        # Force "screen" media so backgrounds, bar colors render
        page.emulate_media(media="screen")
        page.wait_for_timeout(500)

        # Native PDF export — produces vector text (sharp/crisp)
        page.pdf(
            path=str(pdf_path),
            width="1280px",
            height="960px",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )

        browser.close()

    file_size = pdf_path.stat().st_size / 1024
    print(f"Done! PDF exported ({file_size:.0f} KB)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python export_to_pdf.py <input.html> [output.pdf]")
        print("")
        print("Examples:")
        print('  python export_to_pdf.py "<customer>/Migration_Strategy_Report.html"')
        print('  python export_to_pdf.py "<customer>/Migration_Strategy_Report.html" "<customer>/Report_Final.pdf"')
        sys.exit(1)

    html_file = sys.argv[1]
    pdf_file = sys.argv[2] if len(sys.argv) > 2 else None
    export_pdf(html_file, pdf_file)
