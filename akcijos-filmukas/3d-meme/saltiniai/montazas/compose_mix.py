"""Final edit for videos 02-10: meme + 3D + 2D segments, transitions, full sound design."""
import os, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compose import *  # noqa
import compose_all as CA

B = os.path.join(HERE, "build")
MG = os.path.join(B, "mg")
R3 = os.path.join(ROOT, "b3d", "out")
FULL = {2: 192, 3: 192, 4: 180, 5: 186, 6: 186, 7: 186, 8: 186, 9: 186, 10: 186}
# segments: ("meme",) | ("3d", first, last) | ("2d",) ; transition before each segment after the first
PLAN = {
    2: [("meme",), ("3d", 1, 104), ("2d",)],
    3: [("meme",), ("3d", 1, 96), ("2d",)],
    4: [("meme",), ("3d", 1, 6), ("2d",)],
    5: [("meme",), ("3d", 1, 186)],
    6: [("meme",), ("3d", 1, 116), ("2d",)],
    7: [("meme",), ("2d",)],
    8: [("meme",), ("3d", 1, 124), ("2d",)],
    9: [("meme",), ("2d",), ("3d", 60, 186)],
    10: [("meme",), ("3d", 1, 186)],
}
XF = {9: [("zoomin", 0.3), ("circleopen", 0.35)]}  # other joins are hard cuts (the frames match)


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)


def seg3d(k, a, b, out):
    tmp = os.path.join(B, f"sel{k}")
    os.makedirs(tmp, exist_ok=True)
    for f in os.listdir(tmp):
        os.remove(os.path.join(tmp, f))
    for i, fr in enumerate(range(a, b + 1), 1):
        os.symlink(os.path.join(R3, f"ad{k}", f"f_{fr:04d}.png"), os.path.join(tmp, f"f_{i:04d}.png"))
    ad_clip(tmp, out)


def cues2d(k, t0):
    c = []
    a = lambda dt, s: c.append((t0 + dt, s))
    if k == 2:
        for i in range(3): a(0.05 + i * 0.07, whoosh(0.5, 400, 4500, 0.22))
        a(0.65, whoosh(0.35, 600, 4000, 0.16)); a(0.85, whoosh(0.35, 600, 4000, 0.16)); a(1.4, boom(0.4, 0.8)); a(1.4, whoosh(0.4, 3000, 600, 0.2))
        a(3.2, whoosh_up(0.6, 0.3)); a(3.45, pop(520, 0.3)); a(3.65, ding(0.24))
    elif k == 3:
        a(0.0, whoosh(0.7, 200, 4000, 0.32)); a(0.45, shimmer(0.7, 0.14))
        for i, dt in enumerate((1.1, 1.5, 1.9)): a(dt, pop(560 + i * 90, 0.25))
        a(3.4, whoosh(0.6, 2500, 400, 0.2)); a(3.9, whoosh(0.35, 600, 4000, 0.16)); a(4.3, pop(520, 0.3)); a(4.6, ding(0.24))
    elif k == 4:
        a(0.05, whoosh(0.6, 3000, 300, 0.3)); a(0.55, thud(0.25))
        for i, dt in enumerate((0.85, 1.1, 1.35)): a(dt, pop(420 + i * 60, 0.24))
        a(1.72, whoosh(0.35, 600, 4000, 0.15))
        a(2.05, crack(0.6)); a(2.05, thud(0.45)); a(2.06, whoosh(0.45, 5000, 300, 0.4)); a(2.08, sub_drop(0.5, 1.0))
        a(2.25, whoosh(0.6, 300, 3000, 0.25)); a(2.6, shimmer(0.7, 0.12))
        for i, dt in enumerate((2.55, 2.8, 3.05)): a(dt, CA.note(PENTA_[i * 2], 0.4, 0.15)); a(dt, pop_soft(800 + i * 100, 0.08))
        a(3.85, whoosh_up(0.5, 0.25)); a(4.3, whoosh(0.4, 600, 4000, 0.16)); a(4.6, pop(520, 0.3)); a(4.8, ding(0.24))
        c.extend(pulse_bed(t0 + 2.05, t0 + 6.3, bpm=110))
    elif k == 6:
        for i in range(7): a(0.15 + i * 0.05, pop(600 + i * 60, 0.16))
        a(0.9, whoosh(0.5, 400, 3500, 0.2)); a(1.6, CA.note(880, 0.25, 0.15)); a(1.62, whoosh(0.25, 800, 4000, 0.18))
        a(2.25, pop_soft(900, 0.08)); a(2.9, CA.note(1046.5, 0.3, 0.14)); a(3.0, CA.note(1318.5, 0.35, 0.12)); a(3.9, whoosh(0.35, 600, 4000, 0.16))
    elif k == 7:
        r = np.random.default_rng(4)
        for _ in range(60): a(0.2 + r.random() * 2.6, CA.coin(r, 0.1))
        a(2.4, whoosh(0.6, 2500, 400, 0.25)); a(2.65, kaching(0.4)); a(3.6, whoosh(0.35, 600, 4000, 0.16)); a(3.8, whoosh(0.35, 600, 4000, 0.16)); a(4.7, pop(520, 0.3)); a(5.0, ding(0.24))
    elif k == 8:
        a(0.05, whoosh(0.7, 300, 3000, 0.28)); a(0.45, whoosh(0.4, 600, 4000, 0.15))
        for i in range(5): a(1.05 + i * 0.3, CA.note(330, 0.25, 0.1)); a(1.15 + i * 0.3, CA.note(PENTA_[i], 0.4, 0.15))
        a(3.9, whoosh_up(0.6, 0.3)); a(4.15, pop(520, 0.3)); a(4.3, ding(0.24))
    elif k == 9:
        for dt in (0.05, 0.15, 0.3): a(dt, whoosh(0.35, 600, 4000, 0.16))
        a(1.6, riser(1.05, 0.32)); a(2.62, boom(0.6, 1.2))
    return c


PENTA_ = [784.0, 880.0, 1046.5, 1174.7, 1318.5]


def build(k):
    segs, kinds = [], []
    for s in PLAN[k]:
        if s[0] == "meme":
            segs.append(os.path.join(B, f"m{k:02d}.mp4"))
        elif s[0] == "3d":
            p = os.path.join(B, f"a{k:02d}_{s[1]}_{s[2]}.mp4")
            seg3d(k, s[1], s[2], p)
            segs.append(p)
        else:
            segs.append(os.path.join(MG, f"seg{k}.mp4"))
        kinds.append(s)
    ds = [dur(p) for p in segs]
    xf = XF.get(k, [])
    # timeline start of each segment
    starts, t = [], 0.0
    for i, d in enumerate(ds):
        if i > 0 and xf:
            t -= xf[i - 1][1]
        starts.append(t)
        t += d
    T = t
    # video graph
    ins = []
    for p in segs:
        ins += ["-i", p]
    fl = "".join(f"[{i}:v]setsar=1,fps={FPS},format=yuv420p,settb=AVTB[s{i}];" for i in range(len(segs)))
    cur = "s0"
    for i in range(1, len(segs)):
        nxt = f"j{i}"
        if xf:
            tr, d = xf[i - 1]
            fl += f"[{cur}][s{i}]xfade=transition={tr}:duration={d}:offset={starts[i]:.3f}[{nxt}];"
        else:
            fl += f"[{cur}][s{i}]concat=n=2:v=1:a=0[{nxt}];"
        cur = nxt
    # sound
    c = []
    M = ds[0]
    for i, s in enumerate(kinds):
        if s[0] == "3d":
            a0, b0, st = s[1], s[2], starts[i]
            f = lambda fr, st=st, a0=a0: st + (fr - a0) / FPS
            end = starts[i] + ds[i]
            for tt, snd in CA.cues(k, f, M, T):
                if tt < end + 0.2 and (tt >= st - 1.0 or i == 1):
                    c.append((tt, snd))
        elif s[0] == "2d":
            c += cues2d(k, starts[i])
    REW = {4: (1.30, 0.99), 5: (2.85, 0.60)}  # replay hooks: (rewind start, first hit)
    if k in REW:
        fe, hit = REW[k]
        c += [(hit - 0.02, thud(0.45)), (hit, crack(0.3)), (fe, whoosh(fe / 4 + 0.1, 5000, 400, 0.35)), (fe + fe / 4, sub_drop(0.4, 0.8))]
    if kinds[1][0] == "2d":  # meme straight into 2D
        c += [(M - 0.5, riser(0.5, 0.25)), (M - 0.05, sub_drop(0.6, 1.2))]
        amb = lowpass(noise(M), 700)
        c.append((0, amb / abs(amb).max() * 0.05))
        c.append((M, pad(T - M, notes=(98, 146.8, 196, 246.9), gain=0.08)))
        c += pulse_bed(M + 2.6, T - 0.3, bpm=100)
    wav = os.path.join(B, f"mix{k:02d}.wav")
    mixdown(c, T, wav)
    out = os.path.join(B, f"beribus-mix-{k:02d}.mp4")
    run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-i", wav, "-filter_complex", fl + f"[{cur}]format=yuv420p[v];[{len(segs)}:a]loudnorm=I=-14:TP=-1.2:LRA=9[a]",
         "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "22", "-preset", "slow", "-maxrate", "12M", "-bufsize", "24M", "-pix_fmt", "yuv420p", "-r", str(FPS),
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", f"{T:.3f}", "-movflags", "+faststart", out])
    print("done", k, round(T, 2), [round(x, 2) for x in starts])


if __name__ == "__main__":
    for k in [int(a) for a in sys.argv[1:]]:
        build(k)
