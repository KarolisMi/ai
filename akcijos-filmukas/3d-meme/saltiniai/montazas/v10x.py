"""Videos 43-52 at 25 fps: smooth native-speed meme -> 2D ad."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compose import run, ROOT
import v2d4
B = "build"
C = lambda p: os.path.join(ROOT, "clips", p)
MEMES = {43: ("cand/c_3TmWPDuELMY.mp4", 1.40, 5.0, "fill"), 44: ("n2/Aoy8uk5ipLM.mp4", 0, 3.8, "w"), 45: ("n10/FWUxbVp16cQ.mp4", 0, 1.97, "w"),
         46: ("n10/0wNGrM645sE.mp4", 0, 0.94, "w"), 47: ("n10/8uD_jl3sbQA.mp4", 0, 1.35, "w"), 48: ("n2/BV9T1tAszdk.mp4", 0, 1.45, "w"),
         49: ("cand/c_0FLmfZzIfTs.mp4", 0, 0.62, "w"), 50: ("n4/-xU-Yn9L8NM.mp4", 0, 2.4, "w"), 51: ("n3/-2N17Wz57lI.mp4", 0, 3.1, "w"), 52: ("n4/-3X5qtK0rCE.mp4", 0, 3.22, "w")}
MUSIC = {43: (410, 15.356), 44: (726, 14.388), 45: (1127, 10.906), 46: (126, 13.846), 47: (369, 13.712), 48: (305, 12.638), 49: (403, 14.765), 50: (416, 14.753), 51: (369, 13.712), 52: (726, 14.388)}
v2d4.MUSIC.update(MUSIC)


def prep(k):
    f, a, b, mode = MEMES[k]
    loop = "-stream_loop 1" if k == 45 else ""
    if mode == "fill":
        chain = f"[0:v]trim=start={a}:end={b},setpts=PTS-STARTPTS,fps=25,scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,unsharp=5:5:0.5,format=yuv420p[v]"
    else:
        dur = f"trim=start={a}:end={b if k != 45 else 3.94},"
        chain = (f"[0:v]{dur}setpts=PTS-STARTPTS,fps=25,split[x][y];[x]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:2,eq=brightness=-0.25[bg];"
                 f"[y]scale=1080:-2:flags=lanczos,unsharp=5:5:0.5[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,format=yuv420p[v]")
    args = ["ffmpeg", "-y", "-loglevel", "error"] + (["-stream_loop", "1"] if k == 45 else []) + ["-i", C(f), "-filter_complex", chain, "-map", "[v]", "-c:v", "libx264", "-crf", "16", "-r", "25", f"{B}/m{k}.mp4"]
    run(args)
    run(["ffmpeg", "-y", "-loglevel", "error", "-sseof", "-0.04", "-i", f"{B}/m{k}.mp4", "-frames:v", "1", "-update", "1", f"{B}/m{k}_last.png"])


def cues(k, M, T):
    c = [(0, v2d4.music(k, M, T))]
    fx = v2d4.fx
    a = lambda dt, s: c.append((M + dt, s))
    c.append((max(0, M - 0.8), fx(790, 0.45, 0.8)))
    end = 5.2
    if k == 43:
        a(0.0, fx(1492, 0.6)); a(0.45, fx(759, 0.9)); a(0.45, fx(1143, 0.7)); a(0.5, fx(2951, 0.5, 0.5)); a(0.9, fx(2059, 0.6)); a(2.5, fx(2067, 0.5)); a(3.7, fx(2364, 0.5)); end = 5.1
    elif k == 44:
        a(0.0, fx(2150, 0.7))
        for i in range(7): a(0.5 + i * 0.32, fx(2354, 0.5))
        a(4.5, fx(1490, 0.5)); a(4.6, fx(2352, 0.4, 1.0)); end = 5.4
    elif k == 45:
        a(0.0, fx(948, 0.5, 0.6)); [a(0.7 + i * 0.35, fx(1110, 0.45)) for i in range(3)]; a(3.0, fx(1462, 0.5)); [a(3.6 + i * 0.3, fx(2364, 0.5)) for i in range(3)]; a(4.6, fx(2059, 0.6)); a(4.6, fx(2067, 0.5)); end = 5.5
    elif k == 46:
        a(0.0, fx(1704, 0.9)); [a(0.6 + i * 0.6, fx(2299, 0.5)) for i in range(5)]; a(3.4, fx(1143, 0.8)); a(3.6, fx(788, 0.8, 2.0)); a(3.6, fx(1714 if os.path.exists(os.path.join(v2d4.LIB, "fx", "1714.mp3")) else 1492, 0.8)); end = 5.6
    elif k == 47:
        a(0.0, fx(2155, 0.9)); a(0.05, fx(759, 0.6)); a(1.0, fx(1490, 0.5)); a(2.6, fx(2865, 0.6)); [a(3.2 + i * 0.3, fx(2357, 0.4)) for i in range(3)]
    elif k == 48:
        a(0.0, fx(2150, 0.8)); a(0.3, fx(2531 if os.path.exists(os.path.join(v2d4.LIB, "fx", "2531.mp3")) else 1119, 0.6, 2.4)); a(2.7, fx(1133, 0.6)); a(3.0, fx(2155, 0.6)); a(3.05, fx(2067, 0.5))
    elif k == 49:
        a(0.0, fx(2155, 0.9)); a(0.3, fx(1492, 0.4)); [a(0.3 + i * 0.25, fx(2072, 0.25, 0.15)) for i in range(10)]; a(2.9, fx(2863 if os.path.exists(os.path.join(v2d4.LIB, "fx", "2863.mp3")) else 2869, 0.7)); a(3.0, fx(1523 if os.path.exists(os.path.join(v2d4.LIB, "fx", "1523.mp3")) else 1530, 0.6)); end = 5.3
    elif k == 50:
        a(0.0, fx(1317, 0.6)); [a(0.8 + i * 0.22, fx(2925, 0.5)) for i in range(9)]; a(3.0, fx(2352, 0.5, 1.0)); a(3.05, fx(2357, 0.6))
    elif k == 51:
        a(0.0, fx(2150, 0.6)); a(0.85, fx(1530, 0.4, 0.9)); a(1.8, fx(2352, 0.5, 1.0)); a(3.3, fx(1530, 0.4, 0.7)); a(4.0, fx(2865, 0.6)); end = 5.4
    elif k == 52:
        a(0.0, fx(1462, 0.8)); a(0.05, fx(2155, 0.5)); a(2.2, fx(1464, 0.4)); end = 4.9
    c += [(M + end + 0.25, fx(1464, 0.5)), (M + end + 0.55, fx(2364, 0.6)), (M + end + 0.75, fx(2869, 0.45))]
    return c


def build(k):
    M, A = v2d4.dur(f"{B}/m{k}.mp4"), v2d4.dur(f"{B}/mg/seg{k}.mp4"); T = M + A
    v2d4.mix(cues(k, M, T), T, f"{B}/v{k}.wav")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{B}/m{k}.mp4", "-i", f"{B}/mg/seg{k}.mp4", "-i", f"{B}/v{k}.wav", "-filter_complex",
         "[0:v]setsar=1,fps=25,format=yuv420p[a0];[1:v]setsar=1,fps=25,format=yuv420p[b0];[a0][b0]concat=n=2:v=1:a=0[v];[2:a]loudnorm=I=-14:TP=-1.2:LRA=9[a]",
         "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "20", "-preset", "slow", "-maxrate", "14M", "-bufsize", "28M", "-pix_fmt", "yuv420p", "-r", "25",
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", f"{B}/beribus-{k}.mp4"])
    print("done", k, round(M, 2), round(T, 2))


if __name__ == "__main__":
    mode, ids = sys.argv[1], [int(x) for x in sys.argv[2:]]
    for k in ids:
        prep(k) if mode == "prep" else build(k)
