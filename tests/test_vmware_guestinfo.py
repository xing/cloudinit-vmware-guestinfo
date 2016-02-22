from DataSourceVmwareGuestinfo import DataSourceVmwareGuestinfo
from cloudinit import log

from sys import version_info
if version_info.major == 2:
    import __builtin__ as builtins
else:
    import builtins

from mock import mock_open, patch

if DataSourceVmwareGuestinfo.__init__.func_code.co_argcount == 5:
  # cloud-init 0.7.*
  def instance( conf ):
    return DataSourceVmwareGuestinfo( conf, None, {} )
else:
  # cloud-init 0.6.*
  def instance( conf ):
    return DataSourceVmwareGuestinfo( conf )

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
    with patch.object(builtins, 'open', mock_open(read_data='4221369B-38E5-A461-E1F9-5C5EBEC9A328')) as m:
        ds = instance(
                {'datasource':
                    {'VmwareGuestinfo':
                        {'path': ['./tests/fixtures/just_userdata'] }
                        }
                    }
                )
        assert ds.get_instance_id() == '4221369B-38E5-A461-E1F9-5C5EBEC9A328'
    m.assert_called_once_with('/sys/class/dmi/id/product_uuid', 'r')
