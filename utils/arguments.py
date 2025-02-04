import argparse


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--env", "-e", help="Environment", default="glab")
    parser.add_argument("--log-level", "-l", help="Log level", default="INFO")

    return parser.parse_args()
