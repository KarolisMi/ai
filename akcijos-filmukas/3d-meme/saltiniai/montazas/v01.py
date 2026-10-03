"""Video 01 · Baseball into the lens -> 3D price smash."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compose import *  # noqa

D = os.path.join(HERE, "build")
os.makedirs(D, exist_ok=True)
meme = os.path.join(D, "m01.mp4")
ad = os.path.join(D, "a01.mp4")
M = meme_clip(os.path.join(ROOT, "clips/cand/c_3TmWPDuELMY.mp4"), 1.40, 5.045, meme, fill=True, zoom_end=(0.55, 0.6, 0.6, 0.12))
ad_clip(os.path.join(ROOT, "b3d/out/ad1"), ad, zoom_in=(0.25, 0.3))
A = 204 / FPS
T = M + A
f = lambda fr: M + (fr - 1) / FPS  # ad frame -> seconds

c = []
# meme: field ambience, the hit, the ball screaming toward the lens
amb = lowpass(noise(M), 600)
c.append((0, amb / abs(amb).max() * 0.05))
c.append((M - 0.48, crack(0.55)))
c.append((M - 0.45, riser(0.45, 0.35)))
c.append((M - 0.03, sub_drop(0.75, 1.6)))
c.append((M - 0.02, whoosh(0.5, 300, 5000, 0.45)))
# 3D: ball flies away and smashes the old price
c.append((f(2), whoosh(0.7, 200, 2500, 0.3)))
c.append((f(16), boom(0.7, 1.4)))
c.append((f(16), crack(0.35)))
c += clatter(26, f(18), 2.2)
# €100 drops in
c.append((f(56), whoosh(0.6, 2500, 300, 0.3)))
c.append((f(74), sub_drop(0.6, 1.2)))
c.append((f(74), thud(0.45)))
c.append((f(79), thud(0.18)))
c.append((f(85), thud(0.08)))
c.append((f(75), shimmer(1.0, 0.12)))
# copy and CTA
c.append((f(98), whoosh(0.4, 600, 4000, 0.16)))
c.append((f(108), whoosh(0.4, 600, 4000, 0.16)))
c.append((f(150), whoosh(0.4, 3000, 500, 0.14)))
c.append((f(158), pop(520, 0.3)))
c.append((f(168), ding(0.25)))
# music bed: low pad from the cut, pulse once the price lands
c.append((M, pad(A, gain=0.09)))
c += pulse_bed(f(74), T - 0.3, bpm=100, gain=0.9)
wav = os.path.join(D, "v01.wav")
mixdown(c, T, wav)
out = os.path.join(D, "beribus-3d-01.mp4")
join(meme, ad, wav, out)
print("done", out, round(T, 2))
