#!/usr/bin/env bash

# exit when any command fails
set -e

GITHUB_REPO_NAME="streetsidesoftware/vscode-spell-checker"

# The version to download, such as 4.10.0. Defaults to the latest release.
VERSION="$1"
if [ -n "$VERSION" ]; then
    RELEASE="tags/code-spell-checker-v${VERSION}"
else
    RELEASE="latest"
fi

# download the release
# more info here - https://gist.github.com/steinwaywhw/a4cd19cda655b8249d908261a62687f8

wget "$(curl -sf "https://api.github.com/repos/${GITHUB_REPO_NAME}/releases/${RELEASE}" | jq -r '.assets[0].browser_download_url')"

# clean up
rm -rf ./language-server-temp
rm -rf ./language-server
mkdir ./language-server

# unzip
unzip -a code-spell-checker-*.vsix -d ./language-server-temp

rm ./code-spell-checker-*.vsix

# ./language-server/package.json is required for lsp_utils to work. Reuse package.json from the extension folder.
jq '{name,version,private,type,dependencies}' ./language-server-temp/extension/package.json > ./language-server/package.json
cp -R ./language-server-temp/extension/packages/_server/dist ./language-server/_server

rm -rf ./language-server-temp

cd ./language-server
npm i --omit dev # to generate a ./language-server/package-lock.json file
rm -rf ./node_modules # to clean up after `npm install`, we only did it to generate the package-lock.json
cd ..

# clean up
rm -rf ./language-server-temp
echo "Done"
