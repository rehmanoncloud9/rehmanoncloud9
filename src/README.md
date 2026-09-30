# Source
- build_assets.py regenerates every animated SVG in ../assets (Inter is subsetted and embedded). Needs: pip install fonttools brotli
- film/ is the 30 s promo film: film.html (canvas timeline on a 128 BPM grid), audio.py (synthesized score), render.js (Playwright + ffmpeg)
