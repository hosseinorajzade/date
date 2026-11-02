"""Conform the graded shots, typography and soundtrack into the deliverables.

renders/
  AUREL_RadianceSerum_30s_9x16_1080x1920.mp4         master (with type)
  AUREL_RadianceSerum_30s_9x16_1080x1920_CLEAN.mp4   textless
  AUREL_RadianceSerum_30s_16x9_1920x1080.mp4         website edit (with type)
  AUREL_RadianceSerum_30s_16x9_1920x1080_CLEAN.mp4   website textless
  AUREL_packshot_9x16.png / _CLEAN.png, AUREL_packshot_16x9.png
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import BUILD, CUES, DISSOLVE_FRAMES, FADE_IN_FRAMES, FPS, RENDERS, SHOTS, TOTAL_FRAMES  # noqa: E402

NAME = "AUREL_RadianceSerum_30s"
DUR = TOTAL_FRAMES / FPS
# Website edit: 4:5 window (1080x1350 of the 1080x1920 grade) per shot, framed
# on the action, downscaled to 864x1080 and set against an ivory type panel.
CROP_Y_16x9 = {
    "s1_first_drop": 470, "s2_skin_in_light": 300, "s3_formula": 380,
    "s4_ritual": 110, "s5_reveal": 400, "s6_signature": 330,
}
PANEL = "0xEDE7DC"  # matched to the graded packshot backdrop


def run(cmd):
    subprocess.run(cmd, check=True)


def audio_master():
    """Two-pass EBU R128 loudness normalisation to -16 LUFS / -1.5 dBTP (linear)."""
    raw = BUILD / "soundtrack_f32.raw"
    inp = ["-f", "f32le", "-ar", "48000", "-ac", "2", "-i", str(raw)]
    p = subprocess.run(["ffmpeg", "-hide_banner", *inp, "-af",
                        "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True, check=True)
    m = json.loads(p.stderr[p.stderr.rindex("{"):p.stderr.rindex("}") + 1])
    out = BUILD / "soundtrack_master.wav"
    af = ("loudnorm=I=-16:TP=-1.5:LRA=11:linear=true:"
          f"measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
          f"measured_thresh={m['input_thresh']}:offset={m['target_offset']},aresample=48000")
    run(["ffmpeg", "-v", "error", "-y", *inp, "-af", af, "-c:a", "pcm_s24le", "-t", f"{DUR}", str(out)])
    return out


def picture_graph(horizontal, with_type, n_inputs):
    g = []
    labels = []
    for i, s in enumerate(SHOTS):
        chain = f"[{i}:v]setpts=PTS-STARTPTS"
        if horizontal:
            chain += f",crop=1080:1350:0:{CROP_Y_16x9[s['name']]},scale=864:1080:flags=lanczos"
        if i == 0:
            chain += f",fade=t=in:s=0:n={FADE_IN_FRAMES}"
        chain += ",format=yuv444p,settb=1/24"
        g.append(chain + f"[p{i}]")
        labels.append(f"[p{i}]")
    # straight cuts s1..s5, one dissolve s5 -> s6
    g.append("".join(labels[:-1]) + f"concat=n={len(labels) - 1}:v=1:a=0,settb=1/24[body]")
    body_frames = sum(s["frames"] for s in SHOTS[:-1])
    offset = (body_frames - DISSOLVE_FRAMES) / FPS
    g.append(f"[body]{labels[-1]}xfade=transition=fade:duration={DISSOLVE_FRAMES / FPS}:offset={offset}[pic]")
    cur = "[pic]"
    if horizontal:
        g.append(f"color=c={PANEL}:s=1920x1080:r={FPS}:d={DUR},format=yuv444p[bg]")
        g.append(f"[bg]{cur}overlay=x=1056:y=0:shortest=1[comp]")
        cur = "[comp]"
    if with_type:
        bi, ti = n_inputs, n_inputs + 1
        g.append(f"[{bi}:v]format=rgba,fade=t=in:st={CUES['brand_in']}:d=1.0:alpha=1[tb]")
        g.append(f"[{ti}:v]format=rgba,fade=t=in:st={CUES['tagline_in']}:d=1.0:alpha=1[tt]")
        g.append(f"{cur}[tb]overlay=0:0:format=auto[o1]")
        g.append("[o1][tt]overlay=0:0:format=auto[o2]")
        cur = "[o2]"
    g.append(f"{cur}format=yuv420p[vout]")
    return ";".join(g)


def render(horizontal, with_type, audio):
    inputs = []
    for s in SHOTS:
        inputs += ["-i", str(BUILD / f"{s['name']}.mkv")]
    n = len(SHOTS)
    tag = "h" if horizontal else "v"
    if with_type:
        for p in (f"type_brand_{tag}.png", f"type_tagline_{tag}.png"):
            inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{DUR}", "-i", str(BUILD / p)]
    a_idx = n + (2 if with_type else 0)
    inputs += ["-i", str(audio)]
    size = "16x9_1920x1080" if horizontal else "9x16_1080x1920"
    out = RENDERS / f"{NAME}_{size}{'' if with_type else '_CLEAN'}.mp4"
    run(["ffmpeg", "-v", "error", "-y", *inputs,
         "-filter_complex", picture_graph(horizontal, with_type, n),
         "-map", "[vout]", "-map", f"{a_idx}:a",
         "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-profile:v", "high", "-level", "4.2",
         "-pix_fmt", "yuv420p", "-r", str(FPS), "-g", str(FPS * 2),
         "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
         "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-ac", "2",
         "-frames:v", str(TOTAL_FRAMES), "-t", f"{DUR}", "-movflags", "+faststart", str(out)])
    print("rendered", out.name)
    return out


def still(video, out):
    run(["ffmpeg", "-v", "error", "-y", "-sseof", "-0.05", "-i", str(video),
         "-frames:v", "1", "-update", "1", str(out)])
    print("still", out.name)


if __name__ == "__main__":
    RENDERS.mkdir(exist_ok=True)
    audio = audio_master()
    jobs = sys.argv[1:] or ["v", "v_clean", "h", "h_clean"]
    outs = {}
    for j in jobs:
        outs[j] = render(horizontal=j.startswith("h"), with_type=not j.endswith("clean"), audio=audio)
    if "v" in outs:
        still(outs["v"], RENDERS / "AUREL_packshot_9x16.png")
    if "v_clean" in outs:
        still(outs["v_clean"], RENDERS / "AUREL_packshot_9x16_CLEAN.png")
    if "h" in outs:
        still(outs["h"], RENDERS / "AUREL_packshot_16x9.png")
