import os
import shutil
import sys

if os.geteuid() != 0:
    print("Please run this as root.")
    sys.exit(1)


def get_current_script_dir():
    current_script_dir = os.path.realpath(__file__)
    index = current_script_dir.rindex("/")
    return current_script_dir[0:index]


try:
    current_script_dir = get_current_script_dir()
    shutil.copy(
        current_script_dir + "/../airtime-icecast-status.xsl", "/usr/share/icecast2/web"
    )

except Exception as e:
    print(f"exception: {e}")
    sys.exit(1)
