#!/bin/bash
cloudinit_version=${1:-0.7.8}
mkdir -p vendor/cloud-init
git init vendor/cloud-init
cd vendor/cloud-init
git remote add origin https://git.launchpad.net/cloud-init
git fetch --depth=1 origin $cloudinit_version
git checkout FETCH_HEAD
