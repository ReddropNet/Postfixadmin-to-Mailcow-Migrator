#!/bin/bash
# migrate-maildir.sh
# Moves Maildir contents into a proper Maildir/ subfolder

BASE="/var/lib/docker/volumes/mailcowdockerized_vmail-vol-1/_data"
echo "Starting Maildir migration under $BASE..."

find "$BASE" -mindepth 2 -maxdepth 2 -type d | while read -r USERDIR; do
  # Check if this looks like a Maildir (has cur/new/tmp directly inside)
  if [ -d "$USERDIR/cur" ] && [ -d "$USERDIR/new" ] && [ -d "$USERDIR/tmp" ]; then
    echo "Migrating: $USERDIR"

    # Create target Maildir if it doesn't exist
    mkdir -p "$USERDIR/Maildir"

    # Move everything except the new Maildir folder into Maildir/
    shopt -s dotglob
    for item in "$USERDIR"/*; do
      [ "$(basename "$item")" = "Maildir" ] && continue
      mv "$item" "$USERDIR/Maildir/" || {
        echo "⚠️ Failed to move $item"
      }
    done
    shopt -u dotglob

    echo "✅ $USERDIR migrated"
  fi
done
chown -R 5000:5000 "$BASE"

