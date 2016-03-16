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

Metadata
---------------

The guestinfo key `cloudinit.metadata` is interpreted as json. If it contains a key `network-interfaces` it is written to `/etc/network/interfaces`.


Authors
------------------

Hannes Georg @hannesg42

License
-----------------

The MIT License (MIT)

Copyright (c) 2016 XING AG

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
