
import subprocess


def launch_app_in_backgrund(args):
    return subprocess.Popen(args, shell=False)
