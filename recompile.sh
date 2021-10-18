make clean
rm -rf bin
rm src/*.mod
./configure
make
make install
