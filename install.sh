#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "usage: $0 <device-host-or-ip> [ssh-user]"
  exit 1
fi

HOST="$1"
USER_="${2:-comma}"
TARGET="$USER_@$HOST"
REMOTE_DIR="/data/.branding"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

ssh "$TARGET" "mkdir -p $REMOTE_DIR"
scp -q "$DIR/scripts/build_splash.py" "$TARGET:$REMOTE_DIR/build_splash.py"
scp -q "$DIR/scripts/apply_on_device.sh" "$TARGET:$REMOTE_DIR/apply_on_device.sh"
scp -q "$DIR/assets/nmk_logo.png" "$TARGET:$REMOTE_DIR/nmk_logo.png"
scp -q "$DIR/assets/black_bg.jpg" "$TARGET:$REMOTE_DIR/black_bg.jpg"

ssh "$TARGET" "chmod +x $REMOTE_DIR/apply_on_device.sh && $REMOTE_DIR/apply_on_device.sh"

echo "branding applied on $HOST — reboot the device to see the new boot screen"
