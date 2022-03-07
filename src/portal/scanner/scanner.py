import argparse
from pathlib import Path
from typing import Union, List

import serial
import numpy as np

from src.portal.biometrics.camera import create_probe
from src.portal.biometrics.template import compare


def get_template(ser: serial.Serial) -> np.array:
    template_input = ser.readline()

    print(f"template input: {template_input=})")

    template_command, size, length = str(template_input).split()
    print(f'{template_command=} {size=} {length=}')
    size, length = int(size), int(length)

    template_bytes = ser.read(size)
    template = [float(x) for x in str(template_bytes).split()]

    print(f"received template: {np.array(template)}")
    return np.array(template)


def init_scanner(port_name: str = 'COM5') -> Union[None, serial.Serial]:
    ser = serial.Serial(port_name, 9600, timeout=10)

    print(ser)

    ser.write(str.encode("start\n"))

    response = ser.readline()
    print(f"Response to start: {response}")

    response = str(response)
    if response != "ok":
        return None

    return ser


def send_result(ser: serial.Serial, auth_result: bool):
    response = "auth yes" if auth_result else "auth no"

    ser.write(f'{response}\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('usb_port', type=str, nargs='?',
                        help='USB port name')

    args = parser.parse_args()
    print("Starting portal")
    print(args)

    ser = init_scanner(args.usb_port)

    if ser is None:
        quit(1)

    while True:
        input_template = get_template(ser)

        probe_path = Path(".") / "probe.jpg"
        create_probe(probe_path)
        print(f"Wrote probe to {probe_path}")

        dist, auth = compare(input_template, probe_path)

        print(f"Result of auth: {auth}")

        send_result(ser, auth)
