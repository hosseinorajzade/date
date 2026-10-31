"""Original, deterministic sound design for the Daewoo «۸ پیمان» reel.

    python3 audio.py out/cues.json out/audio.wav

Cue times come from index.html (window.audioCues → CONFIG), so picture and sound stay in sync.
Everything is synthesized here with numpy only (no samples, no licensing). Noise is seeded.

Palette (key: D major), calm and precise:
  - pad      : warm additive chords, one per promise (D · Bm · G · A …), resolving to a bright D in the finale
  - chimes   : one bell note per filled ۸ segment, climbing the D-major scale D5 → D6 across the 8 promises
  - ticks    : soft clicks easing out under the animated counters
  - whooshes : filtered-noise swells on transitions, panned right → left (RTL motion)
  - sub      : deep impacts on the hook and when the roof locks into place
"""
import json, sys, wave
import numpy as np

SR = 48000
cues = json.load(open(sys.argv[1]))
OUT = sys.argv[2]
DUR = cues["duration"]
N = int(DUR * SR)
rng = np.random.default_rng(cues["seed"])
t_all = np.arange(N) / SR

L = np.zeros(N); R = np.zeros(N)          # dry bus
RL = np.zeros(N); RR = np.zeros(N)        # reverb send


def hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def place(sig, at, gain=1.0, pan=0.0, send=0.0):
    """Add a mono signal at time `at` (s) with constant-power pan (-1 = left, +1 = right)."""
    i = int(round(at * SR))
    if i >= N: return
    sig = sig[: N - i] * gain
    a = (pan + 1) * np.pi / 4
    gl, gr = np.cos(a), np.sin(a)
    L[i:i + len(sig)] += sig * gl; R[i:i + len(sig)] += sig * gr
    if send:
        RL[i:i + len(sig)] += sig * gl * send; RR[i:i + len(sig)] += sig * gr * send


def place_st(sl, sr, at, gain=1.0, send=0.0):
    i = int(round(at * SR))
    n = min(len(sl), N - i)
    if n <= 0: return
    L[i:i + n] += sl[:n] * gain; R[i:i + n] += sr[:n] * gain
    if send:
        RL[i:i + n] += sl[:n] * gain * send; RR[i:i + n] += sr[:n] * gain * send


def fft_filter(x, lo=None, hi=None, slope=4):
    """Smooth band-pass in the frequency domain (zero-phase)."""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    g = np.ones_like(f)
    if hi: g *= 1 / (1 + (f / hi) ** (2 * slope))
    if lo: g *= 1 / (1 + (lo / np.maximum(f, 1e-3)) ** (2 * slope))
    return np.fft.irfft(X * g, len(x))


# ---------------------------------------------------------------- pad
def pad_voice(freq, n, detune=0.0):
    t = np.arange(n) / SR
    out = np.zeros(n)
    for d in (-detune, 0.0, detune):
        f = freq * 2 ** (d / 1200)
        ph = rng.uniform(0, 2 * np.pi)
        for h in range(1, 7):
            if f * h > 6000: break
            out += np.sin(2 * np.pi * f * h * t + ph * h) / h ** 1.6
    return out / 3


def chord(notes, start, end, gain, att=1.4, rel=1.8, bright=1.0):
    n = int((end - start + rel) * SR)
    t = np.arange(n) / SR
    env = np.minimum(1, t / att) * np.clip((end - start + rel - t) / rel, 0, 1)
    env = env ** 1.5
    sl = np.zeros(n); sr = np.zeros(n)
    for k, m in enumerate(notes):
        v = pad_voice(hz(m), n, detune=7)
        lfo = 1 + 0.12 * np.sin(2 * np.pi * (0.11 + 0.03 * k) * t + k)
        p = (k / max(1, len(notes) - 1)) * 1.2 - 0.6        # spread voices across the stereo field
        a = (p + 1) * np.pi / 4
        sl += v * lfo * np.cos(a); sr += v * lfo * np.sin(a)
    if bright < 1.0:
        sl = fft_filter(sl, hi=900 * bright + 300); sr = fft_filter(sr, hi=900 * bright + 300)
    place_st(sl * env, sr * env, start, gain=gain, send=0.35)


D, Bm, G, A = [50, 57, 62, 64, 66], [47, 54, 61, 62, 66], [43, 50, 59, 62, 66], [45, 52, 59, 61, 64]
prog = [D, Bm, G, A, D, Bm, G, A]
pS, pD = cues["promiseStart"], cues["promiseDur"]
chord([38, 50, 57, 64], 0.0, pS + 0.2, 0.05, att=0.6, rel=1.6, bright=0.5)               # hook / intro: dark Dadd9
for i, c in enumerate(prog):
    chord(c, pS + i * pD - 0.3, pS + (i + 1) * pD + 0.1, 0.045, bright=0.75)
fin = cues["finale"]
chord([43, 50, 57, 62, 64], fin["start"] - 0.2, fin["lock"] - 0.1, 0.05, att=0.8, rel=0.8, bright=0.9)  # Gadd9 lift
chord([38, 50, 57, 62, 66, 69, 74], fin["lock"] - 0.05, DUR - 1.2, 0.05, att=0.35, rel=2.0)              # bright D resolve


# ---------------------------------------------------------------- bells
def bell(freq, dur=3.2, decay=1.25):
    n = int(dur * SR); t = np.arange(n) / SR
    parts = [(1.0, 1.0, 1.0), (2.0, 0.35, 1.6), (3.01, 0.12, 2.4), (4.17, 0.08, 3.2), (0.5, 0.15, 0.7)]
    out = np.zeros(n)
    for ratio, amp, dk in parts:
        out += amp * np.sin(2 * np.pi * freq * ratio * t) * np.exp(-t * dk / decay)
    att = np.minimum(1, t / 0.004)
    return out * att * (1 + 0.04 * np.sin(2 * np.pi * 5.2 * t))


scale = [74, 76, 78, 79, 81, 83, 85, 86]               # D5 … D6: one step per promise, the ۸ "completes the octave"
for i, p in enumerate(cues["promises"]):
    place(bell(hz(scale[i])), p["fill"], gain=0.16, pan=0.35 - 0.1 * i, send=0.55)

for k, m in enumerate([74, 78, 81, 86]):                # roof locks: full D chord, rolled right→left
    place(bell(hz(m), dur=5, decay=2.2), fin["lock"] + 0.04 * k, gain=0.11, pan=0.5 - 0.33 * k, send=0.6)
place(bell(hz(86), dur=5, decay=2.4), fin["logo"] + 0.25, gain=0.10, pan=0.0, send=0.7)
place(bell(hz(93), dur=5, decay=2.0), fin["logo"] + 0.45, gain=0.05, pan=-0.2, send=0.8)


# ---------------------------------------------------------------- ticks under counters
def tick(freq=3200):
    n = int(0.03 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * freq * t) * np.exp(-t * 260) + 0.3 * rng.standard_normal(n) * np.exp(-t * 600)


for p in cues["promises"]:
    if p["counter"]:
        k = 12
        for j in range(k):                              # ease-out spacing, like the power2.out counter
            u = 1 - np.sqrt(1 - (j + 1) / k)
            place(tick(3000 + 40 * j), p["heroIn"] + u * p["countDur"], gain=0.035 * (1 - 0.5 * j / k), pan=0.1, send=0.2)
    else:                                               # word heroes: a soft air swell
        n = int(1.1 * SR); t = np.arange(n) / SR
        air = fft_filter(rng.standard_normal(n), lo=2500, hi=9000, slope=2) * np.sin(np.pi * np.minimum(1, t / 1.1)) ** 2
        place(air, p["heroIn"] - 0.1, gain=0.05, pan=0.0, send=0.3)


# ---------------------------------------------------------------- whooshes (pan right → left)
def whoosh(dur=0.9, lo=300, hi=2600, peak=0.6):
    n = int(dur * SR); t = np.arange(n) / SR
    x = fft_filter(rng.standard_normal(n), lo=lo, hi=hi, slope=2)
    env = np.where(t < peak, (t / peak) ** 2.2, np.exp(-(t - peak) * 9))
    x = x / (np.abs(x).max() + 1e-9) * env
    pan = np.linspace(0.8, -0.8, n)
    a = (pan + 1) * np.pi / 4
    return x * np.cos(a), x * np.sin(a)


for at in [cues["fly"] - 0.25] + [p["exit"] - 0.15 for p in cues["promises"]]:
    wl, wr = whoosh()
    place_st(wl, wr, at, gain=0.09, send=0.3)
wl, wr = whoosh(dur=1.7, lo=150, hi=3500, peak=1.45)    # segments fly together into the roof
place_st(wl, wr, fin["lock"] - 1.45, gain=0.12, send=0.35)
wl, wr = whoosh(dur=0.9, lo=600, hi=5000, peak=0.5)     # question appears
place_st(wl, wr, cues["question"] - 0.45, gain=0.05, send=0.3)


# ---------------------------------------------------------------- sub impacts
def sub(dur=2.4, f0=90, f1=38):
    n = int(dur * SR); t = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-t * 9)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-t * 1.8)
    click = fft_filter(rng.standard_normal(n), hi=1800, slope=2) * np.exp(-t * 70) * 0.5
    return np.tanh(1.6 * (body + click)) * np.minimum(1, t / 0.002)


place(sub(), cues["hook"] + 0.02, gain=0.55, send=0.15)
place(sub(dur=3.0, f0=80, f1=36), fin["lock"], gain=0.5, send=0.2)
place(sub(dur=1.6, f0=70, f1=45), cues["title"], gain=0.18, send=0.2)


# ---------------------------------------------------------------- reverb (seeded, decorrelated stereo IR)
def ir(seconds=3.2):
    n = int(seconds * SR); t = np.arange(n) / SR
    x = rng.standard_normal(n) * np.exp(-t * 6.9 / seconds)
    x = fft_filter(x, lo=120, hi=6500, slope=1)
    x[: int(0.012 * SR)] = 0                             # pre-delay
    return x / np.sqrt(np.sum(x ** 2))


def conv(x, h):
    m = len(x) + len(h)
    n = 1 << (m - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(h, n), n)[: len(x)]


wetL, wetR = conv(RL, ir()), conv(RR, ir())
mixL = L + 0.9 * wetL
mixR = R + 0.9 * wetR

# ---------------------------------------------------------------- master
fade = np.ones(N)
fo = int(2.4 * SR); fade[-fo:] = np.linspace(1, 0, fo) ** 2
fi = int(0.01 * SR); fade[:fi] = np.linspace(0, 1, fi)
mix = np.stack([mixL, mixR], 1) * fade[:, None]
mix = fft_filter(mix[:, 0], lo=28, slope=2), fft_filter(mix[:, 1], lo=28, slope=2)
mix = np.stack(mix, 1)
mix = mix / (np.abs(mix).max() + 1e-9) * 0.89            # -1 dBFS peak (final loudness set by ffmpeg)
mix = np.tanh(mix * 1.1) / np.tanh(1.1)
pcm = (np.clip(mix, -1, 1) * 32767).astype("<i2")
with wave.open(OUT, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print(f"wrote {OUT}  {DUR:.2f}s")
