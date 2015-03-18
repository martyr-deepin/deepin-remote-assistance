
import subprocess


def launch_app_in_background(args):
    return subprocess.Popen(args, shell=False)
