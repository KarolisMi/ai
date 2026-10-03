"""Builds the ten meme-hook ads: real meme clip -> freeze + flash on impact -> Beribus ad."""
import json, math, subprocess, sys, wave
import numpy as np
sys.path.insert(0, '.')
import sfx
from sfx import SR, noise, lowpass, highpass, env, vine_boom, thud, whoosh, boing, t_axis

C = 'clips/cand/c_{}.mp4'
AD = '/home/user/ai/akcijos-filmukas/tiktok-serija/beribus-tiktok-{:02d}.mp4'
# id, start, cut, speed, ambience, impact, ad number
CLIPS = [
    ('3TmWPDuELMY', 3.40, 5.02, 1.0, 'outdoor', 'glass', 3),
    ('1-HurfpFA6w', 1.50, 2.98, 1.0, 'crowd', 'crowd', 10),
    ('BdLWedGBmQY', 0.10, 0.93, 1.0, 'room', 'glass', 5),
    ('5RgxLaOxy1I', 0.40, 1.68, 1.0, 'outdoor', 'bonk', 7),
    ('62cWxOf_U2Y', 3.20, 4.52, 1.0, 'crowd', 'glass', 8),
    ('8secrAaUQ3E', 0.00, 1.10, 1.0, 'outdoor', 'thud', 6),
    ('JEv-Zg2Te7s', 0.00, 1.30, 1.0, 'room', 'thud', 2),
    ('1crEC5tmjnM', 0.30, 2.10, 1.0, 'outdoor', 'thud', 1),
    ('0FLmfZzIfTs', 0.00, 0.62, 0.8, 'room', 'glass', 4),
    ('COymYK9JEIc', 0.20, 1.00, 1.0, 'room', 'glass', 9),
]
FREEZE = 0.22


def glass(gain=0.5):
    dur = 0.9
    t = t_axis(dur)
    s = highpass(noise(dur), 3000) * env(len(t), 0.001, 0.25, 3)
    for _ in range(18):
        f = np.random.uniform(3000, 9000); st = int(np.random.uniform(0, 0.4) * SR)
        g = np.sin(2 * math.pi * f * t_axis(0.12)) * env(int(SR * 0.12), 0.001, 0.05, 4)
        s[st:st + len(g)] += g[:len(s) - st] * 0.3
    return s / (np.abs(s).max() + 1e-9) * gain


def ambience(kind, dur):
    t = t_axis(dur)
    if kind == 'crowd':
        s = lowpass(noise(dur), 1200) * (0.7 + 0.3 * np.sin(2 * math.pi * 0.7 * t)); g = 0.12
    elif kind == 'outdoor':
        s = lowpass(noise(dur), 500); g = 0.06
    else:
        s = lowpass(noise(dur), 250); g = 0.04
    s = s / (np.abs(s).max() + 1e-9) * g
    return s * np.clip(t / 0.05, 0, 1)


def meme_audio(kind, impact, seg, path):
    total = seg + FREEZE
    out = np.zeros(int(SR * (total + 1.5)))
    a = ambience(kind, seg); out[:len(a)] += a
    i = int(seg * SR)
    hits = [vine_boom(0.8)]
    if impact == 'glass': hits.append(glass(0.45))
    elif impact == 'thud': hits.append(thud(0.5))
    elif impact == 'bonk': hits.append(boing(0.35, up=False))
    elif impact == 'crowd':
        o = lowpass(noise(1.2), 900) * env(int(SR * 1.2), 0.15, 0.6, 2); hits.append(o / np.abs(o).max() * 0.35)
    if kind != 'room': hits.append(whoosh(0.35, 800, 4000, 0.15))
    for h in hits:
        j = max(0, i - int(0.01 * SR)); seg_ = h[:len(out) - j]; out[j:j + len(seg_)] += seg_
    out = out[:int(SR * total)]
    out = np.tanh(out * 1.3) / np.tanh(1.3)
    pcm = (np.clip(out, -1, 1) * 32767 * 0.9).astype(np.int16)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(48000); w.writeframes(np.repeat(pcm[:, None], 2, axis=1).tobytes())


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: print(r.stderr[-1500:]); raise SystemExit(1)


def probe(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'csv=p=0', path], capture_output=True, text=True).stdout.strip()
    return [int(x) for x in out.split(',')]


caps_h = {}
for k, (cid, st, cut, speed, amb, imp, ad) in enumerate(CLIPS, 1):
    if len(sys.argv) > 1 and str(k) not in sys.argv[1:]: continue
    src = C.format(cid)
    w, h = probe(src)
    sc = min(1080 / w, 1250 / h); fw, fh = int(w * sc) // 2 * 2, int(h * sc) // 2 * 2
    fy = int(1920 * 0.56 - fh / 2)
    cap = f'memecut/cap{k}.png'; ch = probe(cap)[1]
    cy = max(260, fy - ch - 36)
    seg = (cut - st) / speed
    D = seg + FREEZE
    meme = f'memecut/meme{k}.mp4'
    flt = (f"[0:v]setpts=(PTS-STARTPTS)/{speed},fps=60,split[a][b];"
           f"[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=28:2,eq=brightness=-0.22:saturation=0.8[bg];"
           f"[b]scale={fw}:{fh}[fg];[bg][fg]overlay=(W-w)/2:{fy}[v1];[v1][1:v]overlay=0:{cy},"
           f"tpad=stop_mode=clone:stop_duration={FREEZE},"
           # punch-in during the freeze, then flash to white
           f"zoompan=z='if(gte(in_time,{seg:.3f}),1+0.18*min(1,(in_time-{seg:.3f})/{FREEZE}),1)':x='iw/2-(iw/zoom/2)':y='{fy + fh/2}-(ih/zoom/2)':d=1:s=1080x1920:fps=60,"
           f"fade=t=out:st={D - 0.07:.3f}:d=0.07:color=white,format=yuv420p[v]")
    run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(st), '-t', str(cut - st), '-i', src, '-i', cap, '-filter_complex', flt, '-map', '[v]', '-t', f'{D:.3f}', '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', '60', meme])
    wav = f'memecut/meme{k}.wav'; meme_audio(amb, imp, seg, wav)
    out = f'memecut/beribus-meme-{k:02d}.mp4'
    run(['ffmpeg', '-y', '-loglevel', 'error', '-i', meme, '-i', wav, '-i', AD.format(ad),
         '-filter_complex', f"[2:v]fade=t=in:st=0:d=0.14:color=white,fps=60,setsar=1,format=yuv420p[adv];[2:a]aresample=48000,aformat=channel_layouts=stereo[ada];[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{D:.3f}[ma];[0:v]setsar=1,format=yuv420p[mv];[mv][ma][adv][ada]concat=n=2:v=1:a=1[v][a0];[a0]loudnorm=I=-16:TP=-1.5:LRA=11[a]",
         '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '19', '-pix_fmt', 'yuv420p', '-r', '60', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', out])
    print(k, cid, f'meme {seg:.2f}s +freeze', '-> ad', ad, out)
