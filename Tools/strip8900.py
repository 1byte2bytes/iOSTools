import sys
import os.path

def log_info(message):
    print("[INFO   ] {}".format(message))

def print_help():
    print("strip8900 [input file] [output file]")

if len(sys.argv) != 3:
    print_help()
    sys.exit(3)

if os.path.isfile(sys.argv[1]):
    pass
else:
    print_help()
    sys.exit(1)

file_bytes = b''
with open(sys.argv[1], 'rb') as f:
    file_bytes = f.read()
    if file_bytes.startswith(b'89001.0'):
        file_bytes = file_bytes[2048:]
        log_info("8900 header has been stripped")
    else:
        log_info("No 8900 v1.0 header found")
        sys.exit(2)
with open(sys.argv[2], 'wb') as f:
    f.write(file_bytes)