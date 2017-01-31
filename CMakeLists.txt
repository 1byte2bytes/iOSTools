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

#8900strip
add_executable (8900strip tools/8900strip/8900strip.c)

#checkdmgencrypt
add_executable (checkdmgencrypt tools/checkdmgencrypt/checkdmgencrypt.c)

#liblzfse
add_library(lzfse
  libraries/lzfse/lzfse_decode.c
  libraries/lzfse/lzfse_decode_base.c
  libraries/lzfse/lzfse_encode.c
  libraries/lzfse/lzfse_encode_base.c
  libraries/lzfse/lzfse_fse.c
  libraries/lzfse/lzvn_decode_base.c
  libraries/lzfse/lzvn_encode_base.c)
include_directories(libraries/lzfse)

#decompkernelcache
add_executable (decompkernelcache tools/decompkernelcache/decompkernelcache.c)
target_link_libraries(decompkernelcache lzfse)

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