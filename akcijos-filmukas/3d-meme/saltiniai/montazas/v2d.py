"""2D series 11-15: real meme hook (3.5-4.5 s) -> 2D transition and ad -> CTA, with sound design."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compose import *  # noqa
import compose_all as CA

B = os.path.join(HERE, "build")
MG = os.path.join(B, "mg")
CAND = lambda n: os.path.join(ROOT, "clips/cand", n)
MEMES = {11: ("c_B1Key1p6fg8.mp4", 0.3, 4.6), 12: ("r_4gZnJ06D42I.mp4", 0.0, 4.0), 13: ("c_89uCYM2vYAw.mp4", 0.0, 4.3),
         14: ("c_6MIXR2S2LHQ.mp4", 0.0, 3.6), 15: ("c_39lfhDz5L0k.mp4", 0.0, 4.0)}


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)


def prep(k):
    f, a, b = MEMES[k]
    m = os.path.join(B, f"m{k}.mp4")
    meme_clip(CAND(f), a, b, m, fill=True)
    run(["ffmpeg", "-y", "-loglevel", "error", "-sseof", "-0.06", "-i", m, "-frames:v", "1", "-update", "1", os.path.join(B, f"m{k}_last.png")])


def cues(k, M, T):
    c = []
    a = lambda dt, s: c.append((M + dt, s))
    amb = lowpass(noise(M), 700)
    c.append((0, amb / abs(amb).max() * 0.05))
    c.append((max(0, M - 0.5), riser(0.5, 0.28)))
    c.append((M + 5.4, pad(T - M - 5.4, notes=(98, 146.8, 196, 246.9), gain=0.07)))
    if k == 11:
        c += [(M - 0.1, whoosh(0.45, 300, 6000, 0.4))]; a(0.3, CA.glass(0.65)); a(0.3, sub_drop(0.7, 1.4)); a(0.3, boom(0.5, 1.0))
        for i in range(10): a(0.55 + i * 0.05, pop_soft(700 + i * 40, 0.07))
        a(1.45, CA.slide(0.85, 0.35)); a(2.25, boom(0.5, 1.2)); a(2.25, crack(0.45))
        r = np.random.default_rng(3)
        for _ in range(14): a(2.27 + r.random() * 0.4, CA.domino(0.2))
        a(2.3, shimmer(0.9, 0.15)); a(3.4, whoosh(0.4, 600, 4000, 0.16)); a(4.05, pop(520, 0.26)); a(5.1, whoosh_up(0.5, 0.25)); a(5.6, pop(560, 0.3)); a(5.8, ding(0.24))
        c += pulse_bed(M + 2.25, T - 0.3, bpm=104)
    elif k == 12:
        a(0.0, whoosh(0.45, 400, 5000, 0.4))
        for i in range(5): a(0.5 + i * 0.22, CA.note(330 + i * 20, 0.2, 0.08)); a(0.5 + i * 0.22, key(0.18))
        a(1.7, pop(300, 0.25)); a(2.45, thud(0.6)); a(2.45, boom(0.4, 0.7)); a(3.2, whoosh(0.5, 4000, 400, 0.35))
        for i in range(5): a(3.65 + i * 0.22, CA.note(CA.PENTA[i * 2], 0.5, 0.15))
        a(4.75, kaching(0.4)); a(5.6, whoosh_up(0.5, 0.25)); a(5.9, pop(560, 0.3)); a(6.1, ding(0.24))
        c += pulse_bed(M + 3.2, T - 0.3, bpm=100)
    elif k == 13:
        a(0.0, whoosh(0.5, 3000, 300, 0.35)); a(0.45, thud(0.3))
        for i in range(14): a(0.8 + i * 0.054, key(0.15))
        for i in range(3): a(1.75 + i * 0.2, pop_soft(700 + i * 80, 0.1))
        a(2.5, CA.note(220, 0.6, 0.15)); a(2.55, CA.note(207.7, 0.8, 0.12)); a(3.5, riser(0.3, 0.2)); a(3.7, whoosh(0.7, 400, 3000, 0.25))
        a(3.75, shimmer(0.9, 0.16)); a(4.3, CA.note(1046.5, 0.5, 0.15)); a(4.35, pop(620, 0.25)); a(5.35, whoosh_up(0.5, 0.25)); a(5.8, pop(560, 0.3)); a(6.0, ding(0.24))
        c += pulse_bed(M + 3.7, T - 0.3, bpm=96)
    elif k == 14:
        a(0.0, CA.glass(0.25)); a(0.0, whoosh(0.5, 2000, 300, 0.35))
        for i in range(5): a(0.6 + i * 0.3, pop_soft(500 + i * 60, 0.12)); a(0.75 + i * 0.3, thud(0.08))
        a(2.2, whoosh(0.7, 2500, 200, 0.3))
        r = np.random.default_rng(7)
        for i in range(5): a(2.55 + r.random() * 0.35, thud(r.uniform(0.25, 0.45)))
        a(2.4, CA.note(196, 0.7, 0.16)); a(2.42, CA.note(185, 0.7, 0.12)); a(3.0, boom(0.4, 0.8)); a(3.0, shimmer(0.9, 0.15))
        for i in range(3): a(3.5 + i * 0.25, CA.note(CA.PENTA[2 + i * 2], 0.5, 0.15))
        a(5.35, whoosh_up(0.5, 0.25)); a(5.8, pop(560, 0.3)); a(6.0, ding(0.24))
        c += pulse_bed(M + 3.0, T - 0.3, bpm=104)
    elif k == 15:
        a(0.0, CA.slide(0.16, 0.2)); a(0.16, whoosh(0.4, 400, 5000, 0.4))
        for i in range(5):
            t0 = 0.6 + i * 0.42
            a(t0 + 0.27, thud(0.35)); a(t0 + 0.27, CA.note(CA.PENTA[i * 2], 0.4, 0.15)); a(t0 + 0.5, thud(0.12)); a(t0 + 0.65, thud(0.05))
        a(3.1, CA.note(1046.5, 0.8, 0.16)); a(3.0, pop(560, 0.25)); a(3.2, shimmer(0.8, 0.14)); a(5.35, whoosh_up(0.5, 0.25)); a(5.8, pop(560, 0.3)); a(6.0, ding(0.24))
        c += pulse_bed(M + 0.6, T - 0.3, bpm=110)
    return c


def build(k):
    m, s = os.path.join(B, f"m{k}.mp4"), os.path.join(MG, f"seg{k}.mp4")
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
