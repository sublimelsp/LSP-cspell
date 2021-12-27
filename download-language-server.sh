#!/usr/bin/env bash

GITHUB_REPO_NAME="streetsidesoftware/vscode-spell-checker"

# download the release
# more info here - https://gist.github.com/steinwaywhw/a4cd19cda655b8249d908261a62687f8

wget $(curl -s https://api.github.com/repos/${GITHUB_REPO_NAME}/releases/latest | grep 'browser_' | cut -d\" -f4)

# clean up
rm -rf ./language-server-temp
rm -rf ./language-server
mkdir ./language-server

# unzip
unzip -a "code-spell-checker.zip" -d ./language-server-temp

cd ./language-server-temp/build && unzip -a "code-spell-checker-*.vsix" -d ../
cd .. && rm -rf ./build
cd .. && rm ./code-spell-checker.zip

# ./language-server/package.json is required for lsp_utils to work. Reuse package.json from the extension folder.
cp ./language-server-temp/extension/package.json ./language-server
cp -R ./language-server-temp/extension/packages/ ./language-server/packages

# because the ./language-server is deleted each time we envoke this script
# we need to copy the ./resolve_module.js to the ./language-server again
cp ./resolve_module.js ./language-server

# ./language-server/package-lock.json is required. Without it an error will appear when when starting the plugin.
cd language-server && yarn && yarn build-production

# clean up
cd .. && rm -rf ./language-server-temp
echo "Done"
