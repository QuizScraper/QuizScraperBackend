import subprocess
subprocess.call(['chmod', '0777', './credentials.sh'])
subprocess.call('./credentials.sh')
