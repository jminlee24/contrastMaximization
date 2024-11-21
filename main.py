import sys
import argparse
import config
import time

import contrast_max


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("-r", "--read_limit")
    p.add_argument("-t", "--time_start")
    args = p.parse_args(sys.argv[1:])

    h = -1
    t0 = config.START_TIME

    if args.read_limit:
        h = int(args.read_limit)
    if args.time_start:
        t0 = int(args.time_start)

    cm = contrast_max.ContrastMaximizer(config.RECORDING_PATH, h=h)

    start = time.time()
    res = cm.maximize_variance(t0)
    end = time.time()
    print(res)
    print(f"time elapsed: {end - start}")
    cm.plot_images()
