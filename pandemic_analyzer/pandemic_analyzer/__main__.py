import sys
import os

from pandemic_analyzer.analyzer import Analyzer


def main():
    try:
        if len(sys.argv) != 2 or not os.path.isdir(sys.argv[1]):
            print("Usage: {} [ result_directory | results_directory]".format(sys.argv[0]))
            sys.exit(1)

        dir: str = sys.argv[1]

        single_result: bool = False

        try:
            Analyzer(dir)()
            single_result = True
        except RuntimeError as error:
            pass

        if single_result:
            return

        if os.path.isdir(dir):
            results = sorted([f for f in os.listdir(dir) if os.path.isdir(os.path.join(dir, f))])

            if not len(results):
                print("No results to analyze found")
                return

            for result in results:
                path = os.path.join(dir, result)
                try:
                    Analyzer(path)()
                except RuntimeError as error:
                    print("Directory {} -".format(path), error)
    except KeyboardInterrupt:
        print("Analysis interrupted")


if __name__ == "__main__":
    main()
