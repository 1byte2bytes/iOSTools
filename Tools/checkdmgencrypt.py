import sys
import os.path

def log_info(message):
    print("[INFO   ] {}".format(message))

def print_help():
    print("checkdmgencrypted [input file]")

if len(sys.argv) != 2:
    print_help()
    sys.exit(-1)

if os.path.isfile(sys.argv[1]):
    pass
else:
    print_help()
    sys.exit(-2)

with open(sys.argv[1], 'rb') as f:
    header = f.read(8)
    if header.startswith(b"encrcdsa"):
        log_info("The DMG is encrypted")
        sys.exit(0)
    else:
        log_info("The DMG is not encrypted")
        sys.exit(1)
