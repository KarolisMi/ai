"""2D series v4 (26-30): natural or slow-mo meme hooks (no rewind), real SFX library + music drop on the cut."""
import os, sys, subprocess
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compose import FPS, ROOT, HERE, run  # noqa

B = os.path.join(HERE, "build")
N = lambda d, n: os.path.join(ROOT, "clips", d, n)
# (src, [(start, end, speed, interpolate)], pre-filter, tall)
MEMES = {26: (N("n4", "-3X5qtK0rCE.mp4"), [(0, 3.22, 1.0, False)], "crop=iw:ih*0.76:0:0", 1150),
         27: (N("n4", "AJJ21yLkPh4.mp4"), [(0, 2.3, 0.75, True)], None, 1150),
         28: (N("n4", "0pA-S_9HUHw.mp4"), [(0.4, 3.7, 1.0, False)], None, 1150),
         29: (N("n3", "59H_yOtzG8M.mp4"), [(0.35, 2.12, 1.0, False), (2.12, 2.6, 0.42, True)], None, 1150),
         30: (N("n5", "G7ryB6dOXCs.mp4"), [(0, 2.24, 0.72, True)], None, 1150)}


def band(src, start, end, out, speed, interp, pre, tall):
    mi = f"minterpolate=fps={int(round(24 / speed))}:mi_mode=mci:mc_mode=aobmc:vsbmc=1," if interp else ""
    base = mi + f"trim=start={start}:end={end},setpts=(PTS-STARTPTS)/{speed},fps={FPS}," + (pre + "," if pre else "")
    fg = f"scale=-2:{tall}:flags=lanczos,crop='min(iw,1080)':{tall},unsharp=5:5:0.5"
    chain = (f"[0:v]{base}split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:2,eq=brightness=-0.2[bg];"
             f"[b]{fg}[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,noise=alls=5:allf=t,format=yuv420p[v]")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-filter_complex", chain, "-map", "[v]", "-c:v", "libx264", "-crf", "16", "-r", str(FPS), out])


def prep(k):
    src, pieces, pre, tall = MEMES[k]
    parts = []
    for i, (a, b, sp, it) in enumerate(pieces):
        o = os.path.join(B, f"m{k}_{i}.mp4"); band(src, a, b, o, sp, it, pre, tall); parts.append(o)
    m = os.path.join(B, f"m{k}.mp4")
    lst = os.path.join(B, f"m{k}.txt"); open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c:v", "libx264", "-crf", "16", "-r", str(FPS), "-pix_fmt", "yuv420p", m])
    run(["ffmpeg", "-y", "-loglevel", "error", "-sseof", "-0.06", "-i", m, "-frames:v", "1", "-update", "1", os.path.join(B, f"m{k}_last.png")])


# ---------------- sound: real SFX library + music with the drop on the cut ----------------
import wave
SR = 48000
LIB = os.path.join(ROOT, "sfxlib")
_cache = {}


def load(path):
    if path not in _cache:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
        _cache[path] = np.frombuffer(raw, np.float32).astype(np.float64)
    return _cache[path]


def fx(i, gain=1.0, dur=None, fade=0.08):
    a = load(os.path.join(LIB, "fx", f"{i}.mp3")).copy()
    a = a[np.argmax(np.abs(a) > 0.01):]  # trim leading silence
    if dur:
        a = a[: int(dur * SR)]
        n = int(fade * SR); a[-n:] *= np.linspace(1, 0, n)
    return a * gain


MUSIC = {26: (369, 13.712), 27: (726, 14.388), 28: (403, 14.765), 29: (305, 12.638), 30: (410, 15.356)}


def music(k, M, T, gain=0.55):
    tid, drop = MUSIC[k]
    a = load(os.path.join(LIB, "mus", f"{tid}.mp3"))
    off = drop - M  # the drop lands exactly on the cut
    seg = a[int(off * SR): int((off + T) * SR)].copy()
    t = np.arange(len(seg)) / SR
    pre = t < M
    seg[pre] *= 0.35 * np.clip(t[pre] / 0.4, 0, 1)  # quiet build under the meme
    seg[~pre] *= 1.0
    seg *= np.clip((T - t) / 0.6, 0, 1)
    return seg * gain


def cues(k, M, T):
    c = [(0, music(k, M, T))]
    a = lambda dt, s: c.append((M + dt, s))
    c.append((M - 0.8, fx(790, 0.5, 0.8)))  # riser into the cut
    end = [(5.45, fx(1464, 0.5)), (5.75, fx(2364, 0.6)), (5.95, fx(2869, 0.45))]
    if k == 26:
        a(-0.05, fx(1492, 0.9)); a(0.0, fx(2150, 0.9)); a(0.0, fx(2296, 0.6, 1.2))
        for i in range(3): a(0.35 + 0.62 * (i + 1) - 0.12, fx(1462, 0.8)); a(0.35 + 0.62 * (i + 1) - 0.28, fx(2155, 0.35, 0.3))
        a(0.35 + 0.62 * 3 + 0.5, fx(2364, 0.6)); a(0.35 + 0.62 * 3 + 0.75, fx(1490, 0.8))
        a(0.35 + 0.62 * 3 + 0.95, fx(2865, 0.7)); a(0.35 + 0.62 * 3 + 1.0, fx(2352, 0.5, 1.5))
    elif k == 27:
        a(0.0, fx(1490, 0.9)); a(0.05, fx(2296, 0.5, 1.0))
        for i in range(6): a(0.4 + i * 0.25, fx(2072, 0.2, 0.3))
        a(2.5, fx(2364, 0.6)); a(2.6, fx(2352, 0.4, 1.2)); a(2.85, fx(1464, 0.7)); a(3.4, fx(2357, 0.6)); a(3.0, fx(2069, 0.5))
    elif k == 28:
        a(-0.02, fx(1492, 0.8)); a(0.18, fx(1143, 0.9)); a(0.18, fx(759, 0.35, 1.0))
        a(0.55, fx(2364, 0.5)); a(1.75, fx(1462, 0.6)); a(2.0, fx(1464, 0.5)); a(2.55, fx(2155, 0.6, 0.4)); a(2.55, fx(2067, 0.5))
        for i in range(3): a(3.15 + i * 0.2, fx(2357, 0.45))
    elif k == 29:
        a(-0.02, fx(1492, 0.7)); a(0.3, fx(759, 0.9)); a(0.3, fx(788, 0.7, 1.4))
        a(1.5, fx(2951, 0.5, 0.6)); a(2.1, fx(2296, 0.6, 1.0)); a(2.15, fx(2946, 0.5, 0.5)); a(2.9, fx(2352, 0.5, 1.2)); a(3.0, fx(2865, 0.5)); a(3.5, fx(2364, 0.5))
    elif k == 30:
        a(0.0, fx(1692, 0.9)); a(0.0, fx(1143, 0.8)); a(0.05, fx(1691, 0.5))
        r = np.random.default_rng(3)
        for i in range(18): a(0.5 + r.random() * 1.1, fx(2185, 0.25, 0.25))
        for i in range(10): a(2.15 + i * 0.07 + 0.2, fx(2089, 0.15, 0.3))
        for i in range(3): a(3.0 + i * 0.25, fx(2072, 0.5, 0.3))
        a(4.0, fx(1462, 0.6)); a(4.25, fx(2059, 0.5)); a(4.3, fx(2364, 0.5))
    c += [(M + dt, s) for dt, s in end]
    return c


def mix(cues, T, path):
    out = np.zeros(int(SR * (T + 4)))
    for t, s in cues:
        i = int(max(0, t) * SR); seg = s[: len(out) - i]; out[i: i + len(seg)] += seg
    out = out[: int(SR * T)]
    out = np.tanh(out * 1.1) / np.tanh(1.1)
    pcm = (np.clip(out, -1, 1) * 32767 * 0.9).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(np.repeat(pcm, 2).tobytes())


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)


def build(k):
    m, s = os.path.join(B, f"m{k}.mp4"), os.path.join(B, "mg", f"seg{k}.mp4")
    M, A = dur(m), dur(s)
    T = M + A
    wav = os.path.join(B, f"v{k}.wav")
    mix(cues(k, M, T), T, wav)
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
