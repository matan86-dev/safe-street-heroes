"""Rebuild index.html from the carpet image.

Usage (from the repo root):
    pip install pillow numpy
    python3 source/make_assets.py assets/carpet.png   # writes assets.json (pop-up buildings + ground)
    python3 source/build.py                            # writes index.html
"""
import os
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
src = open(os.path.join(here, 'game_src.html'), encoding='utf-8').read()
assets = open(os.path.join(os.getcwd(), 'assets.json'), encoding='utf-8').read()
out = src.replace('__THREE_URL__', 'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js').replace('__ASSETS_JSON__', assets)
open(os.path.join(root, 'index.html'), 'w', encoding='utf-8').write(out)
print('index.html written')
