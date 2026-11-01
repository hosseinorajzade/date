# Synthesizes the teaser score (dark cinematic electronic, 120 BPM, D minor, heavy bass) and the SFX bed
# from remotion/src/timeline.json, so every whoosh/impact/riser/click lands on the cut it belongs to.
# Output: audio/music.wav, audio/sfx.wav (48 kHz stereo float), mixed + mastered later with ffmpeg.
import json, numpy as np
from scipy import signal
from scipy.io import wavfile

B = '/home/user/date/daewoo_teaser'
TL = json.load(open(f'{B}/remotion/src/timeline.json'))
SR = 48000
DUR = TL['total']
N = int(DUR * SR)
BEAT = 60 / TL['bpm']
S16 = BEAT / 4
rng = np.random.default_rng(7)


def buf():
    return np.zeros((N, 2), np.float64)


def at(t):
    return int(round(t * SR))


def add(dst, x, t, gain=1.0, pan=0.0):
    """Mix mono/stereo x into dst at time t with equal-power pan."""
    if x.ndim == 1:
        l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
        x = np.stack([x * l, x * r], 1) * np.sqrt(2)
    i = at(t)
    if i >= N:
        return
    if i < 0:
        x = x[-i:]
        i = 0
    n = min(len(x), N - i)
    dst[i:i + n] += x[:n] * gain


def note(n):  # midi -> Hz
    return 440.0 * 2 ** ((n - 69) / 12)


def polyblep_saw(freq, dur, phase0=0.0):
    n = int(dur * SR)
    dt = freq / SR
    ph = (phase0 + dt * np.arange(n)) % 1.0
    y = 2 * ph - 1
    m = ph < dt
    t = ph[m] / dt
    y[m] -= t + t - t * t - 1
    m = ph > 1 - dt
    t = (ph[m] - 1) / dt
    y[m] -= t * t + t + t + 1
    return y


def lp(x, fc, order=2):
    sos = signal.butter(order, min(fc, SR * 0.45), 'low', fs=SR, output='sos')
    return signal.sosfilt(sos, x, axis=0)


def hp(x, fc, order=2):
    sos = signal.butter(order, fc, 'high', fs=SR, output='sos')
    return signal.sosfilt(sos, x, axis=0)


def bp(x, f1, f2, order=2):
    sos = signal.butter(order, [f1, min(f2, SR * 0.45)], 'band', fs=SR, output='sos')
    return signal.sosfilt(sos, x, axis=0)


def sweep_lp(x, f_start, f_end, block=512, q=0.9):
    """Time-varying low-pass (exponential cutoff sweep) with filter state carried between blocks."""
    out = np.zeros_like(x)
    nb = int(np.ceil(len(x) / block))
    zi = None
    for b in range(nb):
        fc = f_start * (f_end / f_start) ** (b / max(1, nb - 1))
        bb, aa = signal.iirfilter(2, min(fc, SR * 0.45), btype='low', ftype='butter', fs=SR)
        seg = x[b * block:(b + 1) * block]
        if zi is None:
            zi = signal.lfilter_zi(bb, aa) * 0
            zi = np.stack([zi] * x.shape[1], 1) if x.ndim > 1 else zi
        y, zi = signal.lfilter(bb, aa, seg, axis=0, zi=zi)
        out[b * block:(b + 1) * block] = y
    return out


def env_ad(n, a, d, curve=4.0):
    t = np.arange(n) / SR
    e = np.where(t < a, t / max(a, 1e-6), np.exp(-(t - a) / max(d, 1e-6) * curve / 4))
    return e


def make_ir(rt=2.4, predelay=0.02, bright=5000):
    n = int(rt * SR)
    t = np.arange(n) / SR
    ir = rng.standard_normal((n, 2)) * np.exp(-6.9 * t / rt)[:, None]
    ir = lp(ir, bright)
    ir[: int(predelay * SR)] = 0
    return ir / np.sqrt((ir ** 2).sum(0))


IR_BIG = make_ir(2.8, 0.03, 4500)
IR_ROOM = make_ir(1.1, 0.01, 6000)


def reverb(x, ir, mix):
    if x.ndim == 1:
        x = np.stack([x, x], 1)
    wet = np.stack([signal.fftconvolve(x[:, c], ir[:, c])[: len(x)] for c in range(2)], 1)
    return x * (1 - mix) + wet * mix


# ---------------------------------------------------------------- instruments
def kick(punch=1.0):
    n = int(0.55 * SR)
    t = np.arange(n) / SR
    f = 42 + 118 * np.exp(-t / 0.045)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-t / 0.32)
    click = hp(rng.standard_normal(n), 2500) * np.exp(-t / 0.004) * 0.35
    return np.tanh((body + click) * 1.6 * punch) * 0.9


def clap():
    n = int(0.45 * SR)
    t = np.arange(n) / SR
    nz = bp(rng.standard_normal(n), 900, 3800)
    e = np.zeros(n)
    for k, d in enumerate([0, 0.011, 0.022]):
        i = int(d * SR)
        e[i:] += np.exp(-(t[: n - i]) / (0.006 if k < 2 else 0.16))
    return reverb(nz * e * 0.8, IR_ROOM, 0.35)


def hat(open_=False):
    n = int((0.32 if open_ else 0.06) * SR)
    t = np.arange(n) / SR
    nz = hp(rng.standard_normal(n), 7500, 4)
    return nz * np.exp(-t / (0.11 if open_ else 0.014)) * 0.5


def snare_hit():
    n = int(0.25 * SR)
    t = np.arange(n) / SR
    tone = np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.05)
    nz = bp(rng.standard_normal(n), 1500, 9000) * np.exp(-t / 0.07)
    return (tone * 0.5 + nz) * 0.6


def pad_chord(notes, dur, cutoff=1300, detune=0.12):
    n = int(dur * SR)
    out = np.zeros((n, 2))
    for m in notes:
        for k, cents in enumerate(np.linspace(-detune, detune, 5)):
            f = note(m) * 2 ** (cents / 12)
            s = polyblep_saw(f, dur, rng.random())
            pan = np.linspace(-0.7, 0.7, 5)[k]
            out[:, 0] += s * np.cos((pan + 1) * np.pi / 4)
            out[:, 1] += s * np.sin((pan + 1) * np.pi / 4)
    out = lp(out, cutoff, 2) / (len(notes) * 5)
    e = np.minimum(1, np.arange(n) / (0.9 * SR)) * np.minimum(1, (n - np.arange(n)) / (0.6 * SR))
    return out * e[:, None]


def reese(m, dur, cutoff=420):
    f = note(m)
    s = polyblep_saw(f * 0.993, dur, 0.1) + polyblep_saw(f * 1.007, dur, 0.6)
    sub = np.sin(2 * np.pi * f / 2 * np.arange(int(dur * SR)) / SR) * 0.9
    x = lp(s * 0.5, cutoff, 4) + sub
    n = len(x)
    e = np.minimum(1, np.arange(n) / (0.004 * SR)) * np.minimum(1, (n - np.arange(n)) / (0.01 * SR))
    return np.tanh(x * 1.4 * e) * 0.6


def pluck(m, dur=0.22):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = polyblep_saw(note(m), dur, rng.random()) + 0.5 * polyblep_saw(note(m) * 2.003, dur)
    s = lp(s, 2600, 2) * np.exp(-t / 0.07)
    return s * 0.35


def impact(size=1.0):
    n = int(2.6 * SR)
    t = np.arange(n) / SR
    f = 30 + 70 * np.exp(-t / 0.12)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / (0.9 * size))
    crack = lp(rng.standard_normal(n), 5000) * np.exp(-t / 0.05)
    tail = lp(rng.standard_normal(n), 1800) * np.exp(-t / 0.5) * 0.25
    x = np.tanh((boom * 1.4 + crack * 0.6 + tail) * 1.3)
    return reverb(x, IR_BIG, 0.3) * size


def riser(dur, f0=300, f1=6000, tone=True):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = rng.standard_normal((n, 2)) * 0.6
    x = sweep_lp(hp(x, 200), f0, f1)
    e = (t / dur) ** 2.2
    out = x * e[:, None]
    if tone:
        fr = 180 * (8 ** (t / dur))
        out += (np.sin(2 * np.pi * np.cumsum(fr) / SR) * e * 0.25)[:, None]
    return out


def whoosh(dur=0.5, f0=400, f1=5000, peak=0.6, pan_move=0.8):
    n = int(dur * SR)
    t = np.arange(n) / SR
    nz = rng.standard_normal(n)
    up = sweep_lp(nz[:, None], f0, f1)[:, 0]
    e = np.where(t < peak * dur, (t / (peak * dur)) ** 2, np.exp(-(t - peak * dur) / (0.18 * dur)))
    x = hp(up, 150) * e
    pan = np.linspace(-pan_move, pan_move, n)
    return np.stack([x * np.cos((pan + 1) * np.pi / 4), x * np.sin((pan + 1) * np.pi / 4)], 1) * 1.2


def glitch_burst(dur=0.35):
    n = int(dur * SR)
    out = np.zeros(n)
    i = 0
    while i < n:
        seg = int(rng.uniform(0.012, 0.045) * SR)
        f = rng.choice([180, 360, 720, 1440, 2880])
        tt = np.arange(seg) / SR
        kind = rng.integers(3)
        if kind == 0:
            s = np.sign(np.sin(2 * np.pi * f * tt))
        elif kind == 1:
            s = rng.standard_normal(seg)
        else:
            s = np.zeros(seg)
        s = np.round(s * 6) / 6  # crush
        out[i:i + seg] = s[: n - i] * 0.5
        i += seg
    return hp(out, 120)


def click(bright=1.0):
    n = int(0.03 * SR)
    t = np.arange(n) / SR
    return hp(rng.standard_normal(n), 2000 * bright) * np.exp(-t / 0.003) * 0.9 + np.sin(2 * np.pi * 1800 * t) * np.exp(-t / 0.006) * 0.3


def key_click():
    n = int(0.06 * SR)
    t = np.arange(n) / SR
    x = bp(rng.standard_normal(n), 1800, 7000) * np.exp(-t / 0.008) + np.sin(2 * np.pi * 3200 * t) * np.exp(-t / 0.004) * 0.2
    return x * 0.8


def shimmer(dur=1.2):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = np.zeros(n)
    for m in [74, 77, 81, 86, 89]:
        x += np.sin(2 * np.pi * note(m) * t + rng.random() * 6) * np.exp(-t / 0.6)
    x *= np.minimum(1, t / 0.15)
    return reverb(x * 0.12, IR_BIG, 0.5)


# ---------------------------------------------------------------- score
music = buf()
drums = buf()
bass = buf()

# chord plan (2 bars = 4 s each): Dm | Bb | Gm | A  (D minor, dark)
CH = {'Dm': [50, 53, 57, 62], 'Bb': [46, 50, 53, 58], 'Gm': [43, 50, 55, 58], 'A': [45, 49, 52, 57], 'F': [41, 48, 53, 57]}
ROOT = {'Dm': 38, 'Bb': 34, 'Gm': 31, 'A': 33, 'F': 29}
plan = [(0, 'Dm'), (6, 'Dm'), (10, 'Bb'), (14, 'Gm'), (18, 'A'), (22, 'Dm'), (26, 'Bb'), (30, 'Gm'), (33, 'Dm'), (38, 'Dm')]
ends = [p[0] for p in plan[1:]] + [DUR]

# pads everywhere (quiet in groove, forward in intro/break/end)
for (t0, ch), t1 in zip(plan, ends):
    lvl = 0.55 if t0 < 6 or t0 >= 33 else 0.32
    cut = 900 if t0 < 6 else (1600 if t0 < 33 else 1100)
    add(music, pad_chord(CH[ch], t1 - t0 + 0.6, cut), t0, lvl)

# sub drone in intro & break
for t0, t1 in [(0, 6), (33, 38)]:
    d = t1 - t0
    tt = np.arange(int(d * SR)) / SR
    drone = np.sin(2 * np.pi * note(26) * tt) * np.minimum(1, tt / 1.0) * np.minimum(1, (d - tt) / 0.3)
    add(music, drone * 0.35, t0)

# drums
def in_groove(t):
    return 6 <= t < 33 and not (21.75 <= t < 22)

beats = np.arange(0, DUR, BEAT)
for b in beats:
    if in_groove(b):
        add(drums, kick(), b, 0.95)
    k = int(round(b / BEAT))
    if in_groove(b) and k % 2 == 1:
        add(drums, clap(), b, 0.55)
for s in np.arange(0, DUR, S16):
    k = int(round(s / S16))
    if 1.0 <= s < 6:  # intro ticking hats, growing
        add(drums, hat(), s, 0.08 + 0.18 * (s - 1) / 5 * (k % 2 == 0), pan=0.3 if k % 4 == 2 else -0.2)
    elif in_groove(s):
        if k % 4 == 2:
            add(drums, hat(open_=s >= 22), s, 0.33 if s >= 22 else 0.28, pan=0.15)
        elif s >= 14:
            add(drums, hat(), s, 0.12 + 0.05 * (k % 2 == 0), pan=-0.25)
    elif 33.5 <= s < 36:  # break: soft ticks under the typing
        if k % 2 == 0:
            add(drums, hat(), s, 0.07, pan=0.4)

# heartbeat kicks at the Charisma hit, and the accelerating build into the end
add(drums, kick(1.3), 3.0, 1.0)
for b in [36.0, 36.5, 37.0, 37.25, 37.5, 37.625, 37.75]:
    add(drums, kick(0.9), b, 0.7)
# snare rolls (fills) before 22 and 38
for t0, t1 in [(21.0, 22.0), (37.0, 37.875)]:
    steps = np.arange(t0, t1, S16 / 2)
    for i, s in enumerate(steps):
        add(drums, snare_hit(), s, 0.15 + 0.45 * i / len(steps))

# reese bass: 8th-note pulse on chord root, octave jump on the "and" of beat 4
for (t0, ch), t1 in zip(plan, ends):
    if t0 < 6 or t0 >= 33:
        continue
    for e in np.arange(t0, min(t1, 33), BEAT / 2):
        if 21.75 <= e < 22:
            continue
        k = int(round((e - t0) / (BEAT / 2)))
        m = ROOT[ch] + (12 if k % 8 == 7 else 0)
        add(bass, reese(m, BEAT / 2 * 0.92, 380 + 300 * (e >= 22)), e, 0.75)

# arp in the second half of the groove
for (t0, ch), t1 in zip(plan, ends):
    if not (22 <= t0 < 33):
        continue
    tones = CH[ch][1:] + [CH[ch][1] + 12]
    for i, s in enumerate(np.arange(t0, min(t1, 33), S16)):
        add(music, pluck(tones[i % len(tones)] + 12), s, 0.33, pan=0.45 * np.sin(i * 0.7))

# sidechain: duck pads/bass under every groove kick
duck = np.ones(N)
for b in beats:
    if in_groove(b):
        i = at(b)
        L = int(0.22 * SR)
        e = 1 - 0.65 * np.exp(-np.arange(L) / (0.06 * SR))
        duck[i:i + L] = np.minimum(duck[i:i + L], e[: max(0, min(L, N - i))])
music *= duck[:, None]
bass *= duck[:, None]

# risers and the big hits in the score
add(music, riser(2.0, 250, 7000), 4.0, 0.5)
add(music, riser(1.0, 400, 6000), 32.0, 0.35)
add(music, riser(2.0, 200, 8000), 36.0, 0.55)
add(music, impact(1.2), 0.0, 0.9)
add(music, impact(0.8), 6.0, 0.55)
add(music, impact(1.5), 38.0, 1.0)

music = reverb(music, IR_BIG, 0.18) + drums + bass
# silence the gap right before the final hit, then fade the score out during the ending
gap = np.ones(N)
g0, g1 = at(37.875), at(38.0)
gap[g0:g1] = np.linspace(1, 0.05, g1 - g0)
fade = np.ones(N)
f0, f1 = at(40.5), at(43.0)
fade[f0:f1] = np.linspace(1, 0, f1 - f0) ** 1.6
music *= (gap * fade)[:, None]

# ---------------------------------------------------------------- SFX
sfx = buf()
for tr in TL['transitions']:
    t, kind = tr['t'], tr['type']
    if kind == 'open':
        add(sfx, glitch_burst(0.4), 0.0, 0.35)
    elif kind == 'whipH':
        add(sfx, whoosh(0.45, 600, 9000, 0.75, 0.9), t - 0.34, 0.8)
    elif kind == 'flash':
        add(sfx, whoosh(0.3, 1500, 12000, 0.8, 0.2), t - 0.24, 0.5)
        add(sfx, impact(0.5), t, 0.55)
    elif kind == 'zoomIn':
        add(sfx, whoosh(0.7, 200, 6000, 0.85, 0.3), t - 0.6, 0.85)
        add(sfx, impact(0.4), t, 0.4)
    elif kind == 'glitch':
        add(sfx, glitch_burst(0.32), t - 0.1, 0.5)
        add(sfx, impact(0.35), t, 0.4)
    elif kind == 'sweep':
        add(sfx, whoosh(0.6, 800, 11000, 0.7, -0.9), t - 0.42, 0.75)
    elif kind == 'whipV':
        add(sfx, whoosh(0.4, 500, 8000, 0.8, 0.0), t - 0.32, 0.8)
        add(sfx, impact(0.3), t, 0.35)
    elif kind == 'redFlash':
        add(sfx, impact(0.6), t, 0.55)
        add(sfx, whoosh(0.3, 1000, 10000, 0.8, 0.5), t - 0.24, 0.45)
    elif kind == 'spin':
        add(sfx, whoosh(0.8, 7000, 300, 0.25, -0.3), t - 0.15, 0.7)
    elif kind == 'glitchOut':
        add(sfx, glitch_burst(0.2), t - 0.2, 0.45)

# short riser into every title, landing on the title's first frame
for ti in TL['titles']:
    add(sfx, riser(0.45, 900, 9000, tone=True), ti['in'] - 0.45, 0.32)
# "Charisma" reveal
add(sfx, riser(0.6, 500, 8000), TL['charisma']['in'] - 0.6, 0.35)
# dial: ratchet clicks while the ring turns, big click as it flips to red on the 14.5 beat
for i, s in enumerate(np.arange(14.05, 14.5, 0.0625)):
    add(sfx, click(0.8), s, 0.18 + 0.03 * i, pan=-0.2 + 0.05 * i)
add(sfx, click(1.2), 14.5, 0.6)
add(sfx, impact(0.25), 14.5, 0.3)
# accents in picture: red drum light-on (25.5) and towel neon (32.0)
add(sfx, impact(0.35), 25.5, 0.35)
add(sfx, whoosh(0.35, 3000, 12000, 0.9, 0.0), 31.7, 0.3)
# typing
ty = TL['typing']
for i, ch in enumerate(ty['text']):
    if ch != ' ':
        add(sfx, key_click(), ty['start'] + i * ty['step'], 0.42, pan=-0.15 + 0.03 * i)
# logo reveal
lg = TL['logo']
add(sfx, whoosh(0.9, 400, 12000, 0.6, -0.6), lg['wordmark'][0] - 0.1, 0.45)
add(sfx, shimmer(2.5), lg['symbol'], 0.9)
add(sfx, click(1.4), lg['symbol'], 0.35)
sfx *= fade[:, None] ** 0.5

for name, x in [('music', music), ('sfx', sfx)]:
    peak = np.abs(x).max()
    wavfile.write(f'{B}/audio/{name}.wav', SR, (x / max(peak, 1e-9) * 0.89).astype(np.float32))
    print(name, 'peak before norm', round(float(peak), 3))
