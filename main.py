from ant_simulation import Simulation
import matplotlib.pyplot as plt
import numpy as np

def main():
    np.random.seed(2)
    sim = Simulation()

    plots = [0, 20, 80, 200, 800, 3000, 10000]
    diff_plots = np.diff(plots)

    for p in range(len(diff_plots)):
        plt.subplot(2, 3, p+1)
        sim.loop(diff_plots[p])
        sim.draw()
        plt.colorbar()
        plt.title(str(plots[p+1]) + " Steps")
        print("Iterated " + str(plots[p+1]) + " steps")

    plt.show()

if __name__=="__main__":
    main()