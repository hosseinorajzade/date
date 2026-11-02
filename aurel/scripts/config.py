"""AUREL Radiance Serum 30s spot: edit decision list and grade settings.

Everything is defined at 24 fps (the native rate of all source clips).
Times are in seconds of the SOURCE clip unless stated otherwise.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "source"
BUILD = ROOT / "build"
RENDERS = ROOT / "renders"
FONTS = ROOT / "assets" / "fonts"

FPS = 24
W, H = 1080, 1920          # vertical master
SRC_W, SRC_H = 720, 1280   # all supplied clips

# Shared finishing applied after each shot's grade: lanczos upscale 720p -> 1080p,
# gentle sharpening to recover acutance lost in upscaling, fine grain so all six
# shots (different generators) share one texture.
FINISH = "scale=1080:1920:flags=lanczos,unsharp=5:5:0.35:5:5:0,noise=alls=2:allf=t"

# ---------------------------------------------------------------------------
# Edit decision list
#   frames  : output length in frames
#   mode    : "realtime" | "mci" (ffmpeg motion-interpolated slow motion)
#             | "blend" (frame-blended retime, for near-static camera moves)
#   grade   : ffmpeg filter chain (applied at source resolution, before FINISH)
# ---------------------------------------------------------------------------
SHOTS = [
    dict(
        name="s1_first_drop",
        src="01_first_drop_dark_pipette.mp4",
        mode="realtime", start=3.35, frames=96,      # 0:00.00 - 0:04.00
        # Rich espresso shadows but lifted a touch so they never crush;
        # highlights rolled off; warm (not orange) shadows.
        grade=("curves=all='0/0.025 0.25/0.225 0.6/0.6 1/0.95',"
               "colorbalance=rs=0.02:bs=-0.015:rh=0.0:bh=0.01,eq=saturation=0.92"),
    ),
    dict(
        name="s2_skin_in_light",
        src="02_skin_in_light_macro.mp4",
        # Window light sweeps across the cheek; out-point is before the source
        # blows out into artificial bokeh at 4.67 s.
        mode="realtime", start=0.25, frames=104,     # 0:04.00 - 0:08.33
        # Source is orange/yellow. Pull mids and highlights toward natural skin,
        # lower saturation, soften highlight roll-off.
        grade=("colorbalance=rm=-0.035:gm=-0.005:bm=0.03:rh=-0.025:bh=0.03,"
               "eq=saturation=0.86,curves=all='0/0.012 0.7/0.685 1/0.94'"),
    ),
    dict(
        name="s3_formula",
        src="03_formula_light_pipette.mp4",
        # In-point after the AI "drop reset" glitch at 4.75-5.0 s.
        mode="mci", start=5.04, src_dur=2.96, speed=0.75, frames=93,  # 0:08.33 - 0:12.21
        grade=("colorbalance=rh=-0.015:bh=0.05:bm=0.02,"
               "curves=all='0/0.02 0.5/0.52 1/0.97',eq=saturation=0.9"),
    ),
    dict(
        name="s4_ritual",
        src="04_ritual_application.mp4",
        # Out-point 3.54 s: just before a translucent AI "disc" appears on the
        # cheek (3.6 s onward, never fully clears).
        mode="realtime", start=0.0, frames=85,       # 0:12.21 - 0:15.75
        light_out=8,                                  # window-light wash into the reveal
        grade=("colorbalance=rm=-0.025:bm=0.02:rh=-0.015:bh=0.035,"
               "eq=saturation=0.9,curves=all='0/0.015 0.75/0.735 1/0.95'"),
    ),
    dict(
        name="s5_reveal",
        src="05_bottle_packshot.mp4",
        # Source frames 127 -> 191 (5.30 s -> 8.0 s): the clean push-in after the
        # AI water-ripple artefact on the plinth (2.4-5.2 s) has fully settled.
        mode="dense", src_from=127, src_to=191, ease=None,
        frames=210,                                  # 0:15.75 - 0:24.50 (last 12 f under dissolve)
        light_in=8,
        grade=("colorbalance=bm=0.012:bh=0.025:rh=-0.01,"
               "curves=all='0/0.02 0.5/0.545 0.85/0.915 1/0.975'"),
    ),
    dict(
        name="s6_signature",
        src="05_bottle_packshot.mp4",
        # Source frames 40 -> 0: a gentle settle-back (static product, no liquid
        # or hands, so playing it backwards is invisible) that lands exactly on
        # the cleanest original frame of the bottle (frame 0) for the packshot.
        mode="dense", src_from=40, src_to=0, ease="out",
        frames=144,                                  # 0:24.00 - 0:30.00
        extend=0.88,                                 # backdrop extension for type-safe margins
        grade=("colorbalance=bm=0.012:bh=0.025:rh=-0.01,"
               "curves=all='0/0.02 0.5/0.56 0.85/0.925 1/0.98'"),
    ),
]

DENSIFY = 4               # motion-interpolated sub-frames per source frame (dense mode)
DISSOLVE_FRAMES = 12      # only dissolve in the spot: reveal -> signature
FADE_IN_FRAMES = 12       # from black at the very top
TOTAL_FRAMES = 720        # 30.0 s

# Cue sheet (seconds, programme time) shared by audio + report
CUES = dict(
    cut_skin=96 / FPS,              # 4.000
    cut_formula=200 / FPS,          # 8.333
    drop_release=(200 + 40) / FPS,  # 10.000 - drop separates from the pipette
    cut_ritual=293 / FPS,           # 12.208
    first_touch=(293 + 37) / FPS,   # 13.750 - fingertips meet the cheek
    cut_reveal=378 / FPS,           # 15.750
    dissolve_sig=576 / FPS,         # 24.000
    brand_in=25.0,
    tagline_in=26.4,
)
