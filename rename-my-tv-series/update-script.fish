set -l URL 'https://www.tweaking4all.com/home-theatre/rename-my-tv-series-v2/'
set -l REGEX 'RenameMyTVSeries-([\\d.]+)-Linux64bit\\.tar\\.gz'

set -l VERSION $(../scripts/scrape_website $URL $REGEX 'a.btn-ok' 'href')

cp ./rename-my-tv-series.desktop ./rename-my-tv-series.desktop.bak

# @fish-lsp-disable-next-line 2001
set -l CAPTURED_VERSION $(sd 'Version:\\s+([\\d.]+)' '$1' ./rename-my-tv-series.spec.bak)

if test $CAPTURED_VERSION != $VERSION
  sd "Version:\\s+$CAPTURED_VERSION" "Version:\\s+$VERSION" ./rename-my-tv-series.spec
  rm ./rename-my-tv-series.desktop.bak
end
