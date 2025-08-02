"""
PHYS 325 Final Project
Soren Gabor

SFX Generator: https://sfxr.me
"""

import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir('/Users/soren/Documents/UST/spring2025/comp_phys/phys325-repo-sorenair/')
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from SimLib import render_final
from SimLib import animate_final

def main():
    # Set up and run simulation
    ts = 0.00075
    render_engine = render_final.NBodyRender(screen_size=[1500,900])
    animation_engine = animate_final.Animate(render=render_engine, screen_size=[1500,900], timescale=ts)
    animation_engine.run()

if __name__=="__main__":
    main()