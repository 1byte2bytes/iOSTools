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

#liblzfse
add_library(lzfse SHARED
  libraries/lzfse/lzfse_decode.c
  libraries/lzfse/lzfse_decode_base.c
  libraries/lzfse/lzfse_encode.c
  libraries/lzfse/lzfse_encode_base.c
  libraries/lzfse/lzfse_fse.c
  libraries/lzfse/lzvn_decode_base.c
  libraries/lzfse/lzvn_encode_base.c)
include_directories(libraries/lzfse)

add_library(libcnary SHARED
  libraries/libcnary/cnary.c
  libraries/libcnary/iterator.c
  libraries/libcnary/list.c
  libraries/libcnary/node.c
  libraries/libcnary/node_iterator.c
  libraries/libcnary/node_list.c)

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