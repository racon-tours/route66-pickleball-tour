#!/bin/bash
# build-images.sh — Route 66 Pickleball Tour web image pipeline
#
# Reads source photography from the Drive-synced Route66 image library and
# emits width-stepped WebP derivatives into assets/img/.
#
# Usage:  ./tools/build-images.sh
# Requires: ImageMagick (brew install imagemagick)
#
# To add a photo: append a "SOURCE|slug" line to the MANIFEST block below and
# re-run. Existing derivatives are overwritten; nothing else is touched.

set -euo pipefail

LIB="/Users/ibmike/Library/CloudStorage/GoogleDrive-global.racon.tours@gmail.com/My Drive/02 - Business Units/03 - pickle.tours/Route66/Images"
DESK="/Users/ibmike/Desktop/N&Co/2 - pickle-tours/2-Marketing/Route66"
OUT="$(cd "$(dirname "$0")/.." && pwd)/assets/img"
WIDTHS=(400 800 1200 1800)
QUALITY=80

mkdir -p "$OUT"

MANIFEST=$(cat <<'EOF'
$DESK/picklebus-branded.png|coach-boarding
$LIB/Hotels/little_america_flagstaff/little_america_flagstaff_05_route66-sign-flagstaff-approach.jpg|route66-sign-flagstaff
EOF
)

# HELD — named-property photography. These are supplier-owned images for
# properties that are not yet under contract. Do not restore to the manifest
# until photo-use permission is granted in the signed agreement.
#   $LIB/PlayVenues/missouri_pickleball_club/missouri_pickleball_club_04_full-facility-interior.jpg|courts-missouri-pickleball-club
#   $LIB/Hotels/shangri_la_resort/shangri_la_resort_01_aerial-resort-and-sport-courts.jpg|resort-shangri-la-aerial
#   $LIB/Hotels/hotel_andaluz/hotel_andaluz_02_lobby-fountain-casbah.jpg|hotel-andaluz-lobby
#   $LIB/Hotels/la_quinta_resort_club/la_quinta_resort_club_04_guestroom-with-fireplace.jpg|la-quinta-guestroom

echo "Output: $OUT"
echo

while IFS='|' read -r src slug; do
  [ -z "$src" ] && continue
  src="${src/\$LIB/$LIB}"
  src="${src/\$DESK/$DESK}"

  if [ ! -f "$src" ]; then
    echo "MISSING  $slug  <- $src"
    continue
  fi

  srcw=$(magick identify -format "%w" "$src")
  printf '%-34s %spx wide ->' "$slug" "$srcw"

  for w in "${WIDTHS[@]}"; do
    [ "$w" -gt "$srcw" ] && continue
    magick "$src" \
      -auto-orient -strip \
      -resize "${w}x" \
      -quality "$QUALITY" \
      -define webp:method=6 \
      "$OUT/${slug}-${w}.webp"
    printf ' %s' "$w"
  done
  printf '\n'
done <<< "$MANIFEST"

echo
echo "--- assets/img ---"
ls -lh "$OUT" | awk 'NR>1{printf "%-44s %s\n", $9, $5}'
du -sh "$OUT"
