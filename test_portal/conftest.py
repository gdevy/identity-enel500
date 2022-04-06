import sys
from pathlib import Path
from time import sleep
import pty
import pytest

_is_mac = sys.platform == "darwin"
_mac_scanner_side = "/tmp/ttyCOM"
_mac_portal_side = "/tmp/ttyPy"


# @pytest.fixture(scope="session", autouse=True)
def start_port_pair(request):
    if _is_mac:
        import subprocess
        master, slave = pty.openpty()

        p = subprocess.Popen(
            ["socat", "-d", "-d", f"pty,raw,echo=0,link={_mac_portal_side}",
             f"pty,raw,echo=0,link={_mac_scanner_side}"],
            shell=True, stdin=subprocess.PIPE, stdout=slave, stderr=slave, close_fds=True)
        sleep(5)
        request.addfinalizer(p.kill)
    else:
        print("Remember to start the socket pair")


@pytest.fixture
def scanner_side_port():
    if _is_mac:
        return _mac_scanner_side
    elif sys.platform == "nt":
        return "COM10"


@pytest.fixture
def portal_side_port():
    if _is_mac:
        return _mac_portal_side
    elif sys.platform == "nt":
        return "COM11"


@pytest.fixture
def scanner_serial(scanner_side_port, ):
    import serial

    s = serial.Serial(port=scanner_side_port, baudrate=9600)
    yield s

    s.read_all()
    s.close()


@pytest.fixture
def portal_serial(portal_side_port, ):
    import serial

    s = serial.Serial(port=portal_side_port, baudrate=9600)
    yield s

    s.read_all()
    s.close()


@pytest.fixture
def sample_images():
    return (Path("") / "imgs").resolve()
