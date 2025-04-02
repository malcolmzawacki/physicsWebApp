import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

def plot():
    interval = (2.8, 4)  # start, end
    accuracy = 0.001
    reps = 600  # number of repetitions
    numtoplot = 200
    lims = np.zeros(reps)

    fig, biax = plt.subplots()
    fig.set_size_inches(16, 9)

    lims[0] = np.random.rand()
    for r in np.arange(interval[0], interval[1], accuracy):
        for i in range(reps - 1):
            lims[i + 1] = r * lims[i] * (1 - lims[i])

        biax.plot([r] * numtoplot, lims[reps - numtoplot :], "b.", markersize=0.02)

    biax.set(xlabel="r", ylabel="x", title="logistic map")
    return fig

def input_plot(start = 2.8,end = 4,accuracy=0.001,reps=600,numtoplot=200):
    interval = (start, end)  # start, end
    lims = np.zeros(reps)

    fig, biax = plt.subplots()
    fig.set_size_inches(16, 9)

    lims[0] = np.random.rand()
    for r in np.arange(interval[0], interval[1], accuracy):
        for i in range(reps - 1):
            lims[i + 1] = r * lims[i] * (1 - lims[i])

        biax.plot([r] * numtoplot, lims[reps - numtoplot :], "b.", markersize=0.02)

    biax.set(xlabel="r", ylabel="x", title="logistic map")
    return fig

def main():
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        start = st.number_input("start value",-2.0,10.0,2.8,0.1)
    with col2:
        end = st.number_input("end value",start,11.0,4.0,0.1)
    with col3:
        accuracy = st.number_input("accuracy",0.0001,0.1,0.001,0.001)
    with col4:
        reps = st.number_input("reps",2,1000,600,10)
    with col5:
        numtoplot = st.number_input("number to plot",10,500,200,10)
    fig = input_plot(start,end,accuracy,reps,numtoplot)
    st.pyplot(fig)


if __name__ == "__main__":
    main()