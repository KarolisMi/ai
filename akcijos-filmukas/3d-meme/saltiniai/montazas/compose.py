"""Meme hook + 3D Beribus ad: match-cut transition, grade, sound design, final MP4."""
import json, math, os, subprocess, sys, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
from sfx import (SR, noise, lowpass, highpass, env, t_axis, sweep, whoosh, whoosh_up, boom, thud, shimmer,
                 kaching, key, kick, hat, clap, bass_note, pop, pop_soft, ding, chord, bell, tick)

FPS = 24


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-2500:])
        raise SystemExit(1)


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", path], capture_output=True, text=True).stdout.strip()
    return [int(x) for x in out.split(",")[:2]]


# ---------- sound ----------
def crack(gain=0.6):
    """Bat-on-ball crack: sharp transient plus a woody body."""
    t = t_axis(0.25)
    s = highpass(noise(0.25), 1500) * env(len(t), 0.0005, 0.02, 6)
    s += 0.6 * np.sin(2 * math.pi * 900 * t) * env(len(t), 0.001, 0.05, 5)
    return s / (np.abs(s).max() + 1e-9) * gain


def clatter(n, t0, dur, seed=3):
    r = np.random.default_rng(seed)
    out = []
    for i in range(n):
        tt = t0 + dur * (r.random() ** 1.6)
        f = r.uniform(180, 420)
        x = t_axis(0.18)
        s = (np.sin(2 * math.pi * f * x) * 0.6 + lowpass(noise(0.18), 2500) * 0.5) * env(len(x), 0.001, 0.06, 5)
        out.append((tt, s * r.uniform(0.12, 0.3)))
    return out


def sub_drop(gain=0.6, dur=1.4):
    t = t_axis(dur)
    s = np.sin(2 * math.pi * np.cumsum(70 * np.exp(-t * 1.5) + 32) / SR) * env(len(t), 0.005, dur * 0.7, 2.2)
    return np.tanh(2 * s) * gain


def riser(dur=1.0, gain=0.3):
    t = t_axis(dur)
    s = highpass(lowpass(noise(dur), 1000 + 6000 * (t / dur) ** 2), 300) * (t / dur) ** 2
    s += 0.4 * sweep(200, 900, dur) * (t / dur) ** 2
    return s / (np.abs(s).max() + 1e-9) * gain


def pad(dur, notes=(110, 164.8, 220, 277.2), gain=0.1):
    t = t_axis(dur)
    s = sum(np.sin(2 * math.pi * f * t + 0.3 * np.sin(2 * math.pi * 0.2 * t)) for f in notes) / len(notes)
    s = lowpass(s, 1800)
    return s * np.clip(t / 1.2, 0, 1) * np.clip((dur - t) / 1.0, 0, 1) * gain


def pulse_bed(t0, t1, bpm=100, gain=1.0):
    c, step, t, k = [], 60 / bpm, t0, 0
    while t < t1 - 0.05:
        c.append((t, kick(0.38 * gain)))
        c.append((t + step / 2, hat(0.07 * gain)))
        if k % 2 == 1:
            c.append((t, clap(0.1 * gain)))
        t += step
        k += 1
    return c


def mixdown(cues, total, path):
    out = np.zeros(int(SR * (total + 3)))
    for t, s in cues:
        i = int(max(0, t) * SR)
        seg = s[: len(out) - i]
        out[i: i + len(seg)] += seg
    out = out[: int(SR * total)]
    out = np.tanh(out * 1.15) / np.tanh(1.15)
    out *= np.clip((total - np.arange(len(out)) / SR) / 0.25, 0, 1)
    pcm = (np.clip(out, -1, 1) * 32767 * 0.9).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(np.repeat(pcm[:, None], 2, axis=1).tobytes())


# ---------- picture ----------
def meme_clip(src, start, end, out, fill="auto", zoom_end=None, loops=0, speed=1.0):
    """Meme at 1080x1920/24 fps. Portrait clips fill the frame, landscape ones sit on a blurred copy.
    zoom_end=(cx, cy, amount, dur): push into a point over the final seconds (the match cut)."""
    w, h = probe(src)
    dur = end - start
    if fill == "auto":
        fill = w / h < 0.75
    base = f"trim=start={start}:end={end},setpts=(PTS-STARTPTS)/{speed},fps={FPS},"
    dur = dur / speed
    if fill:
        chain = f"[0:v]{base}scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,unsharp=5:5:0.6[m]"
    else:
        sc = min(1080 / w, 1300 / h)
        fw, fh = int(w * sc) // 2 * 2, int(h * sc) // 2 * 2
        chain = (f"[0:v]{base}split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:2,eq=brightness=-0.2[bg];"
                 f"[b]scale={fw}:{fh}:flags=lanczos,unsharp=5:5:0.5[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2[m]")
    if zoom_end:
        cx, cy, amt, zd = zoom_end
        z = f"if(gte(in_time,{dur - zd:.3f}),1+{amt}*pow(min(1,(in_time-{dur - zd:.3f})/{zd}),2),1)"
        chain += (f";[m]zoompan=z='{z}':x='{cx}*iw-(iw/zoom/2)':y='{cy}*ih-(ih/zoom/2)':d=1:s=1080x1920:fps={FPS},"
                  f"noise=alls=5:allf=t,format=yuv420p[v]")
    else:
        chain += ";[m]noise=alls=5:allf=t,format=yuv420p[v]"
    run(["ffmpeg", "-y", "-loglevel", "error", "-stream_loop", str(loops), "-i", src, "-filter_complex", chain, "-map", "[v]", "-c:v", "libx264", "-crf", "16", "-r", str(FPS), out])
    return dur


def ad_clip(frames_dir, out, zoom_in=None):
    """3D frames upscaled and graded; zoom_in=(amount, dur) eases out of a punch-in at the start."""
    vf = "scale=1080:1920:flags=lanczos,unsharp=5:5:0.45,noise=alls=3:allf=t"
    if zoom_in:
        amt, zd = zoom_in
        vf += (f",zoompan=z='if(lt(in_time,{zd}),1+{amt}*pow(1-in_time/{zd},2),1)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps={FPS}")
    vf += ",format=yuv420p"
    run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(frames_dir, "f_%04d.png"), "-vf", vf, "-c:v", "libx264", "-crf", "16", "-r", str(FPS), out])


def join(meme, ad, wav, out, blend=2):
    """Concatenate with a short motion-blurred blend across the cut."""
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", meme, "-i", ad, "-i", wav, "-filter_complex",
         f"[0:v]setsar=1,fps={FPS},format=yuv420p[a0];[1:v]setsar=1,fps={FPS},format=yuv420p[b0];[a0][b0]concat=n=2:v=1:a=0,format=yuv420p[v];[2:a]loudnorm=I=-14:TP=-1.2:LRA=9[a]",
         "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "22", "-preset", "slow", "-maxrate", "12M", "-bufsize", "24M", "-pix_fmt", "yuv420p", "-r", str(FPS),
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", out])
