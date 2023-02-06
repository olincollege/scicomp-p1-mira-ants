# scicomp-p1-mira-ants

I am not finished with this assignment, and I have communicated with Carrie.

## How to run

To run the code, either run `main.py`, or to run in your own code:

1. Import the simulation class
`from ant_simulation import Simulation`

2. Create a new simulation
`sim = Simulation()`
Optional parameters of Simulation:
- `shape` (default (15,15)) is a 2-element tuple that specifies the size of the simulation space
- `phermone_deposit_rate` (default 4) is the amount of phermones deposited by an ant per time step
- `fidelity` (default 5) is the threshold for the fidelity check returning `True`
- `phermone_limit` (default 10) is the maximum phermone value that the ants can detect

3. Run the simulation for a specific number of steps (for example, 200)
`sim.loop(200)`

- To run the simulation and print the array at each step, set the `print_iter` parameter of `sim.loop` to `True`
- To run the simulation and wait at each step (helpful when using `print_iter`), set the `sleep` parameter of `sim.loop` to the number of seconds to sleep. I like 0.1.

4. Print the simulation's array to see the output (note: I haven't made a proper viewer for this data)
`print(sim.array)`

### Full code to run the simulation

```
from ant_simulation import Simulation
sim = Simulation()
sim.loop(100, print_iter=True, sleep=0.1)
```