
import subprocess

def pkill(path):
    '''Call `pkill -f path` command'''
    subprocess.call(['pkill', '-f', path])
