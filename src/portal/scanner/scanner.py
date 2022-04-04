"""
Communication with the scanner
"""

from pathlib import Path
from re import S
from typing import Union, Dict, List, Tuple
import enum
import time

import serial
from tqdm import tqdm
import numpy as np

from src.portal.biometrics.camera import create_probe
from src.portal.biometrics.template import compare

PRINTDEBUG = False

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
    time.sleep(3)
    ser.write(str.encode("start\n"))
    ser.flush()
    command, data = next_input(ser)
    if command != SerialCommand.STARTOK:
        raise ScannerInitError("Couldn't start communication with scanner")
    return ser


def send_result(ser: serial.Serial, auth_result: bool):
    """
    Send the authentication result back to the scanner.

    "auth yes" if the authentication was successful, "auth no" if not.
    :param ser: serial communication port
    :param auth_result: result of authentication
    """
    ser.write(str.encode(f'auth {"yes" if auth_result else "no"}\n'))


class SerialCommand(enum.Enum):
    TEMPLATE = enum.auto()
    STOP = enum.auto()
    PRINT = enum.auto()
    DEBUG = enum.auto()
    EMPTY = enum.auto()
    INFO = enum.auto()
    STARTOK = enum.auto()
    UNKNOWN = enum.auto()


def read_debug_message(ser: serial.Serial, message_size: int) -> str:
    print_message = ser.read(message_size).decode("utf-8")
    return print_message

def read_until(ser: serial.Serial, delim=" "):
    s = ""
    while True:
        byte_read = ser.read().decode("utf-8")
        if byte_read == delim:
            return s
        s = s + byte_read

def read_template(ser: serial.Serial, template_len: int) -> List[float]:
    template = [None] * template_len
    for i in tqdm(range(template_len)):
        try:
            template_float = read_until(ser,' ')
            template[i] = float(template_float)
        except TypeError:
            print("not a float")
        except Exception as e:
            print(e)
    return template


def read_info(ser: serial.Serial) -> Tuple[str, str, str]:
    fname = ser.readline().decode("utf-8").rstrip()
    lname = ser.readline().decode("utf-8").rstrip()
    dob = ser.readline().decode("utf-8").rstrip()

    return fname, lname, dob


def show_serial_debug(message: str):
    for l in message.split('\n'):
        print(f"serial debug:\t{l}")


def next_input(ser: serial.Serial) -> Tuple[SerialCommand, Union[Dict, None]]:
    while True:
        command_line = ser.readline().decode("utf-8")
        command, data = parse_serial_command(command_line, ser)
        if command == SerialCommand.PRINT:
            show_serial_debug(data['message'])
            continue
        if command == SerialCommand.DEBUG and PRINTDEBUG:
            show_serial_debug(data['message'])
            continue

        if command == SerialCommand.EMPTY:
            continue
        break

    return command, data


def parse_serial_command(command: str, ser: serial.Serial) -> Tuple[SerialCommand, Union[Dict, None]]:
    try:
        command, *command_args = command.split()
    except ValueError:
        return SerialCommand.EMPTY, None

    if command == 'print' or command == 'debug':
        read_bytes = int(command_args[0])
        print_lines = read_debug_message(ser, read_bytes)

        return SerialCommand.PRINT if command == "print" else SerialCommand.DEBUG, {"message": print_lines}
    elif command == 'template':
        template_len = int(command_args[0])
        template = read_template(ser, template_len)

        return SerialCommand.TEMPLATE, {"template": template}
    elif command == 'info':
        fname_len, lname_len, dob_len = int(command_args[0]), int(command_args[1]), int(command_args[1])
        fname, lname, dob = read_info(ser)

        if fname_len != len(fname) or lname_len != len(lname) or dob_len != len(dob):
            print(f'mismatch length')
            print(f'{fname_len=} {fname=}')
            print(f'{lname_len=} {lname=}')
            print(f'{dob_len=} {dob=}')

        return SerialCommand.INFO, {"fname": fname, "lname": lname, "dob": dob}
    elif command == 'ok':
        return SerialCommand.STARTOK, None
    elif command == 'stop':
        print("stop command")
        return SerialCommand.STOP, None

    return SerialCommand.UNKNOWN, None


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
