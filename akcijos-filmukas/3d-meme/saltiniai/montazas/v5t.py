"""Trailer parodies 61-65 at 25 fps."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compose import run
import v2d4
fx = v2d4.fx; B = "build"
ex = lambda i: os.path.exists(os.path.join(v2d4.LIB, "fx", f"{i}.mp3")) and os.path.getsize(os.path.join(v2d4.LIB, "fx", f"{i}.mp3")) > 2000
v2d4.MUSIC.update({62: (410, 15.356), 63: (253, 0.0), 65: (27, 0.0)})


def music_from(k, M, T, gain):
    tid, drop = v2d4.MUSIC[k]
    a = v2d4.load(os.path.join(v2d4.LIB, "mus", f"{tid}.mp3"))
    off = max(0.0, drop - M)
    seg = a[int(off * v2d4.SR): int((off + T) * v2d4.SR)].copy()
    t = np.arange(len(seg)) / v2d4.SR
    seg *= np.clip(t / 0.8, 0, 1) * np.clip((T - t) / 0.8, 0, 1)
    return seg * gain


def cues(k, M, T):
    c = []
    a = lambda dt, s: c.append((M + dt, s))
    if k == 61:  # horror: drones, heartbeat, stingers, no music
        a(0.0, fx(773, 0.9)); a(0.3, fx(2905, 0.6, 3.2))
        for i in range(6): a(0.6 + i * 0.5, fx(490 if ex(490) else 2299, 0.5))
        a(3.6, fx(773, 1.0)); a(3.6, fx(1110, 0.6)); a(3.62, fx(2951, 0.7, 0.5))
        a(5.05, fx(2914 if ex(2914) else 2917 if ex(2917) else 788, 0.8, 1.8)); a(7.15, fx(2905, 0.6, 2.5)); a(7.15, fx(773, 0.7))
        a(9.7, fx(2364, 0.5))
    elif k == 62:  # action: trap drop on the cut
        c.append((0, v2d4.music(62, M, T, gain=0.6)))
        a(0.0, fx(1704, 0.8)); a(1.5, fx(788, 0.8, 1.4)); a(2.85, fx(2903, 0.6, 1.0)); a(4.25, fx(759, 0.9)); a(4.25, fx(1143, 0.7))
        a(5.85, fx(2918, 0.9, 1.5)); a(7.05, fx(2908 if ex(2908) else 788, 0.9, 2.0)); a(9.7, fx(2364, 0.5))
    elif k == 63:  # romance: soft music from the start
        c.append((0, music_from(63, M, T, 0.7)))
        a(0.0, fx(1317, 0.4)); a(4.2, fx(869, 0.6)); a(7.0, fx(2633 if ex(2633) else 2352, 0.5, 1.5)); a(9.7, fx(2357, 0.4))
    elif k == 64:  # fantasy: orchestral hits, no beat
        a(0.0, fx(2150, 0.7)); a(0.4, fx(2290 if ex(2290) else 2918, 0.9, 3.5)); a(2.8, fx(2903, 0.6, 1.2))
        a(4.0, fx(2918, 1.0, 1.8)); a(4.0, fx(2352, 0.5, 2.0)); a(5.0, fx(2293 if ex(2293) else 2059, 0.6)); a(7.05, fx(2908 if ex(2908) else 788, 0.9, 2.0)); a(9.7, fx(2364, 0.5))
    elif k == 65:  # documentary: calm music, birds-ish ambience
        c.append((0, music_from(65, M, T, 0.6)))
        a(7.2, fx(869, 0.5)); a(7.25, fx(2352, 0.35, 1.2)); a(10.1, fx(2357, 0.4))
    return c


def build(k):
    M, A = v2d4.dur(f"{B}/m{k}.mp4"), v2d4.dur(f"{B}/mg/seg{k}.mp4"); T = M + A
    v2d4.mix(cues(k, M, T), T, f"{B}/v{k}.wav")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{B}/m{k}.mp4", "-i", f"{B}/mg/seg{k}.mp4", "-i", f"{B}/v{k}.wav", "-filter_complex",
         "[0:v]setsar=1,fps=25,format=yuv420p[a0];[1:v]setsar=1,fps=25,format=yuv420p[b0];[a0][b0]concat=n=2:v=1:a=0[v];[2:a]loudnorm=I=-14:TP=-1.2:LRA=9[a]",
         "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "20", "-preset", "slow", "-maxrate", "14M", "-bufsize", "28M", "-pix_fmt", "yuv420p", "-r", "25",
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", f"{B}/beribus-trailer-{k}.mp4"])
    print("done", k, round(M, 2), round(T, 2))


if __name__ == "__main__":
    for k in [int(x) for x in sys.argv[1:]]:
        build(k)
