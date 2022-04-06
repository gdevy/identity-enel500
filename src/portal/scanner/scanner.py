"""
Communication with the scanner
"""

from typing import Union, Dict, List, Tuple
import enum
import time

import serial
from tqdm import tqdm

PRINTDEBUG = False


class ScannerInitError(Exception):
    pass


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
    for _ in range(3):
        command, data = next_input(ser, return_empty=True)
        if command == SerialCommand.STARTOK:
            return ser

        print(f"Trying to initiate communication with scanner. Expected ok but got {command}. Retrying")

    raise ScannerInitError(f"Couldn't start communication with scanner.")


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
    template = [0.0] * template_len
    for i in tqdm(range(template_len)):
        template_float = read_until(ser, ' ')
        template[i] = float(template_float)
    return template


def read_info(ser: serial.Serial) -> Tuple[str, str, str]:
    fname = ser.readline().decode("utf-8").rstrip()
    lname = ser.readline().decode("utf-8").rstrip()
    dob = ser.readline().decode("utf-8").rstrip()

    return fname, lname, dob


def show_serial_debug(message: str):
    for l in message.split('\n'):
        print(f"serial debug:\t{l}")


def next_input(ser: serial.Serial, return_empty=False) -> Tuple[SerialCommand, Union[Dict, None]]:
    while True:
        command_line = ser.readline().decode("utf-8")
        command, data = parse_serial_command(command_line, ser)
        if command == SerialCommand.PRINT:
            show_serial_debug(data['message'])
            continue
        if command == SerialCommand.DEBUG:
            if PRINTDEBUG:
                show_serial_debug(data['message'])
            continue

        if command == SerialCommand.EMPTY:
            if return_empty:
                return command, None
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
