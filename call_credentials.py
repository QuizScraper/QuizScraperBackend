import subprocess
subprocess.call(['chmod', 'a+x', './credentials.sh'])
subprocess.call("./credentials.sh")
