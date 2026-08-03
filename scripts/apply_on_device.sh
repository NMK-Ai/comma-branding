#!/usr/bin/env bash
set -euo pipefail

WORKDIR="/data/.branding"
SPLASH_PART="/dev/disk/by-partlabel/splash"
HEADER_BACKUP="$WORKDIR/splash_header_orig.bin"
CONTINUE_SH="/data/continue.sh"
HOOK_MARKER="# NMK: Hide comma boot logo permanently"

mkdir -p "$WORKDIR"

if [ ! -f "$HEADER_BACKUP" ]; then
  dd if="$SPLASH_PART" of="$HEADER_BACKUP" bs=16384 count=1 status=none
fi

PY=python3
if ! "$PY" -c "import PIL" 2>/dev/null; then
  PY=/usr/local/venv/bin/python3
fi
"$PY" "$WORKDIR/build_splash.py" "$WORKDIR/nmk_logo.png" "$HEADER_BACKUP" "$WORKDIR/splash_new.bin"
dd if="$WORKDIR/splash_new.bin" of="$SPLASH_PART" bs=1M conv=notrunc status=none

cp "$WORKDIR/black_bg.jpg" /data/black_bg.jpg

if [ ! -f "$CONTINUE_SH" ] || ! grep -qF "$HOOK_MARKER" "$CONTINUE_SH"; then
  TMP_CONTINUE="$(mktemp)"
  {
    echo "#!/usr/bin/env bash"
    echo "$HOOK_MARKER"
    echo "sudo mount -o remount,rw / 2>/dev/null"
    echo "sudo cp /data/black_bg.jpg /usr/comma/bg.jpg 2>/dev/null"
    echo "sudo mount -o remount,ro / 2>/dev/null"
    if [ -f "$CONTINUE_SH" ]; then
      tail -n +2 "$CONTINUE_SH"
    else
      echo "cd /data/openpilot"
      echo "exec ./launch_openpilot.sh"
    fi
  } > "$TMP_CONTINUE"
  mv "$TMP_CONTINUE" "$CONTINUE_SH"
  chmod +x "$CONTINUE_SH"
fi

echo "done"
