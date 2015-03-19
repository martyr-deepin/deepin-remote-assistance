
import subprocess

# TODO: move this module to dra_utils

def launch_app_in_background(args, shell=False):
    # TODO: check xvfb-run exists
    #args.insert(0, '/usr/bin/xvfb-run')
    return subprocess.Popen(args, shell=shell)
