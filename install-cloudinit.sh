#!/bin/bash
cloudinit_version=${CLOUDINIT_VERSION:-0.7.5}
bzr branch lp:cloud-init vendor/cloud-init -r $cloudinit_version
