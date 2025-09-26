import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
plt.style.use("dark_background")

def input_plot(start = 2.8,end = 4,accuracy=0.001,reps=600,numtoplot=200):
    interval = (start, end)  # start, end
    lims = np.zeros(reps)
    numtoplot = reps - 1
    fig, biax = plt.subplots()
    fig.set_size_inches(16, 9)

    lims[0] = np.random.rand()
    size_of_marker =0.02
    for r in np.arange(interval[0], interval[1], accuracy):
        for i in range(reps - 1):
            lims[i + 1] = r * lims[i] * (1 - lims[i])

        biax.plot([r] * numtoplot, lims[reps - numtoplot :], "y.", markersize=size_of_marker)

    biax.set(xlabel="r", ylabel="x", title="logistic map")
    plt.style.use("dark_background")
    return fig

def main():
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        start = st.number_input("start value",-2.0,3.9,2.0,0.1)
    with col2:
        end = st.number_input("end value",-2.0,4.0,4.0,0.1)
    with col3:
        accuracy = st.number_input("accuracy",0.001,0.1,0.001,0.001)
    with col4:
        reps = st.number_input("reps",200,1000,800,10)
    with col5:
        numtoplot = st.number_input("number to plot",10,500,300,10)
    fig = input_plot(start,end,accuracy,reps,numtoplot)
    st.pyplot(fig)





import numpy as np
import matplotlib.pyplot as plt
from random import randint as ri


W, H = 6, 6
depth_max = 10
shrink = 0.7
branch_angle_base = np.deg2rad(20)
frames = 60
fps = 20

angle_variation = 0.0
depth = 11
grow_frames = int(frames*0.4)

def draw_branch(ax, x,  y, length, theta, depth, angle_variation, left_var=0.0, right_var = 0.0):
    if depth == 0 or length < 1e-3:
        return
    x2 = x + length * np.cos(theta)
    y2 = y + length * np.sin(theta)

    ax.plot([x,x2], [y, y2], linewidth = max(0.5, depth/2), color='g')
    new_len = length * shrink

    left = theta + (branch_angle_base + angle_variation)
    right = theta - (branch_angle_base + angle_variation)
    draw_branch(ax, x2, y2, new_len, 1.0*left, depth - 1, angle_variation*0.9)
    draw_branch(ax, x2, y2, new_len, 1.0*right, depth - 1, angle_variation*0.9)


def tree():

    fig = plt.figure(figsize=(W, H), dpi=200)
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


    ax.axis('off')
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)

    draw_branch(ax, 0.0, 0.0, 0.7, np.pi/2, depth, angle_variation, left_var=0.0, right_var = 0.0)
    st.pyplot(fig)

def fern():
    fern_x = []
    fern_y = []
    fern_x.append(0)
    fern_y.append(0)
    current = 0
    fern_max = 50000
    for i in range(1,fern_max):
        z = ri(1,100)
        if z ==1:
            fern_x.append(0)
            fern_y.append(0.16*fern_y[current])
        elif z >=2 and z <= 86:
            fern_x.append(0.85*fern_x[current] + 0.04*fern_y[current])
            fern_y.append(-0.05*fern_x[current] + 0.85*fern_y[current] + 2.6)
        elif z >= 87 and z <= 93:
            fern_x.append(0.2*fern_x[current] - 0.26 * fern_y[current])
            fern_y.append(0.23*fern_x[current] + 0.23*fern_y[current] + 1.6)
        else:
            fern_x.append(-0.15*fern_x[current] + 0.28 * fern_y[current])
            fern_y.append(0.25*fern_x[current] + 0.25*fern_y[current] + 0.44)
        
        current +=1
        ax = plt.gca()
        fig = plt.figure(dpi=200)
        plt.scatter(fern_x, fern_y, s = 0.2, edgecolor = 'g')
        plt.tight_layout()
        ax.axis('off')
        st.pyplot(fig)


def lorentz():
    dt = 0.005
    s = 10.0
    p = 28
    b = 8/3
    x = 1
    y = 0
    z = 0
    dx = s * (y - x)
    dy = x * (p - z) - y
    dz = x * y  - b * z
    fig = plt.figure()
    ax = fig.add_subplot(projection = '3d')
    xs = []
    ys = []
    zs = []


    points = 5000

    for _ in range (0,points):
        xs.append(x)
        ys.append(y)
        zs.append(z)
        x += dt*dx
        y += dt*dy
        z += dt*dz
        dx = s * (y - x)
        dy = x * (p - z) - y
        dz = x * y  - b * z
    ax.scatter(xs, ys, zs, s = 2.5, c = 'r')
    x = 1.1
    y = 0
    z = 0
    
    for _ in range (0,points):
        xs.append(x)
        ys.append(y)
        zs.append(z)
        x += dt*dx
        y += dt*dy
        z += dt*dz
        dx = s * (y - x)
        dy = x * (p - z) - y
        dz = x * y  - b * z

    ax.scatter(xs, ys, zs, s = .1, c = 'b')
    ax.view_init(elev = 10, azim = -30, roll = 0)
    st.pyplot(fig)


if __name__ == "__main__":
    lorentz()