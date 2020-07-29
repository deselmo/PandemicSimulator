import pandemic as pd
from typing import Optional
import math
import os
import sys


def main():
    if len(sys.argv) != 2:
        print("Usage: {} [parameters_directory | parameters.json]".format(sys.argv[0]))
        sys.exit(1)

    path: str = sys.argv[1]

    if os.path.isdir(path):
        paramss = sorted([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])

        for params in paramss:
            params_file = os.path.join(path, params)

            try:
                simulator: Optional[pd.Simulator] = pd.Simulator.from_params(params_file)
            except KeyboardInterrupt:
                print("Interrupted")
                sys.exit(1)

            if simulator is None:
                print("Invalid parameters file {}".format(params_file))
                continue

            cli(simulator, params_file)

    else:
        try:
            simulator: Optional[pd.Simulator] = pd.Simulator.from_params(path)
        except KeyboardInterrupt:
            print("Interrupted during initialization")
            sys.exit(1)

        if simulator is None:
            print("Invalid parameters file {}".format(path))
            sys.exit(1)

        cli(simulator, path)


def cli(simulator: pd.Simulator, path: str) -> None:
    print("Computing {}...".format(path))

    try:
        leading_zeros: int = math.ceil(math.log(simulator.params.peers_number)/math.log(10))
        while(simulator.step()):
            print(
                "\repoch: " + str(simulator.epoch).zfill(5),
                "-",
                "susceptible: " + str(len(simulator.susceptible_peers)).zfill(leading_zeros),
                "-",
                "infected: " + str(len(simulator.infected_peers)).zfill(leading_zeros),
                "-",
                "patched: " + str(len(simulator.patched_peers)).zfill(leading_zeros),
                end="",
                flush=True
            )
        print()
    except KeyboardInterrupt:
        print("Simulation interrupted")

    simulator.output()

    if simulator.params.output_directory is not None:
        print("Graph successfully saved in '{}'".format(simulator.params.output_directory))


if __name__ == "__main__":
    main()
