"""
Communication with the scanner
"""

from pathlib import Path
from typing import Union

import serial
import numpy as np

from src.portal.biometrics.camera import create_probe
from src.portal.biometrics.template import compare


class ScannerInitError(Exception):
    pass


def get_template(ser: serial.Serial) -> np.array:
    """
    Reads template from scanner
    :param ser: serial communication port to scanner
    :return: template in array form
    """
    template_input = ser.readline()

    print(f"template input: {template_input=})")

    template_command, size, length = str(template_input).split()
    print(f'{template_command=} {size=} {length=}')
    size, length = int(size), int(length)

    template_bytes = ser.read(size)
    template = [float(x) for x in str(template_bytes).split()]

    print(f"received template: {np.array(template)}")
    return np.array(template)


def init_scanner(port_name: str = 'COM5', baud_rate: int = 9600) -> Union[None, serial.Serial]:
    """
    Open serial port, wait for start sequence to complete.
    :param port_name:
    :param baud_rate: baud rate used for serial communication
    :return:
    """
    ser = serial.Serial(port_name, baud_rate, timeout=10)

    print(ser)

    ser.write(str.encode("start\n"))
    ser.flush()
    response = ser.readline()
    print(f"Response to start: {response}")

    response = str(response).strip()
    if response != "ok":
        raise ScannerInitError("Couldn't start communication with scanner")

    return ser


def send_result(ser: serial.Serial, auth_result: bool):
    """
    Send the authentication result back to the scanner.

    "auth yes" if the authentication was successful, "auth no" if not.
    :param ser: serial communication port
    :param auth_result: result of authentication
    """
    response = "auth yes" if auth_result else "auth no"

    ser.write(f'{response}\n')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Interact with ')
    parser.add_argument('usb_port', type=str, nargs='?',
                        help='USB port name')

    args = parser.parse_args()
    print("Starting portal")
    print(args)

    scanner_ser = init_scanner(args.usb_port)

    while True:
        input_template = get_template(scanner_ser)

        probe_path = Path(".") / "probe.jpg"
        create_probe(probe_path)
        print(f"Wrote probe to {probe_path}")

        dist, auth = compare(input_template, probe_path)
        print(f"Result of auth: {auth}")

        send_result(scanner_ser, auth)
