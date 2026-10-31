"""Original, deterministic sound design for the Daewoo «۸ پیمان» reel.

    python3 audio.py out/cues.json out/audio.wav

Cue times come from index.html (window.audioCues → CONFIG), so picture and sound stay in sync.
Everything is synthesized here with numpy only (no samples, no licensing). Noise is seeded.

Palette (key: D major, 120 BPM; every promise = 2 bars):
  - groove   : four-on-the-floor kick with sidechain pumping, claps on 2 & 4, offbeat hats, 8th-note bass
  - arp      : 16th-note plucks through the chords; its filter opens across the piece to build energy
  - pad      : one chord per promise (D · Bm · G · A …); finale: G → A build, landing on a bright D
  - chimes   : one bell note per filled 8-segment, climbing the D-major scale D5 → D6
  - risers   : noise swells into every downbeat and into the finale, panned right → left (RTL motion)
  - sub      : deep impacts on the hook, the lock, and when the 8 lands as ∞
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


# ---------------------------------------------------------------- grid
BPM = cues["bpm"]; BEAT = 60.0 / BPM; BAR = 4 * BEAT
pS, pD = cues["promiseStart"], cues["promiseDur"]
fin = cues["finale"]
END_GROOVE = fin["start"] - BAR / 2           # groove drops for the finale build
D, Bm, G, A = 0, 1, 2, 3
CH = {  # (bass root midi, chord tones for pad/arp)
    D:  (38, [62, 66, 69, 73, 76]),
    Bm: (35, [59, 62, 66, 69, 73]),
    G:  (31, [59, 62, 66, 67, 71]),
    A:  (33, [57, 61, 64, 66, 69]),
}
prog = [D, Bm, G, A, D, Bm, G, A]


def chord_at(t):
    if t < pS: return D
    if t >= fin["inf"]: return D
    if t >= fin["start"]: return G if t < fin["lock"] else A
    return prog[min(7, int((t - pS) // pD))]


# sidechain: duck pad/bass/arp after every kick
duck = np.ones(N)


def add_duck(at, depth=0.55, rel=0.32):
    i = int(at * SR); n = int(rel * SR)
    if i >= N: return
    seg = 1 - depth * np.exp(-np.arange(min(n, N - i)) / (0.25 * n))
    duck[i:i + len(seg)] = np.minimum(duck[i:i + len(seg)], seg)


# ---------------------------------------------------------------- drums
def kick():
    n = int(0.42 * SR); t = np.arange(n) / SR
    f = 46 + 110 * np.exp(-t * 32)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7.5)
    click = fft_filter(rng.standard_normal(n), lo=1500, hi=7000) * np.exp(-t * 300) * 0.25
    return np.tanh(2.2 * (body + click)) * 0.8


def clap():
    n = int(0.3 * SR); t = np.arange(n) / SR
    nz = fft_filter(rng.standard_normal(n), lo=900, hi=6000, slope=2)
    env = np.exp(-t * 22) + 0.6 * np.exp(-np.maximum(0, t - 0.012) * 30) * (t > 0.012) + 0.5 * np.exp(-np.maximum(0, t - 0.024) * 26) * (t > 0.024)
    tone = np.sin(2 * np.pi * 190 * t) * np.exp(-t * 40) * 0.4
    x = nz / (np.abs(nz).max() + 1e-9) * env + tone
    return x


HAT = fft_filter(rng.standard_normal(int(0.08 * SR)), lo=7000, hi=16000, slope=2)
HAT = HAT / np.abs(HAT).max()


def hat(open_=False):
    n = len(HAT); t = np.arange(n) / SR
    return HAT * np.exp(-t * (28 if open_ else 75))


KICK, CLAP = kick(), clap()

intro_hats = pS - 2 * BAR        # bar 1
intro_kick = pS - BAR            # bar 2
t = 0.0; b = 0
while t < DUR - 0.01:
    in_main = pS <= t < END_GROOVE
    in_out = fin["inf"] <= t < DUR - 2.2
    beat_in_bar = b % 4
    # kick: four-on-the-floor from bar 2, half-time in the outro
    if (intro_kick <= t < END_GROOVE) or (in_out and beat_in_bar in (0, 2)):
        place(KICK, t, gain=0.62 if in_main or in_out else 0.45, send=0.03)
        add_duck(t)
    # clap on 2 and 4
    if in_main and beat_in_bar in (1, 3):
        place(CLAP, t, gain=0.16, pan=-0.05, send=0.25)
    # hats: offbeat 8ths, ghost 16ths in the main section
    if intro_hats <= t < END_GROOVE or in_out:
        place(hat(open_=beat_in_bar == 3 and in_main), t + BEAT / 2, gain=0.085, pan=0.25, send=0.05)
        if in_main:
            place(hat(), t + BEAT / 4, gain=0.03, pan=0.35)
            place(hat(), t + 3 * BEAT / 4, gain=0.035, pan=0.15)
    t += BEAT; b += 1

# ---------------------------------------------------------------- bass (8ths, ducked)
bass = np.zeros(N)
t = intro_kick
while t < DUR - 2.2:
    if END_GROOVE <= t < fin["inf"]:
        t += BEAT / 2; continue
    root = CH[chord_at(t + 0.01)][0]
    off = int(round((t - intro_kick) / (BEAT / 2))) % 2   # octave bounce on the offbeat
    f = hz(root + 12 * off + 12)
    n = int(BEAT / 2 * SR * 0.92); tt = np.arange(n) / SR
    v = sum(np.sin(2 * np.pi * f * h * tt) / h ** 1.2 for h in range(1, 6))
    v *= np.minimum(1, tt / 0.004) * np.exp(-tt * 5) * np.minimum(1, (n / SR - tt) / 0.01)
    i = int(t * SR); m = min(n, N - i)
    bass[i:i + m] += v[:m]
    t += BEAT / 2
bass = fft_filter(bass, hi=420, slope=2) * duck * 0.26
L += bass; R += bass

# ---------------------------------------------------------------- arp (16th plucks)
def pluck(freq, dur=0.22):
    n = int(dur * SR); tt = np.arange(n) / SR
    v = sum(np.sin(2 * np.pi * freq * h * tt) * np.exp(-tt * (14 + 6 * h)) / h for h in range(1, 7))
    return v * np.minimum(1, tt / 0.002)


arpL = np.zeros(N); arpR = np.zeros(N)
pattern = [0, 2, 4, 2, 1, 3, 4, 3]
t = pS - 2 * BAR; j = 0
while t < DUR - 2.4:
    if END_GROOVE <= t < fin["inf"]:
        t += BEAT / 4; j += 1; continue
    tones = CH[chord_at(t + 0.01)][1]
    note = tones[pattern[j % 8]] + (12 if (j // 8) % 2 else 0)
    v = pluck(hz(note)) * (1.0 if j % 4 == 0 else 0.65)
    i = int(t * SR); m = min(len(v), N - i)
    pan = 0.45 if j % 2 else -0.45
    a_ = (pan + 1) * np.pi / 4
    arpL[i:i + m] += v[:m] * np.cos(a_); arpR[i:i + m] += v[:m] * np.sin(a_)
    t += BEAT / 4; j += 1
# filter opens over the piece (builds energy), intro is darker
cut = np.interp(t_all, [0, pS, fin["start"], DUR], [900, 2200, 5200, 4200])
arpL2 = np.zeros(N); arpR2 = np.zeros(N)
for lo_t, hi_t in zip(np.arange(0, DUR, 2.0), np.arange(2.0, DUR + 2.0, 2.0)):
    i0, i1 = int(lo_t * SR), min(N, int(hi_t * SR))
    c = float(cut[(i0 + i1) // 2])
    pad_ = int(0.05 * SR); a0 = max(0, i0 - pad_)
    fl = fft_filter(arpL[a0:i1], hi=c, slope=2); fr = fft_filter(arpR[a0:i1], hi=c, slope=2)
    arpL2[i0:i1] = fl[i0 - a0:]; arpR2[i0:i1] = fr[i0 - a0:]
L += arpL2 * duck * 0.055; R += arpR2 * duck * 0.055
RL += arpL2 * duck * 0.03; RR += arpR2 * duck * 0.03


# ---------------------------------------------------------------- pad (ducked)
def pad_voice(freq, n, detune=0.0):
    tt = np.arange(n) / SR
    out = np.zeros(n)
    for dd in (-detune, 0.0, detune):
        f = freq * 2 ** (dd / 1200)
        ph = rng.uniform(0, 2 * np.pi)
        for h in range(1, 7):
            if f * h > 6000: break
            out += np.sin(2 * np.pi * f * h * tt + ph * h) / h ** 1.6
    return out / 3


padL = np.zeros(N); padR = np.zeros(N)


def chord(notes, start, end, gain, att=0.5, rel=0.8):
    n = int((end - start + rel) * SR); tt = np.arange(n) / SR
    env = (np.minimum(1, tt / att) * np.clip((end - start + rel - tt) / rel, 0, 1)) ** 1.5
    i = int(start * SR); m = min(n, N - i)
    for k, mn in enumerate(notes):
        v = pad_voice(hz(mn), n, detune=8) * env * gain
        pan = (k / max(1, len(notes) - 1)) * 1.2 - 0.6; a_ = (pan + 1) * np.pi / 4
        padL[i:i + m] += v[:m] * np.cos(a_); padR[i:i + m] += v[:m] * np.sin(a_)


chord([50, 57, 62, 64, 69], 0.0, pS, 0.05, att=0.2, rel=0.6)
for i, c in enumerate(prog):
    chord([n - 12 for n in CH[c][1][:4]], pS + i * pD - 0.05, pS + (i + 1) * pD, 0.04)
chord([55, 62, 67, 69], fin["start"] - 0.05, fin["lock"], 0.05, att=0.3, rel=0.3)
chord([57, 61, 64, 66, 69], fin["lock"] - 0.05, fin["inf"], 0.055, att=0.2, rel=0.2)
chord([50, 57, 62, 66, 69, 74], fin["inf"] - 0.02, DUR - 1.0, 0.055, att=0.05, rel=1.4)
padL = fft_filter(padL, hi=2600); padR = fft_filter(padR, hi=2600)
L += padL * duck; R += padR * duck
RL += padL * 0.3; RR += padR * 0.3


# ---------------------------------------------------------------- bells
def bell(freq, dur=2.4, decay=0.9):
    n = int(dur * SR); tt = np.arange(n) / SR
    parts = [(1.0, 1.0, 1.0), (2.0, 0.35, 1.6), (3.01, 0.12, 2.4), (4.17, 0.08, 3.2), (0.5, 0.15, 0.7)]
    out = np.zeros(n)
    for ratio, amp, dk in parts:
        out += amp * np.sin(2 * np.pi * freq * ratio * tt) * np.exp(-tt * dk / decay)
    return out * np.minimum(1, tt / 0.003)


scale = [74, 76, 78, 79, 81, 83, 85, 86]               # D5 … D6: one step per filled segment
for i, p in enumerate(cues["promises"]):
    place(bell(hz(scale[i])), p["fill"], gain=0.2, pan=0.35 - 0.1 * i, send=0.45)
for k, m in enumerate([74, 78, 81, 86]):
    place(bell(hz(m), dur=4, decay=1.8), fin["inf"] + 0.03 * k, gain=0.13, pan=0.5 - 0.33 * k, send=0.55)
place(bell(hz(86), dur=4, decay=2.0), fin["logo"], gain=0.11, send=0.6)
place(bell(hz(93), dur=4, decay=1.6), fin["logo"] + BEAT / 2, gain=0.05, pan=-0.2, send=0.7)


# ---------------------------------------------------------------- ticks under counters
def tick(freq=3200):
    n = int(0.03 * SR); tt = np.arange(n) / SR
    return np.sin(2 * np.pi * freq * tt) * np.exp(-tt * 260) + 0.3 * rng.standard_normal(n) * np.exp(-tt * 600)


for p in cues["promises"]:
    if p["counter"]:
        k = 10
        for j in range(k):
            u = 1 - np.sqrt(1 - (j + 1) / k)
            place(tick(3000 + 50 * j), p["heroIn"] + u * p["countDur"], gain=0.03, pan=0.1, send=0.15)


# ---------------------------------------------------------------- whooshes / risers (pan right → left)
def whoosh(dur=0.6, lo=400, hi=3500, peak=None):
    peak = dur * 0.8 if peak is None else peak
    n = int(dur * SR); tt = np.arange(n) / SR
    x = fft_filter(rng.standard_normal(n), lo=lo, hi=hi, slope=2)
    env = np.where(tt < peak, (tt / peak) ** 2.5, np.exp(-(tt - peak) * 14))
    x = x / (np.abs(x).max() + 1e-9) * env
    pan = np.linspace(0.8, -0.8, n); a_ = (pan + 1) * np.pi / 4
    return x * np.cos(a_), x * np.sin(a_)


for at in [pS + i * pD for i in range(1, 8)]:            # into every promise downbeat
    wl, wr = whoosh(); place_st(wl, wr, at - 0.48, gain=0.08, send=0.25)
wl, wr = whoosh(dur=BAR, lo=300, hi=6000, peak=BAR - 0.02)  # riser into the main groove
place_st(wl, wr, pS - BAR, gain=0.08, send=0.3)
wl, wr = whoosh(dur=fin["lock"] - END_GROOVE, lo=250, hi=7000, peak=fin["lock"] - END_GROOVE - 0.02)
place_st(wl, wr, END_GROOVE, gain=0.11, send=0.3)          # build: segments gather
wl, wr = whoosh(dur=fin["inf"] - fin["lock"], lo=500, hi=8000, peak=fin["inf"] - fin["lock"] - 0.02)
place_st(wl, wr, fin["lock"], gain=0.09, send=0.3)         # 8 turns into ∞


# ---------------------------------------------------------------- sub impacts
def sub(dur=2.0, f0=90, f1=38):
    n = int(dur * SR); tt = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-tt * 9)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 2.2)
    click = fft_filter(rng.standard_normal(n), hi=1800, slope=2) * np.exp(-tt * 70) * 0.5
    return np.tanh(1.6 * (body + click)) * np.minimum(1, tt / 0.002)


place(sub(), cues["hook"] + 0.01, gain=0.55, send=0.15)
place(sub(dur=1.4, f0=80, f1=45), fin["lock"], gain=0.35, send=0.2)
place(sub(dur=2.6, f0=85, f1=36), fin["inf"], gain=0.55, send=0.2)
wl, wr = whoosh(dur=1.2, lo=2500, hi=12000, peak=0.01)    # cymbal-like air on the ∞ landing
place_st(wl * 0.6, wr * 0.6, fin["inf"], gain=0.08, send=0.4)


# ---------------------------------------------------------------- reverb (seeded, decorrelated stereo IR)
def ir(seconds=2.2):
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
