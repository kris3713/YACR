set -l SCRIPT_DIR $(status dirname)

set -l URL 'https://www.tweaking4all.com/home-theatre/rename-my-tv-series-v2/'
set -l REGEX 'RenameMyTVSeries-([\\d.]+)-Linux64bit\\.tar\\.gz'

echo 'Executing the `scrape_website` script'
set -l VERSION $("$SCRIPT_DIR/../scripts/scrape_website" $URL $REGEX 'a.btn-ok' 'href')

echo 'Backing up `rename-my-tv-series.desktop` to `rename-my-tv-series.desktop.bak`'
cp "$SCRIPT_DIR/rename-my-tv-series.desktop" "$SCRIPT_DIR/rename-my-tv-series.desktop.bak"

# @fish-lsp-disable-next-line 2001
set -l CAPTURED_VERSION $(sd 'Version:\\s+([\\d.]+)' '$1' "$SCRIPT_DIR/rename-my-tv-series.desktop.bak")

# @fish-lsp-disable-next-line 2001
echo 'Comparing captured version ($CAPTURED_VERSION) with current version ($VERSION)'
echo "Captured version: $CAPTURED_VERSION"
echo "Current version: $VERSION"
if test "$CAPTURED_VERSION" != "$VERSION"
  sd "Version:\\s+$CAPTURED_VERSION" "Version:\\s+$VERSION" "$SCRIPT_DIR/rename-my-tv-series.desktop"
end

echo 'Removing `rename-my-tv-series.desktop.bak`'
rm "$SCRIPT_DIR/rename-my-tv-series.desktop.bak"
