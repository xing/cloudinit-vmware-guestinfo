import unittest
from DataSourceVmwareGuestinfo import DataSourceVmwareGuestinfo
from cloudinit import log

from sys import version_info
if version_info.major == 2:
    import __builtin__ as builtins
else:
    import builtins

from mock import mock_open, patch, Mock

HAS_DISTRO=True
initfn=getattr(DataSourceVmwareGuestinfo.__init__,"func_code",DataSourceVmwareGuestinfo.__init__.__code__)
if initfn.co_argcount == 5:
  # cloud-init 0.7.*
  def instance( conf ):
    return DataSourceVmwareGuestinfo( conf, Mock(), {} )
else:
  # cloud-init 0.6.*
  HAS_DISTRO=False
  def instance( conf ):
    return DataSourceVmwareGuestinfo( conf )

HAS_NETWORK=False
try:
    from cloudinit import net
    HAS_NETWORK=True
except ImportError:
    pass

def test_nothing_set():
    ds = instance(
            {'datasource':
                {'VmwareGuestinfo':
                    {'path': ['./tests/fixtures/nothing_set'] }
                    }
                })
    assert ds.get_data() == False

def test_just_userdata():
    ds = instance(
            {'datasource':
                {'VmwareGuestinfo':
                    {'path': ['./tests/fixtures/just_userdata'] }
                    }
                }
            )
    assert ds.get_data() == True
    assert ds.userdata_raw == "just userdata\n"
    assert ds.metadata == {}


def test_with_metadata():
    ds = instance(
            {'datasource':
                {'VmwareGuestinfo':
                    {'path': ['./tests/fixtures/with_metadata'] }
                    }
                }
            )
    assert ds.get_data() == True
    assert ds.userdata_raw == "with metadata\n"
    assert ds.metadata == {'instance-id': "1234"}
    assert ds.get_instance_id() == '1234'

def test_with_ovfEnv():
    ds = instance(
            {'datasource':
                {'VmwareGuestinfo':
                    {'path': ['./tests/fixtures/with_ovfEnv'] }
                    }
                }
            )
    assert ds.get_data() == True
    assert ds.userdata_raw == "with ovfEnv\n"
    assert ds.metadata == {'instance-id': "5678", 'ip': '192.168.111.1'}

def test_instance_id_from_bios():
    with patch.object(builtins, 'open', mock_open(read_data="4221369B-38E5-A461-E1F9-5C5EBEC9A328\n")) as m:
        ds = instance(
                {'datasource':
                    {'VmwareGuestinfo':
                        {'path': ['./tests/fixtures/just_userdata'] }
                        }
                    }
                )
        assert ds.get_data() == True
        assert ds.get_instance_id() == '4221369B-38E5-A461-E1F9-5C5EBEC9A328'
    m.assert_called_once_with('/sys/class/dmi/id/product_uuid', 'r')

@unittest.skipIf(HAS_DISTRO,
                     "not used on cloudinit 0.7.*")
@patch('cloudinit.util.subp')
@patch('cloudinit.util.write_file')
def test_network_interfaces(write_file, subp):
    subp.return_value = ["",""]
    ds = instance(
            {'datasource':
                {'VmwareGuestinfo':
                    {'path': ['./tests/fixtures/with_network_interfaces'] }
                    }
                }
            )
    assert ds.get_data()
    subp.assert_called_once_with(["ifup","--all"])
    write_file.assert_called_once_with('/etc/network/interfaces',"auto lo\niface lo inet loopback")

@unittest.skipUnless(HAS_DISTRO,
                     "not used on cloudinit 0.6.*")
def test_network_interfaces():
    ds = instance(
            {'datasource':
                {'VmwareGuestinfo':
                    {'path': ['./tests/fixtures/with_network_interfaces'] }
                    }
                }
            )
    ds.distro.apply_network = Mock()
    assert ds.get_data()
    ds.distro.apply_network.assert_called_once_with("auto lo\niface lo inet loopback")

@unittest.skipUnless(HAS_NETWORK,
                     "no network support in cloudinit < 0.7.7")
@patch('cloudinit.util.subp')
@patch('cloudinit.util.write_file')
def test_network_config_parses_network_interfaces(write_file, subp):
    subp.return_value = ["",""]
    ds = instance(
            {'datasource':
                {'VmwareGuestinfo':
                    {'path': ['./tests/fixtures/with_network_interfaces'] }
                    }
                }
            )
    assert ds.get_data()
    print("%r" % ds.network_config)
    assert ds.network_config
    assert ds.network_config['version'] == 1
    assert ds.network_config['config'] == [{'name':'lo','subnets':[{'control':'auto','_orig_eni_name':'lo','type':'loopback'}], 'type':'physical'}]

@patch('cloudinit.util.subp')
@patch('cloudinit.util.write_file')
def test_network_config_wins_over_parsed_network_interfaces(write_file, subp):
    subp.return_value = ["",""]
    ds = instance(
            {'datasource':
                {'VmwareGuestinfo':
                    {'path': ['./tests/fixtures/with_network_config'] }
                    }
                }
            )
    assert ds.get_data()
    print("%r" % ds.network_config)
    assert ds.network_config
    assert ds.network_config['version'] == 1
    assert ds.network_config['config'] == [{'name':'eth1','subnets':[{'control':'auto','type':'dhcp'}], 'type':'physical'}]

@patch('cloudinit.util.subp')
@patch('cloudinit.util.write_file')
def test_network_interfaces_are_ignored_when_network_config_is_available(write_file, subp):
    subp.return_value = ["",""]
    ds = instance(
            {'datasource':
                {'VmwareGuestinfo':
                    {'path': ['./tests/fixtures/with_network_config'] }
                    }
                }
            )
    assert ds.get_data()
    if HAS_NETWORK:
        assert not ds.distro.apply_network.called
    else:
        ds.distro.apply_network.assert_called_once_with("auto lo\niface lo inet loopback")
