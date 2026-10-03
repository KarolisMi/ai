"""Videos 02-10: prebuilt meme clip + rendered 3D ad + sound design -> final MP4."""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compose import *  # noqa

B = os.path.join(HERE, "build")


def glass(gain=0.55):
    dur = 1.0
    t = t_axis(dur)
    s = highpass(noise(dur), 2500) * env(len(t), 0.001, 0.3, 3)
    r = np.random.default_rng(1)
    for _ in range(26):
        f = r.uniform(2500, 9000)
        st = int(r.uniform(0, 0.5) * SR)
        g = np.sin(2 * math.pi * f * t_axis(0.12)) * env(int(SR * 0.12), 0.001, 0.05, 4)
        s[st:st + len(g)] += g[:len(s) - st] * 0.3
    return s / (np.abs(s).max() + 1e-9) * gain


def slide(dur, gain=0.25):
    t = t_axis(dur)
    s = lowpass(noise(dur), 900) * np.clip(t / 0.05, 0, 1) * np.clip((dur - t) / 0.1, 0, 1)
    return s / (np.abs(s).max() + 1e-9) * gain


def coin(r, gain=0.12):
    f = r.uniform(2800, 4200)
    x = t_axis(0.35)
    s = (np.sin(2 * math.pi * f * x) + 0.5 * np.sin(2 * math.pi * f * 1.51 * x)) * env(len(x), 0.001, 0.12, 4)
    return s * gain * r.uniform(0.5, 1)


def domino(gain=0.18):
    x = t_axis(0.08)
    s = (highpass(noise(0.08), 1500) * 0.6 + np.sin(2 * math.pi * 1200 * x)) * env(len(x), 0.0005, 0.02, 5)
    return s / (np.abs(s).max() + 1e-9) * gain


def note(fq, dur=0.6, gain=0.18):
    x = t_axis(dur)
    s = (np.sin(2 * math.pi * fq * x) + 0.3 * np.sin(2 * math.pi * 2 * fq * x)) * env(len(x), 0.004, dur * 0.6, 3)
    return s * gain


PENTA = [523.3, 587.3, 659.3, 784.0, 880.0, 1046.5, 1174.7, 1318.5, 1568.0, 1760.0]


def cues(k, f, M, T):
    c = []
    imp = k <= 5
    if imp:
        c += [(M - 0.02, glass(0.6)), (M - 0.03, sub_drop(0.7, 1.4)), (M, whoosh(0.5, 400, 6000, 0.35))]
        amb = lowpass(noise(M), 700)
        c.append((0, amb / abs(amb).max() * 0.05))
        c.append((max(0, M - 0.4), riser(0.4, 0.25)))
    else:
        c += [(max(0, M - 0.6), riser(0.6, 0.22)), (M + 0.1, whoosh(1.4, 200, 1800, 0.25))]
    if k == 2:
        c += [(f(22), whoosh(0.8, 300, 2500, 0.3)), (f(40), boom(0.7, 1.3)), (f(40), thud(0.5))]
        r = np.random.default_rng(2)
        c += [(f(42) + r.random() * 1.6, thud(r.uniform(0.15, 0.35))) for _ in range(12)]
        c += [(f(78), whoosh(0.6, 2500, 300, 0.3)), (f(92), sub_drop(0.6, 1.2)), (f(92), thud(0.5)), (f(97), thud(0.15))]
        c += [(f(108), whoosh(0.35, 600, 4000, 0.15)), (f(116), whoosh(0.35, 600, 4000, 0.15)), (f(152), pop(520, 0.3)), (f(162), ding(0.25))]
        c.append((f(92), pad(T - f(92), notes=(98, 146.8, 196, 246.9), gain=0.08)))
        c += pulse_bed(f(92), T - 0.3, bpm=104)
    elif k == 3:
        c += [(f(1), crack(0.5)), (f(11), thud(0.32)), (f(11), slide(1.0, 0.3)), (f(34), thud(0.4)), (f(34), note(1318.5, 0.9, 0.12)), (f(34), shimmer(0.8, 0.14))]
        c += [(f(36), slide(0.5, 0.15)), (f(40), whoosh(1.6, 200, 1500, 0.2))]
        c += [(f(92), whoosh(0.35, 600, 4000, 0.15)), (f(98), boom(0.3, 0.6)), (f(146), whoosh(0.35, 3000, 600, 0.14)), (f(154), pop(560, 0.3)), (f(162), ding(0.22))]
        c.append((f(34), pad(T - f(34), notes=(110, 164.8, 220, 329.6), gain=0.08)))
        c += pulse_bed(f(92), T - 0.3, bpm=96)
    elif k == 4:
        c += [(f(26), whoosh(0.4, 600, 4000, 0.15)), (f(32), boom(0.3, 0.6))]
        c += [(f(30 + i * 6), note(PENTA[i], 0.7, 0.16)) for i in range(10)]
        c += [(f(128), whoosh(0.35, 3000, 600, 0.14)), (f(134), whoosh(0.35, 600, 4000, 0.15)), (f(142), pop(520, 0.3)), (f(150), ding(0.22))]
        c.append((M, pad(T - M, notes=(87.3, 130.8, 174.6, 220), gain=0.09)))
        c += pulse_bed(f(92), T - 0.3, bpm=110)
    elif k == 5:
        c += [(f(14), whoosh(0.5, 400, 2500, 0.2))]
        PRESS = 112
        n = 14
        c += [(f(25) + (f(PRESS - 6) - f(25)) * (i / n) ** 0.9, domino(0.2)) for i in range(n)]
        c += [(f(PRESS), boom(0.4, 0.8)), (f(PRESS), note(784, 1.0, 0.18)), (f(PRESS + 2), note(1046.5, 1.0, 0.16)), (f(PRESS + 4), shimmer(1.0, 0.15))]
        c += [(f(PRESS + 6), whoosh(0.35, 600, 4000, 0.15)), (f(PRESS + 12), whoosh(0.35, 600, 4000, 0.15)), (f(156), pop(520, 0.3)), (f(164), ding(0.22))]
        c.append((f(PRESS), pad(T - f(PRESS), notes=(130.8, 196, 261.6, 329.6), gain=0.08)))
        c += pulse_bed(f(PRESS), T - 0.3, bpm=112)
    elif k == 6:
        c += [(f(70 + i * 4), pop(500 + i * 70, 0.24)) for i in range(7)]
        c += [(f(70 + i * 4) + 0.35, key(0.2)) for i in range(7)]
        c += [(f(104), whoosh(0.35, 600, 4000, 0.15)), (f(118), whoosh(0.3, 600, 4000, 0.12)), (f(128), ding(0.22))]
        c.append((M, pad(T - M, notes=(73.4, 110, 146.8, 185), gain=0.08)))
        c += pulse_bed(f(70), T - 0.3, bpm=98)
    elif k == 7:
        r = np.random.default_rng(5)
        c += [(f(46) + r.random() * 3.6, coin(r)) for _ in range(70)]
        c += [(f(92), whoosh(0.6, 2500, 400, 0.25)), (f(104), kaching(0.4))]
        c += [(f(132), whoosh(0.35, 600, 4000, 0.15)), (f(142), pop(520, 0.3)), (f(152), ding(0.22))]
        c.append((M, pad(T - M, notes=(98, 123.5, 146.8, 196), gain=0.08)))
        c += pulse_bed(f(104), T - 0.3, bpm=100)
    elif k == 8:
        c += [(f(62), whoosh(0.7, 300, 2500, 0.25)), (f(70), note(330, 0.6, 0.1)), (f(94), thud(0.4)), (f(94), domino(0.2))]
        c += [(f(96), whoosh(0.35, 600, 4000, 0.15)), (f(104), slide(0.25, 0.15)), (f(112), boom(0.3, 0.6))]
        c += [(f(146), whoosh(0.35, 3000, 600, 0.14)), (f(152), whoosh(0.35, 600, 4000, 0.14)), (f(160), pop(520, 0.3))]
        c.append((f(78), pad(T - f(78), notes=(110, 138.6, 164.8, 220), gain=0.08)))
        c += pulse_bed(f(112), T - 0.3, bpm=96)
    elif k == 9:
        c += [(f(20), whoosh(1.2, 1500, 200, 0.2))]
        c += [(f(24 + i * 4), pop(600 + i * 60, 0.2)) for i in range(4)]
        c += [(f(30), whoosh(0.35, 600, 4000, 0.14))]
        c += [(f(70 + i * 10), slide(0.25, 0.12)) for i in range(4)]
        c += [(f(78 + i * 10), note(PENTA[i * 2], 0.7, 0.17)) for i in range(4)]
        c += [(f(118), boom(0.45, 1.0)), (f(118), shimmer(0.9, 0.14)), (f(146), pop(520, 0.3)), (f(154), ding(0.22))]
        c.append((M, pad(T - M, notes=(116.5, 174.6, 233.1, 293.7), gain=0.08)))
        c += pulse_bed(f(118), T - 0.3, bpm=104)
    elif k == 10:
        c += [(f(20), riser(1.6, 0.32)), (f(58), boom(0.8, 1.6)), (f(58), sub_drop(0.6, 1.4)), (f(58), shimmer(1.6, 0.2))]
        c += [(f(64), whoosh(1.0, 300, 3000, 0.2)), (f(96), whoosh(0.35, 600, 4000, 0.15)), (f(106), whoosh(0.3, 600, 4000, 0.12)), (f(136), pop(520, 0.3))]
        c.append((f(58), chord(0.18, 3.5)))
        c.append((f(58), pad(T - f(58), notes=(65.4, 98, 130.8, 196), gain=0.1)))
        c += pulse_bed(f(80), T - 0.3, bpm=92)
    return c


FRAMES = {2: 192, 3: 192, 4: 180, 5: 186, 6: 186, 7: 186, 8: 186, 9: 186, 10: 186}
if __name__ == "__main__":
    ids = [int(a) for a in sys.argv[1:]] or list(FRAMES)
    for k in ids:
        meme = os.path.join(B, f"m{k:02d}.mp4")
        M = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", meme], capture_output=True, text=True).stdout)
        ad = os.path.join(B, f"a{k:02d}.mp4")
        ad_clip(os.path.join(ROOT, "b3d", "out", f"ad{k}"), ad)
        A = FRAMES[k] / FPS
        T = M + A
        f = lambda fr, M=M: M + (fr - 1) / FPS
        wav = os.path.join(B, f"v{k:02d}.wav")
        mixdown(cues(k, f, M, T), T, wav)
        out = os.path.join(B, f"beribus-3d-{k:02d}.mp4")
        join(meme, ad, wav, out)
        print("done", k, round(T, 2))
