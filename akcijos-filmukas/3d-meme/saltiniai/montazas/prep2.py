"""Longer meme hooks (3.5-4.5 s) for videos 05, 09, 10."""
import os, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compose import meme_clip, run, ROOT, FPS
B = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build")
C = lambda n: os.path.join(ROOT, "clips/cand", n)
ids = [int(a) for a in sys.argv[1:]]
# pull-out memes: (file, hook seconds, loops, speed)
PULL = {9: ("r_2AxoijXH2lo.mp4", 3.6, 4, 0.7), 10: ("r_3eIvVsG3yPY.mp4", 3.6, 3, 0.9)}
for k in ids:
    if k in PULL:
        f, M, loops, sp = PULL[k]
        full = os.path.join(B, f"mfull{k:02d}.mp4")
        meme_clip(C(f), 0, (M + 4.0) * sp, full, loops=loops, speed=sp)
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", full, "-t", f"{M}", "-c:v", "libx264", "-crf", "16", os.path.join(B, f"m{k:02d}.mp4")])
        sd = os.path.join(B, f"seq{k:02d}")
        shutil.rmtree(sd, ignore_errors=True)
        os.makedirs(sd)
        run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{M}", "-i", full, "-vf", "scale=720:1280", "-start_number", "1", os.path.join(sd, "s_%04d.png")])
        print("pull", k, len(os.listdir(sd)))
    REPLAY = {5: ("c_0FLmfZzIfTs.mp4", 2.85, 0.0, 0.60, 0.55), 4: ("c_COymYK9JEIc.mp4", 1.30, 0.0, 0.99, 0.45)}
    if k in REPLAY:
        # full fail plays out, a fast tape rewind, then the run-up again in slow motion into the lens
        f, full_end, a0, hit, sp = REPLAY[k]
        a, r, c = (os.path.join(B, f"m{k:02d}{n}.mp4") for n in "arc")
        meme_clip(C(f), 0, full_end, a)
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", a, "-vf", "reverse,setpts=PTS/4,fps=24,eq=saturation=0.6:contrast=1.15,noise=alls=18:allf=t,format=yuv420p", "-an", "-c:v", "libx264", "-crf", "16", r])
        meme_clip(C(f), a0, hit, c, speed=sp)
        lst = os.path.join(B, f"m{k:02d}.txt")
        open(lst, "w").write("".join(f"file '{p}'\n" for p in (a, r, c)))
        run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c:v", "libx264", "-crf", "16", "-r", str(FPS), "-pix_fmt", "yuv420p", os.path.join(B, f"m{k:02d}.mp4")])
        print("replay", k)
