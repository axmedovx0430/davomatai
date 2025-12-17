#!/bin/bash
set -e

# Try to create swap if possible (might fail without privileges, but worth a try)
# This is a common workaround for low-memory environments
if [ ! -f /swapfile ]; then
    echo "Attempting to allocate swap..."
    fallocate -l 512M /swapfile || dd if=/dev/zero of=/swapfile bs=1M count=512
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile || echo "Failed to enable swap (likely due to permissions), continuing without it..."
else
    echo "Swap file already exists."
fi

# Run the application
exec "$@"
