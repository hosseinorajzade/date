"""Render the end-card typography as transparent PNG overlays.

Brand    : AUREL            (Cormorant Garamond 500, wide tracking)
Product  : RADIANCE SERUM   (Inter Light, small caps-style tracking)
Tagline  : Your Skin, In Its Own Light.   (Cormorant Garamond 400)

Fonts: Cormorant Garamond (SIL OFL 1.1), Inter (SIL OFL 1.1) - both licensed for
commercial use, files in assets/fonts.

Text is rendered at 3x and downsampled for clean anti-aliasing. All text sits
inside 10% horizontal and 12% vertical safe margins.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
from config import BUILD, FONTS  # noqa: E402

SS = 3
INK = (52, 41, 33)  # espresso, never pure black


def font(name, px):
    return ImageFont.truetype(str(FONTS / name), px * SS)


def tracked_line(draw, cx, y, text, fnt, tracking_em, fill):
    """Draw centred text with letter-spacing (PIL has no native tracking)."""
    size = fnt.size
    gap = tracking_em * size
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + gap * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill, anchor="ls")  # baseline-anchored
        x += w + gap


def layer(w, h, items, out):
    img = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for cx, baseline, text, fnt, track, alpha in items:
        tracked_line(d, cx * SS, baseline * SS, text, fnt, track, INK + (alpha,))
    img.resize((w, h), Image.LANCZOS).save(out)
    print("wrote", out.name)


def build():
    BUILD.mkdir(exist_ok=True)
    brand_v = font("cormorant-garamond-latin-500-normal.woff", 112)
    prod_v = font("Inter-Light.otf", 25)
    tag_v = font("cormorant-garamond-latin-400-normal.woff", 56)

    # Vertical 1080x1920: bottle cap top ~y500, plinth base ~y1490 (final frame).
    layer(1080, 1920, [
        (540, 346, "AUREL", brand_v, 0.30, 236),
        (540, 412, "RADIANCE SERUM", prod_v, 0.42, 215),
    ], BUILD / "type_brand_v.png")
    layer(1080, 1920, [
        (540, 1622, "Your Skin, In Its Own Light.", tag_v, 0.035, 230),
    ], BUILD / "type_tagline_v.png")

    # Website 1920x1080: picture panel on the right (x 1056-1920), type panel left.
    brand_h = font("cormorant-garamond-latin-500-normal.woff", 120)
    prod_h = font("Inter-Light.otf", 24)
    tag_h = font("cormorant-garamond-latin-400-normal.woff", 52)
    cx = 528
    layer(1920, 1080, [
        (cx, 492, "AUREL", brand_h, 0.30, 236),
        (cx, 560, "RADIANCE SERUM", prod_h, 0.42, 215),
    ], BUILD / "type_brand_h.png")
    layer(1920, 1080, [
        (cx, 676, "Your Skin, In Its Own Light.", tag_h, 0.035, 230),
    ], BUILD / "type_tagline_h.png")


if __name__ == "__main__":
    build()
