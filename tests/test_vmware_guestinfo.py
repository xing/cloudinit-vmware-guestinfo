from DataSourceVmwareGuestinfo import DataSourceVmwareGuestinfo
from cloudinit import log

def test_nothing_set():
    ds = DataSourceVmwareGuestinfo(
            {'datasource':
                {'VmwareGuestinfo':
                    {'path': ['./tests/fixtures/nothing_set'] }
                    }
                }
            , None, {})
    assert ds.get_data() == False

def test_just_userdata():
    ds = DataSourceVmwareGuestinfo(
            {'datasource':
                {'VmwareGuestinfo':
                    {'path': ['./tests/fixtures/just_userdata'] }
                    }
                }
            , None, {})
    assert ds.get_data() == True
    assert ds.userdata_raw == "just userdata\n"
    assert ds.metadata == {}


def test_with_metadata():
    ds = DataSourceVmwareGuestinfo(
            {'datasource':
                {'VmwareGuestinfo':
                    {'path': ['./tests/fixtures/with_metadata'] }
                    }
                }
            , None, {})
    assert ds.get_data() == True
    assert ds.userdata_raw == "with metadata\n"
    assert ds.metadata == {'instance-id': "1234"}

def test_with_ovfEnv():
    ds = DataSourceVmwareGuestinfo(
            {'datasource':
                {'VmwareGuestinfo':
                    {'path': ['./tests/fixtures/with_ovfEnv'] }
                    }
                }
            , None, {})
    assert ds.get_data() == True
    assert ds.userdata_raw == "with ovfEnv\n"
    assert ds.metadata == {'instance-id': "5678", 'ip': '192.168.111.1'}

