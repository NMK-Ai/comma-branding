# comma-branding

Custom branding assets for Comma 3X devices.

## Contents

- `nmk_branding.png` — Branding image (1280×886)
- `splash.bmp` — Boot splash BMP (1080×2160, 24bpp, PIL bits=32)
- `install_splash.py` — Splash partition writer

## Usage

```bash
# Upload splash.bmp and install_splash.py to device
scp splash.bmp comma@<device-ip>:/tmp/splash_nmk.bmp
scp install_splash.py comma@<device-ip>:/tmp/write_splash.py

# Write to splash partition
ssh comma@<device-ip> "sudo python3 /tmp/write_splash.py /tmp/splash_nmk.bmp"

# Reboot
ssh comma@<device-ip> "sudo reboot"
```

## Format

- Partition: `/dev/disk/by-partlabel/splash` (34,226,176 bytes)
- Layout: DDPH header (16,384 bytes) + BMP (6,998,454 bytes) + padding
- BMP: 1080×2160, 24bpp, generated with PIL `bits=32`
