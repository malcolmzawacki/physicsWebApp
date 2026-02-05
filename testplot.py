def mandelbrot(x, y, threshold):
    """Calculates whether the number c = x + i*y belongs to the 
    Mandelbrot set. In order to belong, the sequence z[i + 1] = z[i]**2 + c
    must not diverge after 'threshold' number of steps. The sequence diverges
    if the absolute value of z[i+1] is greater than 4.
    
    :param float x: the x component of the initial complex number
    :param float y: the y component of the initial complex number
    :param int threshold: the number of iterations to considered it converged
    """
    # initial conditions
    c = complex(x, y)
    z = complex(0, 0)
    
    for i in range(threshold):
        z = z**2 + c
        if abs(z) > 4.:  # it diverged
            return i
        
    return threshold - 1  # it didn't diverge


def julia_quadratic(zx, zy, cx, cy, threshold):
    """Calculates whether the number z[0] = zx + i*zy with a constant c = x + i*y
    belongs to the Julia set. In order to belong, the sequence 
    z[i + 1] = z[i]**2 + c, must not diverge after 'threshold' number of steps.
    The sequence diverges if the absolute value of z[i+1] is greater than 4.
    
    :param float zx: the x component of z[0]
    :param float zy: the y component of z[0]
    :param float cx: the x component of the constant c
    :param float cy: the y component of the constant c
    :param int threshold: the number of iterations to considered it converged
    """
    # initial conditions
    z = complex(zx, zy)
    c = complex(cx, cy)
    
    for i in range(threshold):
        z = z**2 + c
        if abs(z) > 4.:  # it diverged
            return i
        
    return threshold - 1  # it didn't diverge

import numpy as np
import matplotlib.pyplot as plt

W, H = 6, 6
depth_max = 7
shrink = 0.67
branch_angle_base = np.deg2rad(28)
frames = 60
fps = 20
outfile = "fractal_canopy.gif"

grow_frames = int(frames*0.4)

def draw_branch(ax, x,  y, length, theta, depth, angle_variation):
    if depth == 0 or length < 1e-3:
        return
    x2 = x + length * np.cos(theta)
    y2 = y + length * np.sin(theta)

    ax.plot([x,x2], [y, y2], linewidth = max(0.5, depth/2), color='g')
    new_len = length * shrink
    left = theta + (branch_angle_base + angle_variation)
    right = theta - (branch_angle_base + angle_variation)
    draw_branch(ax, x2, y2, new_len, left, depth - 1, angle_variation*0.9)
    draw_branch(ax, x2, y2, new_len, right, depth - 1, angle_variation*0.9)


depth_schedule = []
angle_schedule = []

for f in range(frames):
    if f < grow_frames:
        d = 2 + (depth_max - 2) * (f / max(1, grow_frames - 1))
        depth_schedule.append(int(round(d)))
        angle_schedule.append(0.0)
    else:
        depth_schedule.append(depth_max)
        t = (f - grow_frames) / (frames - grow_frames)
        sway = np.deg2rad(10) * np.sin(2 * np.pi * (t * 0.75))
        angle_schedule.append(sway)

fig = plt.figure(figsize=(W, H), dpi=100)
ax = plt.gca()
ax.set_aspect('equal')
ax.axis('off')

est_height = 0
L = 1.0

for _ in range(depth_max):
    est_height += L
    L *= shrink
margin = 0.1 * est_height
xlim = (-est_height/2 - margin, est_height/2 +margin)
ylim = (0, est_height + margin)

def init():
    ax.clear()
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    return []

def update(frame):
    ax.clear()
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    depth = depth_schedule[frame]
    angle_variation = angle_schedule[frame]
    draw_branch(ax, 0.0, 0.0, 1.0, np.pi/2, depth, angle_variation)
    return []

#anim = FuncAnimation(fig, update, init_func=init,frames = frames, blit = False, interval = 1000/fps)
#anim.save(outfile, writer=PillowWriter(fps=fps))

