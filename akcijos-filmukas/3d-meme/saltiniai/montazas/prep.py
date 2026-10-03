"""Prepare meme clips, shatter frames and screen sequences for videos 02-10."""
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compose import meme_clip, run, ROOT, FPS
B = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build")
C = lambda n: os.path.join(ROOT, "clips/cand", n)
# impact memes: clip up to the hit, last frame for the shatter
IMPACT = {2: ("c_BdLWedGBmQY.mp4", 0.10, 0.90, 1.0), 3: ("c_62cWxOf_U2Y.mp4", 3.10, 4.47, 1.0),
          4: ("c_COymYK9JEIc.mp4", 0.20, 0.99, 1.0), 5: ("c_0FLmfZzIfTs.mp4", 0.00, 0.60, 0.8)}
for k, (f, a, b, sp) in IMPACT.items():
    out = os.path.join(B, f"m{k:02d}.mp4")
    meme_clip(C(f), a, b, out, speed=sp)
    run(["ffmpeg", "-y", "-loglevel", "error", "-sseof", "-0.06", "-i", out, "-frames:v", "1", "-update", "1", os.path.join(B, f"m{k:02d}_last.png")])
    print("impact", k)
# pull-out memes: meme full screen for M seconds, then it keeps playing on the device
PULL = {6: ("r_6Ld7VlcJy88.mp4", 2.2, 4), 7: ("r_AWASe9GYqt8.mp4", 2.2, 5), 8: ("r_1QndkaCy0k4.mp4", 2.1, 3),
        9: ("r_2AxoijXH2lo.mp4", 2.3, 3), 10: ("r_3eIvVsG3yPY.mp4", 2.4, 2)}
for k, (f, M, loops) in PULL.items():
    full = os.path.join(B, f"mfull{k:02d}.mp4")
    meme_clip(C(f), 0, M + 4.0, full, loops=loops)
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", full, "-t", f"{M}", "-c", "copy", os.path.join(B, f"m{k:02d}.mp4")])
    sd = os.path.join(B, f"seq{k:02d}")
    os.makedirs(sd, exist_ok=True)
    run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{M}", "-i", full, "-vf", "scale=720:1280", "-start_number", "1", os.path.join(sd, "s_%04d.png")])
    print("pull", k, len(os.listdir(sd)))
