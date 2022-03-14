import argparse
import enum
from typing import Union, Dict, List, Tuple

import serial


class ScannerInitError(Exception):
    pass


class SerialCommand(enum.Enum):
    TEMPLATE = enum.auto()
    STOP = enum.auto()
    PRINT = enum.auto()
    EMPTY = enum.auto()
    UNKNOWN = enum.auto()


def read_debug_message(ser: serial.Serial, message_size: int) -> List[str]:
    print_message = ser.read(message_size).decode("utf-8")
    return print_message.split("\n")


def read_template(ser: serial.Serial, read_bytes: int, template_len: int):
    template_bytes = ser.read(read_bytes)

    return template_bytes


def parse_serial_command(command: str, ser: serial.Serial) -> Tuple[SerialCommand, Union[Dict, None]]:
    try:
        command, *command_args = command.split()
    except ValueError:
        print("Blank command")
        return SerialCommand.EMPTY, None

    if command == 'print':
        read_bytes = int(command_args[0])
        print_lines = read_debug_message(ser, read_bytes)

        return SerialCommand.PRINT, {"message": print_lines}
    elif command == 'template':
        read_bytes, template_len = int(command_args[0]), int(command_args[1])
        template = read_template(ser, read_bytes, template_len)

        return SerialCommand.TEMPLATE, {"template": template}
    elif command == 'stop':
        print("stop command")
        return SerialCommand.STOP, None

    return SerialCommand.UNKNOWN, None


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
    response = ser.readline().decode("utf-8")
    print(f"Response to start: {response}")

    response = str(response).strip()
    if response != "ok":
        raise ScannerInitError("Couldn't start communication with scanner")

    return ser


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--port", default='/tmp/ttyPy')
    args = arg_parser.parse_args()

    scanner_serial = init_scanner(args.port)

    while True:
        line = scanner_serial.readline().decode("utf-8")
        res = parse_serial_command(line, scanner_serial)
