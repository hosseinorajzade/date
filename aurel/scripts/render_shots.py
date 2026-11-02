"""Render each shot of the EDL to a graded 1080x1920 lossless intermediate (FFV1).

usage: python3 -I scripts/render_shots.py [shot_name ...]
"""
import subprocess
import sys

import numpy as np
from PIL import Image, ImageFilter

sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from config import BUILD, DENSIFY, FINISH, FPS, SHOTS, SRC, SRC_H, SRC_W  # noqa: E402

IVORY = np.array([244, 237, 226], dtype=np.float32)  # light-wash colour (window light)


def decode(path, start_frame=0, count=None, start_time=None):
    """Return uint8 array (n, H, W, 3) of source frames."""
    cmd = ["ffmpeg", "-v", "error"]
    if start_time is not None:
        cmd += ["-ss", f"{start_time:.4f}"]
    cmd += ["-i", str(path)]
    vf = []
    if start_frame:
        vf.append(f"select='gte(n\\,{start_frame})'")
    if vf:
        cmd += ["-vf", ",".join(vf), "-vsync", "0"]
    if count:
        cmd += ["-frames:v", str(count)]
    cmd += ["-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    raw = subprocess.run(cmd, check=True, capture_output=True).stdout
    arr = np.frombuffer(raw, np.uint8).reshape(-1, SRC_H, SRC_W, 3)
    return arr


def retime_blend(frames, src_from, src_to, n_out, ease=None):
    """Frame-blended retime between two source frame indices (either direction)."""
    out = []
    for i in range(n_out):
        u = i / (n_out - 1)
        if ease == "out":
            u = 1 - (1 - u) ** 2
        pos = src_from + (src_to - src_from) * u
        a = int(np.floor(pos))
        b = min(a + 1, len(frames) - 1)
        w = pos - a
        f = frames[a].astype(np.float32) * (1 - w) + frames[b].astype(np.float32) * w
        out.append(f)
    return out


def _hblur(band, r):
    """Box blur along x only (keeps the vertical light falloff intact)."""
    if band.shape[0] == 0:
        return band
    c = np.cumsum(np.pad(band, ((0, 0), (r + 1, r), (0, 0)), mode="edge"), axis=1)
    return (c[:, 2 * r + 1:] - c[:, :-2 * r - 1]) / (2 * r + 1)


def extend_backdrop(frame, scale):
    """Pull the frame back to `scale` and continue the plain ivory backdrop into
    the new margin. Sides: pure edge continuation (the floor shadow simply runs
    on to the frame edge, as it does in the source). Top/bottom: edge
    continuation softened along x only, so the wall/floor light falloff stays
    physically continuous. Used only on the final packshot, to create
    type-safe space above and below the product without altering it."""
    fw, fh = int(SRC_W * scale) // 2 * 2, int(SRC_H * scale) // 2 * 2
    x0 = (SRC_W - fw) // 2
    y0 = 40  # keep more room below the plinth for the tagline
    fg = np.asarray(Image.fromarray(np.clip(frame, 0, 255).astype(np.uint8))
                    .resize((fw, fh), Image.LANCZOS), np.float32)
    pad = ((y0, SRC_H - y0 - fh), (x0, SRC_W - x0 - fw), (0, 0))
    canvas = np.pad(fg, pad, mode="edge")
    canvas[:y0] = _hblur(canvas[:y0], 30)
    canvas[y0 + fh:] = _hblur(canvas[y0 + fh:], 30)
    canvas[y0:y0 + fh, x0:x0 + fw] = fg
    return canvas


def light_wash(frames, n, at_end):
    """Soft lift toward ivory window light over n frames (max 30%)."""
    for k in range(n):
        idx = len(frames) - n + k if at_end else k
        t = (k + 1) / n if at_end else 1 - k / n
        a = 0.30 * (t ** 2)
        frames[idx] = frames[idx] * (1 - a) + IVORY * a
    return frames


def encode(frames, shot, out_path):
    chain = []
    if "crop" in shot:
        cw, ch, cx, cy = shot["crop"]
        chain.append(f"crop={cw}:{ch}:{cx}:{cy}")
    chain.append(shot["grade"])
    chain.append(FINISH)
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{SRC_W}x{SRC_H}", "-r", str(FPS), "-i", "-",
           "-vf", ",".join(chain), "-c:v", "ffv1", "-pix_fmt", "yuv444p", str(out_path)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for f in frames:
        p.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes())
    p.stdin.close()
    if p.wait():
        raise SystemExit(f"encode failed for {shot['name']}")


def render(shot):
    src = SRC / shot["src"]
    n = shot["frames"]
    if shot["mode"] == "realtime":
        frames = list(decode(src, start_time=shot["start"], count=n).astype(np.float32))
    elif shot["mode"] == "mci":
        mci = BUILD / f"{shot['name']}_mci.mkv"
        if not mci.exists():
            factor = 1 / shot["speed"]
            subprocess.run([
                "ffmpeg", "-v", "error", "-y", "-ss", str(shot["start"]), "-t", str(shot["src_dur"]),
                "-i", str(src), "-vf",
                f"setpts=PTS*{factor:.6f},minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1",
                "-c:v", "ffv1", str(mci)], check=True)
        frames = list(decode(mci, count=n).astype(np.float32))
    elif shot["mode"] == "dense":
        # Motion-interpolate the source span to DENSIFY x frames, then sample it
        # with the (optionally eased) time curve. Keeps the label crisp at very
        # slow speeds instead of the softness/pulsing of plain frame blending.
        lo, hi = sorted((shot["src_from"], shot["src_to"]))
        dense = BUILD / f"{shot['name']}_dense.mkv"
        if not dense.exists():
            subprocess.run([
                "ffmpeg", "-v", "error", "-y", "-ss", f"{lo / FPS:.5f}", "-t", f"{(hi - lo + 1) / FPS:.5f}",
                "-i", str(src), "-vf",
                f"setpts=PTS*{DENSIFY},minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1",
                "-c:v", "ffv1", str(dense)], check=True)
        allf = decode(dense)
        a = min((shot["src_from"] - lo) * DENSIFY, len(allf) - 1)
        b = min((shot["src_to"] - lo) * DENSIFY, len(allf) - 1)
        frames = retime_blend(allf, a, b, n, shot.get("ease"))
    elif shot["mode"] == "blend":
        allf = decode(src)
        frames = retime_blend(allf, shot["src_from"], shot["src_to"], n, shot.get("ease"))
    else:
        raise ValueError(shot["mode"])
    if len(frames) < n:
        raise SystemExit(f"{shot['name']}: only {len(frames)} frames, need {n}")
    frames = frames[:n]
    if "extend" in shot:
        frames = [extend_backdrop(f, shot["extend"]) for f in frames]
    if shot.get("light_out"):
        frames = light_wash(frames, shot["light_out"], at_end=True)
    if shot.get("light_in"):
        frames = light_wash(frames, shot["light_in"], at_end=False)
    out = BUILD / f"{shot['name']}.mkv"
    encode(frames, shot, out)
    print(f"rendered {out.name}: {n} frames")


if __name__ == "__main__":
    BUILD.mkdir(exist_ok=True)
    wanted = set(sys.argv[1:])
    for s in SHOTS:
        if not wanted or s["name"] in wanted:
            render(s)
