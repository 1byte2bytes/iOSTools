cmake_minimum_required (VERSION 2.8.11)
project (iOSTools)
add_executable (8900strip 8900strip/8900strip.c)
add_executable (checkdmgencrypt checkdmgencrypt/checkdmgencrypt.c)
add_executable (decompkernelcache decompkernelcache/decompkernelcache.c)
add_library(lzfse
  lzfse/lzfse_decode.c
  lzfse/lzfse_decode_base.c
  lzfse/lzfse_encode.c
  lzfse/lzfse_encode_base.c
  lzfse/lzfse_fse.c
  lzfse/lzvn_decode_base.c
  lzfse/lzvn_encode_base.c)
include_directories(lzfse)
target_link_libraries(decompkernelcache lzfse)
add_executable (kcache kcache/crypto.c kcache/kcache.c kcache/lzss.c kcache/util.c)
if (WIN32)
add_executable (genpass genpass/genpass.cpp win/getopt.c)
include_directories(win/include)
TARGET_LINK_LIBRARIES(genpass ../win/ssleay32)
TARGET_LINK_LIBRARIES(genpass ../win/libeay32)
add_executable (vfdecrypt vfdecrypt/vfdecrypt.c win/getopt.c)
TARGET_LINK_LIBRARIES(vfdecrypt ../win/ssleay32)
TARGET_LINK_LIBRARIES(vfdecrypt ../win/libeay32)
target_link_libraries(vfdecrypt wsock32 ws2_32)
else()
include_directories(mac/include)
add_executable (genpass genpass/genpass.cpp)
add_executable (vfdecrypt vfdecrypt/vfdecrypt.c)
find_package(OpenSSL)
include_directories(${OPENSSL_INCLUDE_DIR})
TARGET_LINK_LIBRARIES(genpass ${OPENSSL_LIBRARIES})
TARGET_LINK_LIBRARIES(vfdecrypt ${OPENSSL_LIBRARIES})
TARGET_LINK_LIBRARIES(kcache ${OPENSSL_LIBRARIES})
endif()