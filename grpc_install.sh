
set -ex

git clone -b $(curl -L https://grpc.io/release) https://github.com/grpc/grpc
cd grpc
git submodule update --init
git submodule update --update
# git clone -b $(curl -L https://grpc.io/release) https://github.com/grpc/grpc
# echo 'export LOCAL=${HOME}/packages' >> ${HOME}/.bashrc
source ~/.bashrc

# Install c-ares
cd third_party/cares/cares
git fetch origin
git checkout cares-1_15_0
mkdir -p cmake/build
cd cmake/build
cmake -DCMAKE_BUILD_TYPE=Release ../..
make -j24 DESTDIR=${LOCAL} install
cd ../../../../..
rm -rf third_party/cares/cares  # wipe out to prevent influencing the grpc build

# Install zlib
cd third_party/zlib
mkdir -p cmake/build
cd cmake/build
cmake -DCMAKE_BUILD_TYPE=Release ../..
make -j24 DESTDIR=${LOCAL} install
cd ../../../..
rm -rf third_party/zlib  # wipe out to prevent influencing the grpc build

# Install protobuf
cd third_party/protobuf
mkdir -p cmake/build
cd cmake/build
cmake -Dprotobuf_BUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release ..
make -j24 DESTDIR=${LOCAL} install
cd ../../../..
rm -rf third_party/protobuf  # wipe out to prevent influencing the grpc build

# Install gRPC
mkdir -p cmake/build
cd cmake/build
cmake -DgRPC_INSTALL=ON -DCMAKE_PREFIX_PATH=${LOCAL}/usr/local -DgRPC_BUILD_TESTS=OFF -DgRPC_PROTOBUF_PROVIDER=package -DgRPC_ZLIB_PROVIDER=package -DgRPC_CARES_PROVIDER=package -DgRPC_SSL_PROVIDER=package -DCMAKE_BUILD_TYPE=Release ../..
make -j24 DESTDIR=${LOCAL} install
cd ../..

# Build helloworld example using cmake
cd examples/cpp/helloworld
mkdir -p cmake/build
cd cmake/build
cmake -DCMAKE_PREFIX_PATH=${LOCAL}/usr/local -DgRPC_DIR=${LOCAL}/lib/cmake/grpc ../..
make
