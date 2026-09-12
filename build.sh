#!/usr/bin/env bash
# Assemble the deployable tree: the images directory plus its headers.
#
# images/ holds index.html, murica.bmp (the current image, overwritten each
# run) and the timestamped archive. It is copied rather than served in place
# so the generated _headers and .build-id do not land in the source tree.

set -euo pipefail

[ -d images ] || { echo "no images/ directory" >&2; exit 1; }

rm -rf dist
mkdir -p dist
cp -R images/. dist/

install -m 0644 _headers dist/_headers

# Identifies the deployed commit so the fallback workflow can tell whether
# Cloudflare already published this tree.
printf '%s\n' "${WORKERS_CI_COMMIT_SHA:-${GITHUB_SHA:-local}}" > dist/.build-id

echo "staged $(find dist -type f | wc -l | tr -d ' ') files into dist/"
