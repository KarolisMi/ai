"""2D series v2 (16-20): real meme hook, the meme's object carries straight into the 2D ad (match cut), CTA."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compose import *  # noqa

B = os.path.join(HERE, "build")
N2 = lambda n: os.path.join(ROOT, "clips/n2", n)
# k: (file, start, end, speed)
MEMES = {16: ("18DiP6FCXvw.mp4", 0.0, 0.95, 0.3), 17: ("4dzabqGw-sQ.mp4", 0.0, 1.58, 0.48), 18: ("1QhisOiyl_k.mp4", 0.0, 3.3, 1.0),
         19: ("Cu5SrSNcyEc.mp4", 0.0, 1.6, 0.5), 20: ("9_VYm7R-OT8.mp4", 0.0, 1.55, 0.47)}


# pre-crop (black bars) and how tall the meme sits on its blurred backdrop
PRE = {18: "crop=360:360:140:0"}
TALL = {19: 1150, 18: 1500}


def meme_band(src, start, end, out, speed, pre=None, tall=None):
    base = f"trim=start={start}:end={end},setpts=(PTS-STARTPTS)/{speed},fps={FPS}," + (pre + "," if pre else "")
    fg = f"scale=-2:{tall}:flags=lanczos,crop='min(iw,1080)':{tall},unsharp=5:5:0.5" if tall else "scale=1080:-2:flags=lanczos,unsharp=5:5:0.5"
    chain = (f"[0:v]{base}split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:2,eq=brightness=-0.2[bg];"
             f"[b]{fg}[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,noise=alls=5:allf=t,format=yuv420p[v]")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-filter_complex", chain, "-map", "[v]", "-c:v", "libx264", "-crf", "16", "-r", str(FPS), out])


def prep(k):
    f, a, b, sp = MEMES[k]
    m = os.path.join(B, f"m{k}.mp4")
    if k in PRE or k in TALL:
        meme_band(N2(f), a, b, m, sp, PRE.get(k), TALL.get(k))
    else:
        meme_clip(N2(f), a, b, m, speed=sp)
    run(["ffmpeg", "-y", "-loglevel", "error", "-sseof", "-0.06", "-i", m, "-frames:v", "1", "-update", "1", os.path.join(B, f"m{k}_last.png")])




import numpy as np
import compose_all as CA


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)


def cues(k, M, T):
    c = []
    a = lambda dt, s: c.append((M + dt, s))
    amb = lowpass(noise(M), 700)
    c.append((0, amb / abs(amb).max() * 0.05))
    c.append((max(0, M - 0.6), riser(0.6, 0.3)))
    if k == 16:
        c.append((M - 0.3, whoosh(0.35, 300, 6000, 0.45))); a(0.3, sub_drop(0.6, 1.3)); a(0.3, whoosh(0.5, 5000, 600, 0.3))
        a(0.78, boom(0.5, 1.2)); a(0.78, crack(0.45))
        r = np.random.default_rng(2)
        for _ in range(5): a(1.0 + r.random() * 0.6, thud(r.uniform(0.15, 0.3)))
        a(1.35, whoosh(0.6, 2500, 300, 0.3)); a(1.82, sub_drop(0.6, 1.3)); a(1.82, thud(0.5)); a(2.1, thud(0.15)); a(1.9, shimmer(0.9, 0.14))
        a(2.3, whoosh(0.35, 600, 4000, 0.15)); a(4.0, whoosh_up(0.5, 0.25)); a(4.4, pop(560, 0.3)); a(4.6, ding(0.24))
        c += pulse_bed(M + 1.82, T - 0.3, bpm=104); c.append((M + 1.82, pad(T - M - 1.82, notes=(98, 146.8, 196, 246.9), gain=0.07)))
    elif k == 17:
        a(0.0, sub_drop(0.6, 1.3))
        for i in range(3): a(0.04 + i * 0.05, whoosh(0.25, 6000, 1500, 0.35)); a(0.04 + i * 0.05, crack(0.18))
        a(0.3, whoosh(0.6, 400, 3000, 0.3)); a(0.55, boom(0.4, 0.8)); a(0.6, pop(500, 0.3)); a(1.0, whoosh(0.3, 600, 4000, 0.14))
        for i in range(10): a(1.7 + i * 0.09, pop_soft(600 + i * 60, 0.12))
        a(2.8, whoosh(0.3, 600, 4000, 0.14)); a(3.9, whoosh_up(0.5, 0.25)); a(4.3, pop(560, 0.3)); a(4.5, ding(0.24))
        c += pulse_bed(M + 0.55, T - 0.3, bpm=112); c.append((M + 0.4, pad(T - M - 0.4, notes=(110, 164.8, 220, 277.2), gain=0.07)))
    elif k == 18:
        a(0.0, whoosh(0.45, 300, 4000, 0.35)); a(0.38, sub_drop(0.5, 1.0))
        for i, dt in enumerate((0.5, 1.05, 1.45, 1.85)): a(dt, pop(480 + i * 70, 0.28)); a(dt, CA.note(CA.PENTA[i * 2], 0.4, 0.13))
        a(2.35, pop(700, 0.3)); a(2.4, shimmer(0.7, 0.13)); a(3.0, whoosh(0.5, 600, 4000, 0.2)); a(3.1, whoosh(0.7, 300, 3000, 0.25))
        a(4.6, whoosh_up(0.5, 0.25)); a(5.0, pop(560, 0.3)); a(5.2, ding(0.24))
        c += pulse_bed(M + 0.5, T - 0.3, bpm=100); c.append((M + 0.4, pad(T - M - 0.4, notes=(87.3, 130.8, 174.6, 220), gain=0.07)))
    elif k == 19:
        c.append((M - 0.15, whoosh(0.4, 400, 3000, 0.3))); a(0.0, whoosh(1.3, 1500, 300, 0.25))
        for i in range(8): a(0.1 + i * 0.15, whoosh(0.15, 2500, 1200, 0.08))
        a(1.25, thud(0.45)); a(1.25, boom(0.35, 0.7)); a(1.6, CA.note(220, 0.6, 0.14)); a(1.62, CA.note(207.7, 0.7, 0.1))
        a(2.55, shimmer(0.9, 0.16)); a(2.6, CA.note(1046.5, 0.5, 0.14))
        for i in range(3): a(3.1 + i * 0.25, pop(560 + i * 80, 0.24))
        a(4.6, whoosh_up(0.5, 0.25)); a(5.0, pop(560, 0.3)); a(5.2, ding(0.24))
        c += pulse_bed(M + 2.55, T - 0.3, bpm=100); c.append((M + 1.3, pad(T - M - 1.3, notes=(98, 146.8, 196, 246.9), gain=0.07)))
    elif k == 20:
        a(0.0, whoosh(0.85, 2500, 250, 0.3)); a(0.85, thud(0.6)); a(0.85, boom(0.45, 1.0)); a(0.95, thud(0.2)); a(1.05, thud(0.08))
        a(1.25, CA.note(523.3, 0.6, 0.12)); a(1.3, CA.note(784, 0.8, 0.12)); a(1.75, shimmer(0.7, 0.13))
        for i in range(3): a(2.4 + i * 0.25, pop(560 + i * 80, 0.24))
        a(4.5, whoosh_up(0.5, 0.25)); a(4.9, pop(560, 0.3)); a(5.1, ding(0.24))
        c += pulse_bed(M + 0.85, T - 0.3, bpm=104); c.append((M + 0.85, pad(T - M - 0.85, notes=(98, 123.5, 146.8, 196), gain=0.07)))
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
