"""Synthesised sound effects for the ten Beribus TikTok videos.

Every sound is generated from sine waves and filtered noise, so there are no
third-party samples and no licensing questions. Cue times match the
animation timelines in ten2-src.html.
"""
import math
import sys
import wave

import numpy as np

SR = 48000
rng = np.random.default_rng(7)


def t_axis(dur):
    return np.arange(int(SR * dur)) / SR


def env(n, a=0.005, d=0.2, curve=4.0):
    """Attack then exponential-ish decay over n samples."""
    x = np.arange(n) / SR
    att = np.clip(x / max(a, 1e-4), 0, 1)
    dec = np.exp(-curve * np.clip(x - a, 0, None) / max(d, 1e-4))
    return att * dec


def lowpass(x, cutoff):
    """One-pole lowpass; cutoff may be an array (time-varying)."""
    cutoff = np.broadcast_to(np.asarray(cutoff, dtype=float), x.shape)
    a = 1 - np.exp(-2 * math.pi * cutoff / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc += a[i] * (x[i] - acc)
        y[i] = acc
    return y


def highpass(x, cutoff):
    return x - lowpass(x, cutoff)


def sweep(f0, f1, dur, shape="exp"):
    t = t_axis(dur)
    if shape == "exp":
        f = f0 * (f1 / f0) ** (t / dur)
    else:
        f = f0 + (f1 - f0) * (t / dur)
    return np.sin(2 * math.pi * np.cumsum(f) / SR)


def noise(dur):
    return rng.standard_normal(int(SR * dur))


# ---------- sound library ----------
def whoosh(dur=0.6, lo=300, hi=3500, gain=0.5):
    n = int(SR * dur)
    x = np.linspace(0, 1, n)
    shape = np.sin(math.pi * x) ** 1.6
    cut = lo + (hi - lo) * np.sin(math.pi * x)
    s = highpass(lowpass(noise(dur), cut), 150) * shape
    return s / (np.abs(s).max() + 1e-9) * gain


def whoosh_up(dur=0.7, gain=0.45):
    n = int(SR * dur)
    x = np.linspace(0, 1, n)
    cut = 400 + 5000 * x ** 2
    s = highpass(lowpass(noise(dur), cut), 200) * (x ** 1.5) * np.clip((1 - x) * 12, 0, 1)
    return s / (np.abs(s).max() + 1e-9) * gain


def pop(f=520, gain=0.5, dur=0.12):
    s = sweep(f * 1.6, f, dur) * env(int(SR * dur), 0.002, dur * 0.6, 5)
    return s * gain


def pop_soft(f=700, gain=0.3):
    return pop(f, gain, 0.09)


def click(gain=0.35):
    n = int(SR * 0.03)
    s = highpass(noise(0.03), 2500) * env(n, 0.0005, 0.008, 6) + 0.4 * np.sin(2 * math.pi * 1800 * t_axis(0.03)) * env(n, 0.0005, 0.01, 6)
    return s / (np.abs(s).max() + 1e-9) * gain


def key(gain=0.18):
    f = rng.uniform(2200, 3600)
    n = int(SR * 0.025)
    s = highpass(noise(0.025), f) * env(n, 0.0003, 0.006, 6) + 0.3 * np.sin(2 * math.pi * rng.uniform(300, 500) * t_axis(0.025)) * env(n, 0.0005, 0.01, 6)
    return s / (np.abs(s).max() + 1e-9) * gain * rng.uniform(0.7, 1.0)


def bell(f=1320, gain=0.35, dur=1.4):
    t = t_axis(dur)
    s = sum(a * np.sin(2 * math.pi * f * m * t) * np.exp(-t * (2.5 + m)) for m, a in [(1, 1.0), (2.01, 0.45), (3.0, 0.22), (4.2, 0.1)])
    return s * np.clip(t / 0.003, 0, 1) * gain


def ding(gain=0.32):
    a = bell(1318, gain)
    b = bell(1976, gain * 0.9)
    out = np.zeros(len(a) + int(SR * 0.09))
    out[: len(a)] += a
    out[int(SR * 0.09):] += b
    return out


def chord(gain=0.3, dur=1.6):
    t = t_axis(dur)
    s = sum(np.sin(2 * math.pi * f * t) for f in (523.25, 659.25, 783.99, 1046.5)) / 4
    return s * env(len(t), 0.02, dur * 0.6, 3) * gain


def kaching(gain=0.4):
    chink = highpass(noise(0.08), 4000) * env(int(SR * 0.08), 0.001, 0.03, 5)
    out = np.zeros(int(SR * 1.5))
    out[: len(chink)] += chink / (np.abs(chink).max() + 1e-9) * 0.5
    b = bell(2093, 0.8)
    out[int(SR * 0.07): int(SR * 0.07) + len(b)] += b[: len(out) - int(SR * 0.07)]
    return out * gain


def boom(gain=0.55, dur=1.2):
    t = t_axis(dur)
    s = np.sin(2 * math.pi * np.cumsum(50 + 60 * np.exp(-t * 8)) / SR) * env(len(t), 0.004, 0.5, 3)
    s += 0.25 * lowpass(noise(dur), 600) * env(len(t), 0.002, 0.15, 4)
    return s / (np.abs(s).max() + 1e-9) * gain


def thud(gain=0.4):
    return boom(gain, 0.35)


def shimmer(dur=1.0, gain=0.18):
    out = np.zeros(int(SR * dur))
    for _ in range(26):
        f = rng.uniform(2500, 6500)
        st = int(rng.uniform(0, dur - 0.25) * SR)
        g = np.sin(2 * math.pi * f * t_axis(0.25)) * env(int(SR * 0.25), 0.004, 0.08, 4)
        out[st: st + len(g)] += g * rng.uniform(0.3, 1)
    w = np.sin(math.pi * np.linspace(0, 1, len(out)))
    return out / (np.abs(out).max() + 1e-9) * gain * w


def boing(gain=0.35, up=True):
    dur = 0.45
    t = t_axis(dur)
    f = (220 + 380 * np.sin(math.pi * t / dur * 0.5)) if up else (500 - 250 * t / dur)
    vib = 1 + 0.08 * np.sin(2 * math.pi * 18 * t)
    s = np.sin(2 * math.pi * np.cumsum(f * vib) / SR) * env(len(t), 0.005, 0.3, 3)
    return s * gain


def slide_whistle(gain=0.25):
    dur = 0.5
    s = sweep(500, 1500, dur) * np.sin(math.pi * np.linspace(0, 1, int(SR * dur)))
    return s * gain


def send(gain=0.3):
    return sweep(600, 1400, 0.12) * env(int(SR * 0.12), 0.003, 0.08, 4) * gain


def receive(gain=0.3):
    a = np.sin(2 * math.pi * 880 * t_axis(0.12)) * env(int(SR * 0.12), 0.003, 0.08, 4)
    b = np.sin(2 * math.pi * 1320 * t_axis(0.16)) * env(int(SR * 0.16), 0.003, 0.1, 4)
    out = np.zeros(len(a) + int(SR * 0.08) + len(b))
    out[: len(a)] += a
    out[int(SR * 0.08): int(SR * 0.08) + len(b)] += b
    return out * gain


def tick(gain=0.2, f=3000):
    n = int(SR * 0.012)
    return np.sin(2 * math.pi * f * t_axis(0.012)) * env(n, 0.0003, 0.004, 5) * gain


def tone_rise(i, gain=0.22):
    base = [392, 440, 494, 523, 587][i]
    dur = 0.9
    s = sweep(base * 0.94, base, dur) * env(int(SR * dur), 0.05, 0.6, 2.5)
    s += 0.3 * sweep(base * 2 * 0.94, base * 2, dur) * env(int(SR * dur), 0.05, 0.4, 3)
    return s * gain


def printer(dur, gain=0.16):
    t = t_axis(dur)
    s = lowpass(noise(dur), 1800) * (0.6 + 0.4 * np.sign(np.sin(2 * math.pi * 26 * t)))
    s += 0.3 * np.sin(2 * math.pi * 120 * t)
    fade = np.clip(t / 0.05, 0, 1) * np.clip((dur - t) / 0.08, 0, 1)
    return s / (np.abs(s).max() + 1e-9) * gain * fade


def scribble(dur=0.9, gain=0.22):
    t = t_axis(dur)
    s = highpass(lowpass(noise(dur), 5000), 1200) * (0.5 + 0.5 * np.abs(np.sin(2 * math.pi * 7 * t)))
    fade = np.clip(t / 0.03, 0, 1) * np.clip((dur - t) / 0.05, 0, 1)
    return s / (np.abs(s).max() + 1e-9) * gain * fade


def flip(gain=0.3):
    s = highpass(noise(0.12), 1500) * env(int(SR * 0.12), 0.002, 0.05, 4)
    return s / (np.abs(s).max() + 1e-9) * gain


def tear(gain=0.35):
    dur = 0.45
    t = t_axis(dur)
    crackle = (rng.random(len(t)) > 0.92).astype(float) * rng.standard_normal(len(t))
    s = highpass(lowpass(noise(dur) * 0.4 + crackle, 6000), 900) * np.clip(t / 0.02, 0, 1) * np.exp(-t * 4)
    return s / (np.abs(s).max() + 1e-9) * gain


def womp(gain=0.3):
    a = np.sin(2 * math.pi * 392 * t_axis(0.25)) * env(int(SR * 0.25), 0.01, 0.2, 3)
    b = sweep(370, 260, 0.6) * env(int(SR * 0.6), 0.01, 0.5, 2.5)
    out = np.zeros(int(SR * 0.9))
    out[: len(a)] += a
    out[int(SR * 0.28): int(SR * 0.28) + len(b)] += b
    return out * gain


def vine_boom(gain=0.7):
    dur = 1.3
    t = t_axis(dur)
    f = 95 * np.exp(-t * 1.2) + 38
    s = np.sin(2 * math.pi * np.cumsum(f) / SR)
    s = np.tanh(3.2 * s) * env(len(t), 0.003, 0.9, 2.2)
    s += 0.5 * lowpass(noise(dur), 900) * env(len(t), 0.001, 0.06, 5)
    return s / (np.abs(s).max() + 1e-9) * gain


def record_scratch(gain=0.45):
    dur = 0.42
    t = t_axis(dur)
    f = 260 + 900 * np.sin(math.pi * t / dur * 1.6) ** 2
    saw = 2 * ((np.cumsum(f) / SR) % 1) - 1
    s = lowpass(saw + 0.6 * noise(dur), 3500) * np.clip(t / 0.01, 0, 1) * np.clip((dur - t) / 0.05, 0, 1)
    return s / (np.abs(s).max() + 1e-9) * gain


def drumroll(dur=0.8, gain=0.4):
    out = np.zeros(int(SR * dur))
    tt = 0.0
    while tt < dur:
        rate = 9 + 26 * (tt / dur)
        hit = highpass(noise(0.05), 1200) * env(int(SR * 0.05), 0.001, 0.02, 5)
        i = int(tt * SR)
        seg = hit[: len(out) - i] * (0.35 + 0.65 * tt / dur)
        out[i: i + len(seg)] += seg
        tt += 1 / rate
    return out / (np.abs(out).max() + 1e-9) * gain


def kick(gain=0.5):
    t = t_axis(0.35)
    s = np.sin(2 * math.pi * np.cumsum(50 + 110 * np.exp(-t * 30)) / SR) * env(len(t), 0.002, 0.25, 3)
    return s * gain


def hat(gain=0.12):
    s = highpass(noise(0.05), 7000) * env(int(SR * 0.05), 0.001, 0.015, 5)
    return s / (np.abs(s).max() + 1e-9) * gain


def clap(gain=0.22):
    s = np.zeros(int(SR * 0.2))
    for k, d in enumerate((0, 0.012, 0.024)):
        b = highpass(lowpass(noise(0.12), 4000), 900) * env(int(SR * 0.12), 0.001, 0.05 if k == 2 else 0.01, 5)
        i = int(d * SR); s[i: i + len(b)] += b[: len(s) - i]
    return s / (np.abs(s).max() + 1e-9) * gain


def bass_note(f, dur, gain=0.18):
    t = t_axis(dur)
    s = np.sin(2 * math.pi * f * t) + 0.3 * np.sin(2 * math.pi * 2 * f * t)
    return s * env(len(t), 0.005, dur * 0.8, 2) * gain


def beat(c, t0, t1, bpm=118):
    """Light four-on-the-floor bed with a simple bass line."""
    step = 60 / bpm
    notes = [55, 55, 65.4, 49]
    k = 0
    tt = t0
    while tt < t1 - 0.05:
        c.append((tt, kick(0.42)))
        c.append((tt + step / 2, hat(0.1)))
        if k % 2 == 1: c.append((tt, clap(0.16)))
        if k % 2 == 0: c.append((tt, bass_note(notes[(k // 4) % 4], step * 1.8, 0.16)))
        tt += step; k += 1


def sine_times(t0, dur, count):
    """Moments an eased (sine) progress crosses k/count, k = 1..count."""
    return [t0 + dur * math.acos(1 - 2 * (k / count)) / math.pi for k in range(1, count + 1)]


# ---------- cue sheets ----------
def cues(vid):
    c = []
    add = lambda t, s: c.append((t, s))
    if vid == 1:
        add(0.22, boing(0.25)); [add(t, pop(560, 0.35)) for t in (0.45, 2.6, 4.4, 6.65, 9.0)]
        add(2.62, boing(0.3)); add(3.38, thud(0.25)); add(6.65, slide_whistle(0.22)); add(7.35, bell(1760, 0.18, 0.8))
        add(9.4, shimmer(0.5, 0.14)); add(11.3, whoosh_up(0.7, 0.35)); add(12.0, ding(0.28))
    elif vid == 2:
        for i in range(3): add(0.1 + i * 0.15, whoosh(1.4, 200, 1800, 0.28))
        add(1.65, boom(0.5)); add(1.9, shimmer(1.1, 0.16))
        for i in range(7): add(1.8 + i * 0.07, tick(0.08, 2600 + i * 120))
        add(3.35, whoosh(1.2, 200, 1500, 0.25))
        for t in (4.4, 5.2, 6.6, 7.3): add(t, whoosh(0.6, 500, 2500, 0.16))
        add(6.65, boom(0.32, 0.9)); add(6.7, shimmer(0.8, 0.12)); add(9.2, whoosh(1.0, 300, 1500, 0.2)); add(9.6, bell(659, 0.22, 2.0))
    elif vid == 3:
        add(0.3, pop(480, 0.3))
        for t0, d in ((2.4, 1.2), (5.4, 1.5)):
            for t in sine_times(t0, d, int(d * 34)): add(t, tick(0.13, 2400))
        add(3.6, thud(0.3)); add(6.9, kaching(0.4))
        for i in range(4): add(9.4 + i * 0.18, pop_soft(700 + i * 90, 0.22))
        add(10.15, whoosh(0.6, 400, 2500, 0.2))
    elif vid == 4:
        add(0.5, whoosh_up(0.8, 0.35)); add(2.3, flip(0.3)); add(2.75, flip(0.2)); add(4.4, whoosh(0.7, 300, 2500, 0.25))
        for t in sine_times(4.4, 3.8, 9): add(t - 0.15, whoosh(0.35, 600, 3500, 0.14))
        add(8.4, whoosh(0.8, 300, 2000, 0.18)); add(9.3, tear(0.4)); add(9.9, ding(0.28))
    elif vid == 5:
        msgs = [(0.15, 1), (1.4, 0), (2.4, 1), (3.6, 0), (5.0, 1), (6.2, 0), (7.6, 1), (8.6, 0), (9.8, 1), (11.0, 0), (12.2, 0)]
        for t, me in msgs:
            add(t, send(0.28) if me else receive(0.26))
            if not me: add(t - 0.75, pop_soft(900, 0.08))
    elif vid == 6:
        q = "website price for a small business"
        for t in sine_times(0.6, 1.6, len(q)): add(t, key(0.16))
        add(2.3, pop_soft(650, 0.18)); add(2.6, pop_soft(700, 0.18)); add(3.4, pop(620, 0.28))
        add(5.3, click(0.4)); add(5.6, whoosh(0.9, 200, 3000, 0.4)); add(6.45, boom(0.3, 0.9))
        for i in range(5): add(7.5 + i * 0.16, pop_soft(650 + i * 80, 0.2))
        add(8.6, ding(0.28))
    elif vid == 7:
        add(0.6, printer(5.2, 0.15)); add(6.2, scribble(0.9, 0.2)); add(7.0, pop(600, 0.22))
        add(8.6, whoosh_up(0.9, 0.35)); add(9.5, ding(0.3))
    elif vid == 8:
        add(0.9, womp(0.26)); add(3.0, whoosh(1.4, 200, 1500, 0.22)); add(4.4, shimmer(0.7, 0.16))
        add(5.0, whoosh(0.8, 200, 1500, 0.16)); add(6.3, whoosh(0.8, 200, 1500, 0.16)); add(7.1, ding(0.24))
        add(8.6, whoosh(1.0, 300, 1800, 0.2)); add(9.0, pop(560, 0.25))
    elif vid == 9:
        for i in range(5): add(1.2 + i * 1.0, tone_rise(i, 0.22)); add(1.2 + i * 1.0, tick(0.1, 2800))
        add(6.35, chord(0.3)); add(7.7, kaching(0.36)); add(8.6, whoosh(0.6, 400, 2500, 0.2))
    elif vid == 10:
        total = 0
        from_code = ["<header>", "  <h1>Sunrise Bakery</h1>", "  <p>Fresh bread daily</p>", "  <a class=\"btn\">Order now</a>", "</header>", "", "<section class=\"menu\">", "  <img src=\"bread.jpg\">", "</section>", "", "<style>", "  .btn { background: #B4532A }", "</style>"]
        total = sum(len(l) + 1 for l in from_code)
        for k, t in enumerate(sine_times(0.8, 4.8, total)):
            if k % 2 == 0: add(t, key(0.13))
        add(6.0, whoosh(1.1, 200, 2500, 0.32)); add(7.0, pop_soft(700, 0.2)); add(8.4, ding(0.26)); add(8.9, pop(560, 0.22))
    elif vid == 11:
        add(0.0, whoosh(0.4, 600, 3000, 0.2)); add(0.8, pop(620, 0.3)); add(1.6, vine_boom(0.75))
        add(2.25, record_scratch(0.45)); add(2.4, pop_soft(500, 0.2)); add(2.65, pop_soft(650, 0.2))
        add(3.4, whoosh(0.6, 300, 3000, 0.3))
        for k, t in enumerate(sine_times(3.75, 2.2, 160)):
            if k % 2 == 0: add(t, key(0.12))
        add(6.0, whoosh(0.8, 200, 2500, 0.3))
        for i in range(4): add(7.0 + i * 0.4, pop(560 + i * 120, 0.28))
        add(9.4, whoosh_up(0.6, 0.3)); add(9.5, pop(500, 0.25)); add(10.55, scribble(0.3, 0.2)); add(10.85, pop_soft(700, 0.18))
        add(10.95, drumroll(0.8, 0.42)); add(11.75, kaching(0.45)); add(11.75, boom(0.35, 0.9)); add(11.8, shimmer(0.9, 0.16))
        add(12.6, whoosh(0.6, 400, 3000, 0.25))
        for i in range(10): add(13.1 + i * 0.08, pop_soft(500 + i * 60, 0.16))
        add(14.2, pop(520, 0.3)); add(15.6, whoosh(0.6, 300, 2000, 0.22)); add(16.0, chord(0.26, 1.5))
        beat(c, 3.45, 10.9); beat(c, 11.75, 15.6)
    return c


def render(vid, dur, path):
    out = np.zeros(int(SR * (dur + 2)))
    for t, s in cues(vid):
        i = int(t * SR)
        if i < 0 or i >= len(out):
            continue
        seg = s[: len(out) - i]
        out[i: i + len(seg)] += seg
    out = out[: int(SR * dur)]
    # gentle limiter and a short tail fade so loops do not click
    out = np.tanh(out * 1.2) / np.tanh(1.2)
    out *= np.clip((dur - np.arange(len(out)) / SR) / 0.05, 0, 1)
    pcm = (np.clip(out, -1, 1) * 32767 * 0.9).astype(np.int16)
    stereo = np.repeat(pcm[:, None], 2, axis=1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(stereo.tobytes())


if __name__ == "__main__":
    DUR = {11: 17.5, 1: 14, 2: 12, 3: 12, 4: 13, 5: 15, 6: 13, 7: 13, 8: 13, 9: 12.5, 10: 13}
    ids = [int(a) for a in sys.argv[1:]] or list(DUR)
    for v in ids:
        render(v, DUR[v], f"sfx-{v:02d}.wav")
        print("wav", v)
