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


def roulette():
    import random
    st.title("Roulette: Modified Martingale Strategy")
 
    st.write("Rules:")
    st.write("1. Betting ends either when all money is lost, or all rounds are played")
    st.write("2. Next bet on win is minimum")
    st.write("""3. Next bet on loss is either double last bet, 
             or table max if doubling exceeds table max, 
             or all remaining cash, if that's the least of the three options""")
    st.write("")
    # enumerate all possible outcomes from 0 to 37 (using 37 as standin for 00)
    outcomes = []
    for i in range(38):
        outcomes.append(i)

    # this is betting on black, but betting on red would be symmetric in probability
    winning_outcomes = set([2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35])

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        # set the minimum of the table
        init_bet = st.number_input("Minimum Bet", 1, 100, value = 2, step = None)
    with col2:
        # set entering money
        starting_cash = st.number_input("Starting Cash", 2, None, 5_000, step=None)
    with col3:
        # set maximum multiplier
        max_mult = st.number_input("Maximum Bet", 10, 100_000, 5_000, step=None)
    with col4:
        # set how long person is at the table
        time_limit = st.number_input("Rounds of Play", 10, 100_000, value=10_000, step=None)
    with col5:
        # set number of paths to examine
        samples = st.number_input("Samples", 10, 10_000, value=100, step=None)

    yields = []      # this will hold the results of each sample (time series)
    max_bets = []    # this will hold the largest bet each sample has to make

    for i in range(samples):
        # initialize the circumstances of each sample
        time_plot = []
        yield_plot = []
        if init_bet is None:
            init_bet = 2
        bet = init_bet
        cash = starting_cash
        time = 0
        max_bet = init_bet
        # play the game
        while time < time_limit:
            lost = False

            # spin the wheel
            result = random.choice(outcomes)
            if result in winning_outcomes:
                cash += bet
                bet = init_bet  # reset the bet on a win

            else:  # loss
                cash -= bet
                if cash <= 0: # went broke, sample is done
                    # this stops the normal generation of plotted data, and fills the remainder with last value
                    # which forces a match up in graph size
                    lost = True
                    for j in range(time, time_limit):
                        time_plot.append(j)
                        yield_plot.append(cash - starting_cash)
                    time = time_limit  # game is over, walk away

                else: # still some cash left
                    # choose the lowest of: doubling the bet, maxing out the table, remaining cash
                    bet = min(2 * bet, max_mult, cash)
                    if bet > max_bet:
                        max_bet = bet

            if not lost:
                time_plot.append(time)  # add current time step to list (for plotting)
                yield_plot.append(cash - starting_cash)  # add current yield to list (for plotting)

            time += 1  # go to next step / play

        yields.append(yield_plot)  # add sample's results to larger list
        max_bets.append(max_bet)

    # compute final yields from the plotted data so stats match the graph
    final_yields = [yp[-1] for yp in yields]

    # fraction of samples that ended with a true loss (negative net)
    negative_return_count = sum(1 for y in final_yields if y <= 0)
    negative_rate = 100 * negative_return_count / samples

    # graphing stuff
    fig = plt.figure()
    ax = fig.add_subplot()
    average_yield = []

    # add all results to the graph
    for yield_plot in yields:
        ax.plot(range(len(yield_plot)), yield_plot)
        average_yield.append(yield_plot[-1])

    with st.expander("Graph"):
        st.pyplot(fig)

    col1, col2 = st.columns(2)
    with col1:
        st.write("Maximum bet stats:")
        st.write(f"Mean: ${np.mean(max_bets):,.0f}")
        st.write(f"Median: ${np.median(max_bets):,.0f}")
        st.write(f"Max: ${max(max_bets):,.0f}")
        st.write(f"Min: ${min(max_bets):,.0f}")
    with col2:
        st.write("Payout Stats")
        st.write(f"Mean: ${np.mean(average_yield):,.0f}")
        st.write(f"Median: ${np.median(average_yield):,.0f}")
        st.write(f"Max: ${max(average_yield):,.0f}")
        st.write(f"Min: ${min(average_yield):,.0f}")
        st.write(f"Negative Return Rate: {negative_rate:.2f}%")

P_WIN = 18/38
P_LOSE = 1 - P_WIN

import random
def reverse_roulette(min_bet, max_bet, starting_cash, target_profit, max_rounds):


    cash = starting_cash
    bet = min_bet
    rounds = 0

    target_cash = starting_cash + target_profit

    while rounds < max_rounds and cash > 0 and cash < target_cash:
        # legal bet: can't exceed cash or table max
        b = min(bet, cash, max_bet)
        if b <= 0:
            break

        result = random.random()  # quicker than choice()
        if result < P_WIN:
            cash += b
            bet = min_bet
        else:
            cash -= b
            if cash <= 0:
                break
            # double up, capped by table max and remaining cash
            bet = min(2 * b, max_bet, cash)

        rounds += 1


    return cash, rounds

def planner_tab():
    st.header("martingale profit planner (simulated)")

    col1, col2, col3 = st.columns(3)
    with col1:
        min_bet = st.number_input("table minimum ($)", 1, 1_000, value=5, step=1)
        max_bet = st.number_input("table maximum ($)", min_bet, 1_000_000, value=1_000, step=10)
    with col2:
        target_profit = st.number_input("desired profit ($)", 1, 100_000, value=100, step=10)
        bankroll = st.number_input("starting bankroll ($)", min_bet, 1_000_000, value=2_000, step=50)
    with col3:
        desired_prob = st.number_input(
            "desired success probability",
            min_value=0.01,
            max_value=0.99,
            value=0.90,
            step=0.01,
        )
        max_rounds = st.number_input(
            "max spins to simulate",
            min_value=10,
            max_value=5_000,
            value=500,
            step=10,
        )

    samples = st.slider("number of simulated sessions", 100, 10_000, 2000, step=100)

    if st.button("run planner simulation"):
        successes = 0
        some_successes = 0
        break_evens = 0
        losses = 0
        total_losses = 0
        success_rounds = []
        net_profit_list = []
        for _ in range(samples):
            cash, r = reverse_roulette(
                min_bet=min_bet,
                max_bet=max_bet,
                starting_cash=bankroll,
                target_profit=target_profit,
                max_rounds=max_rounds,
            )
            success = True if cash >= (bankroll + target_profit) else False
            some_success = True if cash > bankroll else False
            break_even = True if cash == bankroll else False
            loss = True if (0 < cash) and (cash < bankroll) else False
            total_loss = True if cash == 0 else False
            if success:
                successes += 1
                success_rounds.append(r)
            if some_success:
                some_successes += 1
            if break_even:
                break_evens += 1
            if loss:
                losses += 1
            if total_loss:
                total_losses += 1
            net_profit_list.append(cash-bankroll)
        
        expected_profit = np.mean(net_profit_list)
        se = np.std(net_profit_list, ddof=1) / np.sqrt(len(net_profit_list))
        success_rate = successes / samples
        some_success_rate = some_successes / samples
        some_success_rate -= some_success_rate
        break_even_rate = break_evens / samples
        loss_rate = losses / samples
        total_loss_rate = total_losses / samples
        avg_success_rounds = np.mean(success_rounds)


        st.write(f"***complete*** **success rate:** {100*success_rate:.2f}% "
                 f"(target: {100*desired_prob:.2f}%)")
        st.write(f"**average number of spins until success:** {avg_success_rounds:.0f}")
        st.write(f"***some*** **success rate (profit, but less than target):** {100*some_success_rate:.2f}%")
        st.write(f"**break-even rate:** {100*break_even_rate:.2f}%")
        st.write(f"***some*** **loss rate (loss, but not total):** {100*loss_rate:.2f}%")
        st.write(f"***complete*** **loss rate:** {100*total_loss_rate:.2f}%")
        st.write(f"**expected outcome(\$):** {expected_profit:.0f}  $\pm$  {se:.0f}")
        if success_rate >= desired_prob:
            st.success("with these conditions, you *approximately* meet your desired success probability.")
        else:
            st.warning("with these conditions, you fall SHORT of your desired success probability.")

        st.caption(
            "note: this is a monte carlo estimate, not exact math. "
            "increase 'number of simulated sessions' for a more stable estimate (at the cost of speed)."
        )



