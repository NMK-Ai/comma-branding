import os, sys

PARTITION_SIZE = 34226176
HEADER_SIZE = 16384

bmp_path = sys.argv[1] if len(sys.argv) > 1 else '/tmp/splash_nmk.bmp'
with open(bmp_path, 'rb') as f:
    new_bmp = f.read()
print(f'BMP: {len(new_bmp)} bytes')

with open('/dev/disk/by-partlabel/splash', 'rb') as f:
    header = f.read(HEADER_SIZE)

new_splash = header + new_bmp
padding = PARTITION_SIZE - len(new_splash)
if padding < 0:
    print(f'ERROR: too large by {-padding}')
    sys.exit(1)
new_splash += b'\x00' * padding

fd = os.open('/dev/disk/by-partlabel/splash', os.O_WRONLY)
os.write(fd, new_splash)
os.fsync(fd)
os.close(fd)
print(f'WRITTEN: {len(new_splash)} bytes')
