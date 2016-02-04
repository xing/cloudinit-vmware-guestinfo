#!/bin/bash
cloudinit_version=${1:-0.7.5}
mkdir -p vendor
bzr branch lp:cloud-init vendor/cloud-init -r $cloudinit_version
cd vendor/cloud-init
