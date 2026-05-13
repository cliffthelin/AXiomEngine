#!/usr/bin/env bash
# AXIOMENGINE QEMU MICROVM LAUNCHER (Phase 4)
# Used for high-security agent execution.

KERNEL="./vmlinux"
ROOTFS="./rootfs.ext4"

if [[ ! -f "$KERNEL" ]]; then
    echo "⚠️  Kernel not found. Please place 'vmlinux' in the root directory."
    echo "You can download a minimal kernel from: https://github.com/firecracker-microvm/firecracker/raw/main/resources/tests/vmlinux"
    exit 1
fi

if [[ ! -f "$ROOTFS" ]]; then
    echo "⚠️  RootFS not found. Please place 'rootfs.ext4' in the root directory."
    exit 1
fi

echo "🚀 Launching Agent MicroVM..."

qemu-system-x86_64 \
    -M microvm,x-option-roms=off,pit=off,pic=off,rtc=off \
    -enable-kvm -cpu host -m 512m -smp 2 \
    -kernel "$KERNEL" \
    -append "console=ttyS0 root=/dev/vda rw" \
    -drive file="$ROOTFS",format=raw,if=none,id=hd0 \
    -device virtio-blk-device,drive=hd0 \
    -netdev user,id=net0 -device virtio-net-device,netdev=net0 \
    -display none -serial stdio \
    -no-reboot
