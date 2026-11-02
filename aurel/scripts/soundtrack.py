"""Original score + sound design for the AUREL spot, synthesised from scratch
(numpy only, no samples, no third-party audio -> no licensing questions).

Writes build/soundtrack_f32.raw (48 kHz, stereo, float32 little-endian, 30.0 s).
The loudness pass (-16 LUFS integrated, -1.5 dBTP) happens at mux time.
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from config import BUILD, CUES  # noqa: E402

SR = 48000
DUR = 30.0
N = int(SR * DUR)
rng = np.random.default_rng(7)

A4 = 440.0
NOTE = {n: i for i, n in enumerate(["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"])}


def hz(name):
    pitch, octave = name[:-1], int(name[-1])
    return A4 * 2 ** ((NOTE[pitch] + 12 * (octave + 1) - 69) / 12)


def t_axis(n):
    return np.arange(n) / SR


def fft_filter(x, lo=None, hi=None, slope=2):
    """Zero-phase spectral band filter with smooth (butterworth-like) skirts."""
    n = len(x)
    X = np.fft.rfft(x, axis=0)
    f = np.fft.rfftfreq(n, 1 / SR)
    g = np.ones_like(f)
    if hi:
        g /= np.sqrt(1 + (f / hi) ** (2 * slope))
    if lo:
        g /= np.sqrt(1 + (lo / np.maximum(f, 1e-3)) ** (2 * slope))
    if X.ndim == 2:
        g = g[:, None]
    return np.fft.irfft(X * g, n, axis=0)


def place(bus, sig, t0, pan=0.0, gain=1.0):
    """Add mono or stereo sig into the stereo bus at t0 seconds (equal-power pan)."""
    i0 = int(round(t0 * SR))
    if sig.ndim == 1:
        l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
        sig = np.stack([sig * l, sig * r], 1)
    i1 = min(i0 + len(sig), len(bus))
    if i1 > i0:
        bus[i0:i1] += sig[: i1 - i0] * gain


def env_adsr(n, a, r, hold_curve=1.0):
    e = np.ones(n)
    na, nr = int(a * SR), int(r * SR)
    if na:
        e[:na] = np.sin(np.linspace(0, np.pi / 2, na)) ** 2
    if nr:
        e[-nr:] *= np.cos(np.linspace(0, np.pi / 2, nr)) ** 2
    return e * hold_curve


# --------------------------------------------------------------------------- music
def pad_note(f, dur, bright=0.3):
    """Warm detuned pad voice: three slightly detuned sines + soft harmonics,
    slow chorus drift, returned as stereo."""
    n = int(dur * SR)
    t = t_axis(n)
    out = np.zeros((n, 2))
    for k, (cents, pan) in enumerate([(-5, -0.7), (0, 0.0), (6, 0.7)]):
        drift = 1 + 0.0012 * np.sin(2 * np.pi * (0.11 + 0.05 * k) * t + k)
        ff = f * 2 ** (cents / 1200) * drift
        ph = 2 * np.pi * np.cumsum(ff) / SR + rng.uniform(0, 6.28)
        v = np.sin(ph) + bright * 0.35 * np.sin(2 * ph) + bright * 0.12 * np.sin(3 * ph)
        l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
        out[:, 0] += v * l
        out[:, 1] += v * r
    return out / 3


def pad_chord(notes, t0, t1, amp, bright=0.3, a=1.4, r=1.8, swell=None):
    dur = t1 - t0 + r
    n = int(dur * SR)
    sig = np.zeros((n, 2))
    for nm in notes:
        f = hz(nm)
        w = 1.0 if f > 90 else 0.42
        sig += pad_note(f, dur, bright) * w
    e = env_adsr(n, a, r)
    if swell is not None:  # linear gain ramp (start, end) across the chord
        e *= np.linspace(swell[0], swell[1], n)
    return sig * e[:, None] * amp / max(len(notes), 1) ** 0.5


def piano(name, vel=0.3, dur=None):
    """Additive piano: inharmonic partials, pitch-dependent two-stage decay,
    soft hammer transient, two slightly detuned strings."""
    f = hz(name)
    tau = float(np.clip(3.2 * (220 / f) ** 0.45, 0.9, 5.5))
    dur = dur or min(tau * 4.0, 9.0)
    n = int(dur * SR)
    t = t_axis(n)
    B = 0.00035
    sig = np.zeros(n)
    for k in range(1, 13):
        fk = k * f * np.sqrt(1 + B * k * k)
        if fk > 16000:
            break
        ak = (1 / k) ** 1.15 * (0.6 + 0.4 * vel) ** (k - 1)
        tk = tau / (1 + 0.45 * (k - 1))
        dec = 0.65 * np.exp(-t / (tk * 0.18)) + 0.35 * np.exp(-t / tk)
        for det in (-0.7, 0.7):  # two strings, beating gently
            sig += 0.5 * ak * dec * np.sin(2 * np.pi * (fk + det * k * 0.15) * t + rng.uniform(0, 6.28))
    att = np.minimum(1, t / 0.004)
    hammer = fft_filter(rng.standard_normal(n), lo=200, hi=2500) * np.exp(-t / 0.012) * 0.04
    sig = (sig * att + hammer) * vel
    sig *= np.cos(np.clip((t - (dur - 0.3)) / 0.3, 0, 1) * np.pi / 2) ** 2  # tail-off
    return sig


# --------------------------------------------------------------------------- sfx
def water_drop(f0=900, f1=2300, length=0.12, level=0.5):
    """Small serum droplet: a fast rising resonant chirp (the bubble 'plip')."""
    n = int(length * SR)
    t = t_axis(n)
    sweep = 0.022
    f = f0 * (f1 / f0) ** np.clip(t / sweep, 0, 1)
    ph = 2 * np.pi * np.cumsum(f) / SR
    e = np.minimum(1, t / 0.0015) * np.exp(-t / 0.028)
    body = np.sin(ph) * e
    click = fft_filter(rng.standard_normal(n), lo=3000, hi=9000) * np.exp(-t / 0.0025) * 0.15
    return (body + click) * level


def glass_tink(f=2650, level=0.12):
    n = int(1.6 * SR)
    t = t_axis(n)
    sig = np.zeros(n)
    for ratio, a, tau in [(1, 1, 0.5), (2.76, 0.5, 0.28), (5.40, 0.25, 0.15), (8.93, 0.12, 0.08)]:
        sig += a * np.sin(2 * np.pi * f * ratio * t) * np.exp(-t / tau)
    return sig * np.minimum(1, t / 0.002) * level


def airy(dur, level):
    """Breath of air: band-passed noise with a slow swell (macro skin shot)."""
    n = int(dur * SR)
    x = fft_filter(rng.standard_normal((n, 2)), lo=2500, hi=9000, slope=1)
    e = np.sin(np.linspace(0, np.pi, n)) ** 1.5
    return x * e[:, None] * level


def room_tone(dur, level):
    n = int(dur * SR)
    x = fft_filter(rng.standard_normal((n, 2)), lo=60, hi=500, slope=1)
    return x * env_adsr(n, 0.6, 0.8)[:, None] * level


def skin_touch(level):
    n = int(0.55 * SR)
    t = t_axis(n)
    x = fft_filter(rng.standard_normal(n), lo=900, hi=4500, slope=1)
    e = np.sin(np.clip(t / 0.55, 0, 1) * np.pi) ** 2
    return x * e * level


def soft_accent(level):
    """Low-impact musical accent for the reveal: a rounded sub swell (G1)."""
    n = int(2.4 * SR)
    t = t_axis(n)
    f = hz("G1")
    sig = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(4 * np.pi * f * t)
    e = np.minimum(1, t / 0.035) * np.exp(-t / 0.7)
    return sig * e * level


def low_atmos(dur, level):
    n = int(dur * SR)
    x = fft_filter(rng.standard_normal((n, 2)), lo=30, hi=140, slope=2)
    return x * env_adsr(n, 1.2, 1.5)[:, None] * level


# --------------------------------------------------------------------------- reverb
def reverb(x, rt=3.2, predelay=0.018, damp_hz=5200):
    n_ir = int(rt * SR)
    t = t_axis(n_ir)
    ir = rng.standard_normal((n_ir, 2)) * np.exp(-6.9 * t / rt)[:, None]
    ir = fft_filter(ir, lo=120, hi=damp_hz, slope=1)
    dark_tail = fft_filter(rng.standard_normal((n_ir, 2)), hi=1800) * np.exp(-6.9 * t / (rt * 1.25))[:, None]
    ir = ir + 0.6 * dark_tail
    ir = np.concatenate([np.zeros((int(predelay * SR), 2)), ir])
    ir /= np.sqrt((ir ** 2).sum(0, keepdims=True))
    n = len(x) + len(ir)
    nfft = 1 << (n - 1).bit_length()
    y = np.fft.irfft(np.fft.rfft(x, nfft, axis=0) * np.fft.rfft(ir, nfft, axis=0), nfft, axis=0)
    return y[: len(x)]


# --------------------------------------------------------------------------- arrange
def build():
    music = np.zeros((N + SR * 8, 2))
    sfx = np.zeros_like(music)

    c = CUES
    # Harmony: D major colour, never resolving fully until the packshot.
    chords = [
        (["D2", "A2", "E3", "F#3", "C#4"], 0.0, c["cut_skin"] + 0.3, 0.22, 0.10, (0.35, 1.0)),
        (["B1", "F#2", "D3", "C#4"], c["cut_skin"], c["cut_formula"] + 0.3, 0.24, 0.18, None),
        (["G1", "D2", "B2", "F#3"], c["cut_formula"], c["cut_ritual"] + 0.3, 0.24, 0.22, None),
        (["E2", "B2", "D3", "F#3"], c["cut_ritual"], c["cut_reveal"] + 0.3, 0.24, 0.24, None),
        (["G1", "D2", "B2", "F#3", "A3"], c["cut_reveal"], 20.2, 0.26, 0.30, (0.8, 1.15)),   # the rise
        (["A1", "E2", "D3", "E3", "A3"], 20.0, c["dissolve_sig"] + 0.2, 0.30, 0.40, (1.0, 1.45)),
        (["D2", "A2", "F#3", "E4", "A4"], c["dissolve_sig"], 31.0, 0.34, 0.32, None),   # resolution
    ]
    for notes, t0, t1, amp, bright, swell in chords:
        place(music, pad_chord(notes, t0, t1, amp, bright, swell=swell), t0)
    # high shimmer joining for the rise
    place(music, pad_chord(["A4", "D5"], 19.5, c["dissolve_sig"], 0.07, 0.05, a=3.0, swell=(0.2, 1.0)), 19.5)

    motif = [
        (1.20, "A4", .30), (2.90, "F#5", .26), (c["cut_skin"], "E5", .28), (6.00, "C#5", .24),
        (7.40, "D5", .22), (c["cut_formula"], "B4", .26), (10.70, "F#5", .22),
        (c["cut_ritual"], "D5", .26), (c["first_touch"], "A4", .2), (15.0, "B4", .18),
        (c["cut_reveal"], "G2", .40), (c["cut_reveal"] + 0.01, "D3", .30), (c["cut_reveal"] + 0.03, "B4", .26),
        (17.6, "F#5", .26), (19.0, "A5", .24), (20.0, "E5", .28), (21.2, "A5", .28),
        (22.2, "B5", .26), (23.1, "C#6", .24),
        (c["dissolve_sig"], "D3", .38), (c["dissolve_sig"] + 0.035, "A3", .32),
        (c["dissolve_sig"] + 0.07, "F#4", .30), (c["dissolve_sig"] + 0.105, "D5", .30),
        (c["brand_in"], "A5", .24), (c["tagline_in"], "D6", .22), (28.0, "F#5", .14),
    ]
    for t0, nm, v in motif:
        pan = float(np.clip((hz(nm) - 400) / 900, -0.4, 0.4))
        place(music, piano(nm, v), t0, pan=pan)

    # --- sound design, synced to picture
    place(sfx, low_atmos(c["cut_skin"] + 1.5, 0.22), 0.0)
    place(sfx, glass_tink(2650, 0.07), 0.85, pan=-0.2)                    # pipette glass catches light
    place(sfx, water_drop(820, 2100, level=0.32), c["cut_skin"] - 0.12, pan=-0.1)  # sound bridge into skin
    place(sfx, airy(c["cut_formula"] - c["cut_skin"] + 0.6, 0.035), c["cut_skin"] - 0.2)
    place(sfx, glass_tink(3100, 0.04), c["cut_formula"] + 0.2, pan=0.2)
    place(sfx, water_drop(950, 2500, level=0.42), c["drop_release"], pan=0.05)  # drop separates
    place(sfx, water_drop(1500, 3200, length=0.07, level=0.12), c["drop_release"] + 0.11, pan=0.1)
    place(sfx, room_tone(c["cut_reveal"] - c["cut_ritual"] + 0.6, 0.09), c["cut_ritual"])
    place(sfx, skin_touch(0.05), c["first_touch"] - 0.15, pan=0.15)
    place(sfx, skin_touch(0.035), c["first_touch"] + 0.75, pan=0.1)
    place(sfx, soft_accent(0.22), c["cut_reveal"])

    wet_m = reverb(music, rt=3.6)
    wet_s = reverb(sfx, rt=2.2, damp_hz=7000)
    mix = music * 0.78 + wet_m * 0.42 + sfx * 0.9 + wet_s * 0.22
    mix = fft_filter(mix, lo=38, slope=2)  # clean sub rumble
    mix = mix[:N]
    # final musical fade: gentle, ending in near-silence on the last frame
    fade = int(2.2 * SR)
    mix[-fade:] *= (np.cos(np.linspace(0, np.pi / 2, fade)) ** 1.6)[:, None]
    # tiny fade-in so the very first sample is silent
    fi = int(0.05 * SR)
    mix[:fi] *= np.linspace(0, 1, fi)[:, None]
    mix /= np.abs(mix).max() / 0.8
    BUILD.mkdir(exist_ok=True)
    mix.astype("<f4").tofile(BUILD / "soundtrack_f32.raw")
    print("soundtrack written", mix.shape)


if __name__ == "__main__":
    build()
