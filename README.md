DataSourceVmwareGuestinfo  vmware guestinfo based provider for cloud-init
====================

[![Build Status](https://travis-ci.org/xing/cloudinit-vmware-guestinfo.svg?branch=master)](https://travis-ci.org/xing/cloudinit-vmware-guestinfo)

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

The guestinfo settings are buried deep in the vsphere api. They can be set using the `extraConfig` property of [vim.vm.ConfigSpec](https://pubs.vmware.com/vsphere-60/index.jsp?topic=%2Fcom.vmware.wssdk.apiref.doc%2Fvim.vm.ConfigSpec.html). Here is an actual example from our ruby code using rbvmomi:

```ruby
# Adds guestinfo entries
# @param [RbVmomi::VIM::VM] vm
# @param [Hash<String,Object>] guestinfo
def add_guestinfo(vm, guestinfo)
  extraConfig = guestinfo.map do |key, value|
    {key: "guestinfo.#{key}", value: value.to_s}
  end
  spec = RbVmomi::VIM.VirtualMachineConfigSpec(extraConfig: extraConfig)
  vm.ReconfigVM_Task('spec' => spec).wait_for_completion
end
```

Metadata
---------------

The guestinfo key `cloudinit.metadata` is interpreted as json and used as metadata.


Network config
---------------

Via network-interfaces
=========================

The most straight-forward way to configure a virtual machines network is to inject a properly formatted `/etc/network/interfaces` [man page](http://manpages.ubuntu.com/manpages/xenial/man5/interfaces.5.html). This works on all cloud-init versions.

To do so, add the content of the file to your metadata as `network-interfaces`. This for example sets eth0 to dhcp:

```json
{
  "network-interfaces":"auto lo eth0
iface lo inet loopback
iface eth0 inet dhcp"
}
```


Via cloudinit.net ( cloud-init > 0.7.7 )
=================================

Newer versions of cloud-init learned to write different network configs. The config is passed directly in the metadata json as `network-config`. Sadly the exact format is completely undocumented ( hint: `cloudinit/net/__init__.py` :( ).

Here is a documentation by example:

```json
{
  "network-config": {
    "version": 1,
    "config": [
      {
        "name":"lo",
        "type":"physical",
        "subnets":{
          "control":"auto",
          "type":"loopback"
        }
      },
      {
        "name":"eth0",
        "type":"physical",
        "subnets":{
          "control":"auto",
          "type":"static",
          "address":"1.2.3.4"
        }
      }
    ]
  }
}

```

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
