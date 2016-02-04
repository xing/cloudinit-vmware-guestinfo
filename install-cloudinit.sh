#!/bin/bash
cloudinit_version=${CLOUDINIT_VERSION:-0.7.5}
mkdir -p vendor
bzr branch lp:cloud-init vendor/cloud-init -r $cloudinit_version
cd vendor/cloud-init
if [ -f requirements.txt ] ; then
  pip install -r requirements.txt
fi
