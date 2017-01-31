cmake_minimum_required (VERSION 2.8.11)
project (iOSTools)
if(WIN32)
find_package(OpenSSL)
include_directories(win/include)
else()
include_directories(mac/include)
find_package(OpenSSL REQUIRED)
include_directories(${OPENSSL_INCLUDE_DIR})
endif()
include_directories(libraries/include)

#------------------------------------------------------------------
# LIBRARIES
#------------------------------------------------------------------

#LIBLZFSE
add_library(lzfse SHARED
  libraries/lzfse/lzfse_decode.c
  libraries/lzfse/lzfse_decode_base.c
  libraries/lzfse/lzfse_encode.c
  libraries/lzfse/lzfse_encode_base.c
  libraries/lzfse/lzfse_fse.c
  libraries/lzfse/lzvn_decode_base.c
  libraries/lzfse/lzvn_encode_base.c)
include_directories(libraries/lzfse)

#LIBCNARY
add_library(libcnary SHARED
  libraries/libcnary/cnary.c
  libraries/libcnary/iterator.c
  libraries/libcnary/list.c
  libraries/libcnary/node.c
  libraries/libcnary/node_iterator.c
  libraries/libcnary/node_list.c)

#LIBPLIST
add_library(libplist SHARED
  libraries/libplist/Array.cpp
  libraries/libplist/base64.c
  libraries/libplist/Boolean.cpp
  libraries/libplist/bplist.c
  libraries/libplist/bytearray.c
  libraries/libplist/Data.cpp
  libraries/libplist/Date.cpp
  libraries/libplist/Dictionary.cpp
  libraries/libplist/hashtable.c
  libraries/libplist/Integer.cpp
  libraries/libplist/Key.cpp
  libraries/libplist/Node.cpp
  libraries/libplist/plist.c
  libraries/libplist/ptrarray.c
  libraries/libplist/Real.cpp
  libraries/libplist/String.cpp
  libraries/libplist/Structure.cpp
  libraries/libplist/time64.c
  libraries/libplist/Uid.cpp
  libraries/libplist/xplist.c)
target_link_libraries(libplist libcnary)

#LIBUSBMUXD
add_library(libusbmuxd SHARED 
  libraries/libusbmuxd/libusbmuxd.c
  libraries/libusbmuxd/collection.c
  libraries/libusbmuxd/socket.c)
target_link_libraries(libusbmuxd libplist)

#LIBUSB
set(libusb_shared_sources libraries/libusb/core.c
  libraries/libusb/descriptor.c
  libraries/libusb/hotplug.c
  libraries/libusb/io.c
  libraries/libusb/strerror.c
  libraries/libusb/sync.c)
if(APPLE)
set(libusb_os_sources libraries/libusb/os/darwin_usb.c)
elseif(WIN32)
set(libusb_os_sources libraries/libusb/os/windows_nt_common.c
  libraries/libusb/os/windows_usbdk.c
  libraries/libusb/os/windows_winusb.c)
else()
set(libusb_os_sources libraries/libusb/os/linux_netlink.c
  libraries/libusb/os/linux_udev.c
  libraries/libusb/os/linux_usbfs.c)
endif()
if(UNIX)
set(libusb_platform_sources libraries/libusb/os/poll_posix.c
  libraries/libusb/os/threads_posix.c)
elseif(WIN32)
set(libusb_platform_sources libraries/libusb/os/poll_windows.c
  libraries/libusb/os/threads_windows.c)
endif()
add_library(libusb SHARED ${libusb_shared_sources} ${libusb_os_sources} ${libusb_platform_sources})
if(APPLE)
target_link_libraries(libusb "-framework CoreFoundation")
target_link_libraries(libusb "-framework IOKit")
set_target_properties(libusb PROPERTIES LINK_FLAGS "-Wl,-F/Library/Frameworks")
endif()

#------------------------------------------------------------------
# TOOLS
#------------------------------------------------------------------

#8900strip
add_executable (8900strip tools/8900strip/8900strip.c)

#checkdmgencrypt
add_executable (checkdmgencrypt tools/checkdmgencrypt/checkdmgencrypt.c)

#decompkernelcache
add_executable (decompkernelcache tools/decompkernelcache/decompkernelcache.c)
target_link_libraries(decompkernelcache lzfse)

#plistutil
add_executable(plistutil tools/plistutil/plistutil.c)
target_link_libraries(plistutil libplist)

#plistutil
add_executable(iproxy tools/iproxy/iproxy.c)
target_link_libraries(iproxy libusbmuxd)

#kcache
add_executable (kcache tools/kcache/crypto.c tools/kcache/kcache.c tools/kcache/lzss.c tools/kcache/util.c)
if(WIN32)
TARGET_LINK_LIBRARIES(kcache ../win/ssleay32)
TARGET_LINK_LIBRARIES(kcache ../win/libeay32)
else()
TARGET_LINK_LIBRARIES(kcache ${OPENSSL_LIBRARIES})
endif()

#genpass
if(WIN32)
add_executable (genpass tools/genpass/genpass.cpp win/getopt.c)
TARGET_LINK_LIBRARIES(genpass ../win/ssleay32)
TARGET_LINK_LIBRARIES(genpass ../win/libeay32)
else()
add_executable (genpass tools/genpass/genpass.cpp)
TARGET_LINK_LIBRARIES(genpass ${OPENSSL_LIBRARIES})
endif()

#vfdecrypt
if (WIN32)
add_executable (vfdecrypt tools/vfdecrypt/vfdecrypt.c win/getopt.c)
TARGET_LINK_LIBRARIES(vfdecrypt ../win/ssleay32)
TARGET_LINK_LIBRARIES(vfdecrypt ../win/libeay32)
target_link_libraries(vfdecrypt wsock32 ws2_32)
else()
add_executable (vfdecrypt tools/vfdecrypt/vfdecrypt.c)
TARGET_LINK_LIBRARIES(vfdecrypt ${OPENSSL_LIBRARIES})
endif()