"""2D series v3 (21-25): meme hook built from speed-ramped pieces, object carries into the 2D ad."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compose import *  # noqa
import compose_all as CA
from v2d2 import meme_band, dur

B = os.path.join(HERE, "build")
N = lambda d, n: os.path.join(ROOT, "clips", d, n)
# pieces: (start, end, speed) or "R" = fast tape rewind of the previous piece
MEMES = {21: (N("n3", "AP42ohtASY8.mp4"), [(0, 1.8, 1.0), "R", (0.0, 0.6, 0.45)], 1150),
         22: (N("n3", "CJHh0mRjSWA.mp4"), [(0, 1.0, 0.5), (0, 0.69, 0.5)], None),
         23: (N("n3", "12I4QwK-Loo.mp4"), [(0, 2.2, 1.0), (2.2, 2.61, 0.4)], 1150),
         24: (N("n3", "2xoWsKp_lKg.mp4"), [(0, 1.45, 1.0), (1.45, 2.1, 0.3)], 1920),
         25: (N("n3", "1vQ8eIFsUH4.mp4"), [(0, 1.89, 1.0), "R", (0.35, 0.85, 0.45)], 1080)}


def prep(k):
    src, pieces, tall = MEMES[k]
    parts, prev = [], None
    for i, p in enumerate(pieces):
        o = os.path.join(B, f"m{k}_{i}.mp4")
        if p == "R":
            run(["ffmpeg", "-y", "-loglevel", "error", "-i", prev, "-vf", "reverse,setpts=PTS/4,fps=24,eq=saturation=0.6:contrast=1.15,noise=alls=18:allf=t,format=yuv420p", "-an", "-c:v", "libx264", "-crf", "16", o])
        else:
            meme_band(src, p[0], p[1], o, p[2], None, tall)
        parts.append(o); prev = o
    lst = os.path.join(B, f"m{k}.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    m = os.path.join(B, f"m{k}.mp4")
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c:v", "libx264", "-crf", "16", "-r", str(FPS), "-pix_fmt", "yuv420p", m])
    run(["ffmpeg", "-y", "-loglevel", "error", "-sseof", "-0.06", "-i", m, "-frames:v", "1", "-update", "1", os.path.join(B, f"m{k}_last.png")])


def cues(k, M, T):
    c = []
    a = lambda dt, s: c.append((M + dt, s))
    amb = lowpass(noise(M), 700)
    c.append((0, amb / abs(amb).max() * 0.05))
    c.append((max(0, M - 0.6), riser(0.6, 0.3)))
    end = lambda t0: [whoosh_up(0.5, 0.25), pop(560, 0.3), ding(0.24)]
    if k == 21:
        c.append((M - 0.3, whoosh(0.35, 300, 5000, 0.45))); a(0.35, crack(0.5)); a(0.35, sub_drop(0.6, 1.2))
        st = highpass(noise(1.2), 1500) * 0.18; a(0.35, st)
        a(1.55, whoosh(0.7, 3000, 400, 0.3)); a(1.85, CA.glass(0.25)); a(2.1, shimmer(0.8, 0.14))
        for i in range(3): a(2.4 + i * 0.25, pop(560 + i * 80, 0.24))
        a(4.5, whoosh_up(0.5, 0.25)); a(4.9, pop(560, 0.3)); a(5.1, ding(0.24))
        c += pulse_bed(M + 1.55, T - 0.3, bpm=104); c.append((M + 1.55, pad(T - M - 1.55, notes=(98, 146.8, 196, 246.9), gain=0.07)))
    elif k == 22:
        c.append((M - 0.3, whoosh(0.4, 300, 5000, 0.4))); a(0.35, boom(0.4, 0.8))
        r = np.random.default_rng(6)
        for _ in range(26): a(0.5 + r.random() * 1.2, CA.slide(0.12, 0.08))
        a(1.9, whoosh(0.8, 300, 3000, 0.4)); a(2.1, shimmer(1.0, 0.16)); a(2.6, kaching(0.4))
        for i in range(4): a(3.2 + i * 0.15, pop_soft(700 + i * 90, 0.12))
        a(4.45, whoosh_up(0.5, 0.25)); a(4.8, pop(560, 0.3)); a(5.0, ding(0.24))
        c += pulse_bed(M + 0.35, T - 0.3, bpm=100); c.append((M + 2.1, pad(T - M - 2.1, notes=(98, 123.5, 146.8, 196), gain=0.07)))
    elif k == 23:
        c.append((M - 0.25, whoosh(0.3, 400, 4000, 0.4))); a(0.3, boom(0.5, 1.1)); a(0.3, CA.glass(0.4))
        r = np.random.default_rng(9)
        for i in range(40): a(1.75 + i * 0.035 + r.random() * 0.02, CA.domino(0.12))
        a(3.25, shimmer(0.9, 0.15)); a(3.3, CA.note(1046.5, 0.6, 0.14)); a(3.6, pop(560, 0.26))
        a(4.45, whoosh_up(0.5, 0.25)); a(4.9, pop(560, 0.3)); a(5.1, ding(0.24))
        c += pulse_bed(M + 1.75, T - 0.3, bpm=112); c.append((M + 0.4, pad(T - M - 0.4, notes=(73.4, 110, 146.8, 185), gain=0.08)))
    elif k == 24:
        a(0.0, thud(0.6)); a(0.0, crack(0.6)); a(0.02, CA.glass(0.5)); a(0.0, sub_drop(0.6, 1.3))
        a(1.65, CA.glass(0.6)); a(1.7, whoosh(0.8, 2000, 200, 0.3))
        r = np.random.default_rng(4)
        for _ in range(10): a(2.0 + r.random() * 0.8, thud(r.uniform(0.05, 0.15)))
        a(2.6, shimmer(0.9, 0.15)); a(2.75, CA.note(1046.5, 0.5, 0.13))
        for i in range(3): a(3.1 + i * 0.25, pop(560 + i * 80, 0.24))
        a(4.45, whoosh_up(0.5, 0.25)); a(4.9, pop(560, 0.3)); a(5.1, ding(0.24))
        c += pulse_bed(M + 2.6, T - 0.3, bpm=100); c.append((M + 2.6, pad(T - M - 2.6, notes=(98, 146.8, 196, 246.9), gain=0.07)))
    elif k == 25:
        a(0.0, whoosh(0.85, 3000, 300, 0.35)); a(0.85, thud(0.4)); a(0.95, thud(0.1))
        a(1.1, pop_soft(700, 0.12)); a(1.55, pop_soft(650, 0.1)); a(1.4, CA.note(220, 0.5, 0.12)); a(1.42, CA.note(207.7, 0.6, 0.1))
        a(1.85, pop(820, 0.25)); a(2.35, whoosh(0.35, 600, 4000, 0.15))
        for dt in (2.75, 3.25, 4.6): a(dt, pop_soft(800, 0.14))
        a(3.95, key(0.2)); a(4.0, CA.whoosh(0.2, 2000, 5000, 0.12) if hasattr(CA, "whoosh") else whoosh(0.2, 2000, 5000, 0.12))
        a(5.6, whoosh_up(0.5, 0.25)); a(6.0, pop(560, 0.3)); a(6.2, ding(0.24))
        c += pulse_bed(M + 2.75, T - 0.3, bpm=98); c.append((M + 2.4, pad(T - M - 2.4, notes=(87.3, 130.8, 174.6, 220), gain=0.07)))
    return c


def build(k):
    m, s = os.path.join(B, f"m{k}.mp4"), os.path.join(B, "mg", f"seg{k}.mp4")
    M, A = dur(m), dur(s)
    T = M + A
    wav = os.path.join(B, f"v{k}.wav")
    mixdown(cues(k, M, T), T, wav)
    out = os.path.join(B, f"beribus-2d-{k}.mp4")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", m, "-i", s, "-i", wav, "-filter_complex",
         f"[0:v]setsar=1,fps={FPS},format=yuv420p[a0];[1:v]setsar=1,fps={FPS},format=yuv420p[b0];[a0][b0]concat=n=2:v=1:a=0[v];[2:a]loudnorm=I=-14:TP=-1.2:LRA=9[a]",
         "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "22", "-preset", "slow", "-maxrate", "12M", "-bufsize", "24M", "-pix_fmt", "yuv420p", "-r", str(FPS),
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", out])
    print("done", k, round(M, 2), round(T, 2))


if __name__ == "__main__":
    mode, ids = sys.argv[1], [int(a) for a in sys.argv[2:]]
    for k in ids:
        prep(k) if mode == "prep" else build(k)
