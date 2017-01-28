import zipfile
import glob
import os
import os.path
import sys
import shutil

def log_debug(message):
    print("[DEBUG  ] {}".format(message))

def log_info(message):
    print("[INFO   ] {}".format(message))

def log_fatal(message):
    print("[FATAL  ] {}".format(message))

def make_folder_for_build(folder, build):
    if os.path.isdir("{}/{}".format(folder, build)):
        log_info("Clearing the {} folder".format(folder))
        shutil.rmtree("{}/{}".format(folder, build))
        log_info("Creating the {} folder".format(folder))
        os.mkdir("{}/{}".format(folder, build))
    else:
        log_info("Creating the {} folder".format(folder))
        os.mkdir("{}/{}".format(folder, build))

def strip_img2_header(filename, stripped_filename):
    file_bytes = []
    with open(filename, 'rb') as f:
        for i in range(2048):
            f.read()
        while 1:
            byte = f.read()
            file_bytes.append(byte)
            if not byte:
                break
    with open(stripped_filename, 'wb') as f:
        for byte in file_bytes:
            f.write(byte)


valid_builds = ["1A543a"]

IPSW_files = glob.glob("IPSW/*.ipsw")
for IPSW in IPSW_files:
    IPSW_split = IPSW.split("_")
    IPSW_build = ""
    log_info("Working on IPSW {}".format(IPSW))
    for build in valid_builds:
        if build in IPSW_split:
            log_info("Detected iOS build {}".format(build))
            IPSW_build = build
    if IPSW_build == "":
        log_info("{} is invalid, perhaps the build is not supported".format(IPSW))
        sys.exit(1)

    make_folder_for_build("Contents", IPSW_build)
    make_folder_for_build("Temp", IPSW_build)

    log_info("Extractiong IPSW contents")
    IPSW_zip = zipfile.ZipFile(IPSW)
    IPSW_zip.extractall("Temp/{}".format(IPSW_build))
    IPSW_zip.close()

    img2_files = glob.glob("Temp/{}/Firmware/all_flash/*/*.img2".format(build))
    for img2_file in img2_files:
        log_info("Stripping IMG2 header from {}".format(img2_file.rsplit("\\", 1)[1]))
        strip_img2_header(img2_file, "{}.stripped".format(img2_file))

        log_info("Placing stripped IMG2 file {} into Contents folder".format(img2_file.rsplit("\\", 1)[1]))
        os.makedirs(os.path.dirname("Contents/{}".format(img2_file[4:])), exist_ok=True)
        os.rename("{}.stripped".format(img2_file), "Contents/{}".format(img2_file[4:]))

    log_info("Copying manifest file into Contents folder")
    manifest_temp = glob.glob("Temp/{}/Firmware/all_flash/*/manifest".format(build))
    shutil.copyfile(manifest_temp[0], "Contents/{}".format(manifest_temp[0][4:]))