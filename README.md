DataSourceVmwareGuestinfo  vmware guestinfo based provider for cloud-init
====================

Requirements
------------------

Ubuntu 12.04/14.04: Install package `cloud-init`.


Install
---------------

Copy `DataSourceVmareGuestinfo.py` to `/usr/lib/python2.7/dist-packages/cloudinit/`.
Edit `/etc/cloud/cloud.cfg.d/90_dpkg.cfg` to include `VmwareGuestinfo` in the list of providers.

Usage
----------------

Set the guestinfo key `cloudinit.userdata` to your raw userdata. Optionally set the key `cloudinit.metadata` to a json object containing the necessary metadata.
