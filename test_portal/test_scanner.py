import pytest

from src.portal.scanner import scanner


def test_init_scanner_success(scanner_serial, portal_side_port):
    scanner_serial.write(b"ok\n")
    ser = scanner.init_scanner(port_name=portal_side_port, )

    assert scanner_serial.readline().decode("utf-8") == "start\n"

    ser.close()


def test_init_scanner_fail(scanner_serial, portal_side_port):
    scanner_serial.write(b"any\n")
    with pytest.raises(scanner.ScannerInitError):
        scanner.init_scanner(portal_side_port, )


def test_send_result(scanner_serial, portal_serial):
    scanner.send_result(portal_serial, True)

    r = scanner_serial.readline().decode("utf-8")
    assert r == "auth yes\n"


def test_read_debug_message(scanner_serial, portal_serial):
    msg = "debug message"
    scanner_serial.write(str.encode(msg))

    msg_return = scanner.read_debug_message(portal_serial, message_size=len(msg))

    assert msg == msg_return


def test_read_template(scanner_serial, portal_serial):
    sample_template = [
        1.2, 2.333, 5.01, -1.3
    ]

    template_string = " ".join(map(str, sample_template)) + " "
    scanner_serial.write(str.encode(template_string))
    scanner_serial.flush()

    template_return = scanner.read_template(portal_serial, len(sample_template))

    assert sample_template == template_return


def test_read_until(scanner_serial, portal_serial):
    msg = "hello there. how are you"
    words = msg.split()
    scanner_serial.write(str.encode(msg))

    for word in words[:-1]:
        word_return = scanner.read_until(portal_serial, " ")
        assert word == word_return

    last_word = portal_serial.read(len(words[-1])).decode("utf-8")
    assert words[-1] == last_word


@pytest.mark.parametrize(
    "command, command_str, expected_data, additional_data",
    [
        (scanner.SerialCommand.EMPTY, "", None, None),
        (scanner.SerialCommand.PRINT, "print 13", {"message": "print message"}, "print message"),
        (scanner.SerialCommand.DEBUG, "debug 13", {"message": "debug message"}, "debug message"),
    ]
)
def test_parse_serial_command_print(scanner_serial, portal_serial, command, command_str, expected_data,
                                    additional_data):
    if additional_data is not None:
        scanner_serial.write(str.encode(additional_data))

    command_return, data_return = scanner.parse_serial_command(command_str, portal_serial)

    assert command_return == command
    assert data_return == expected_data


@pytest.mark.parametrize(
    "command, command_str, expected_data, additional_data",
    [
        (scanner.SerialCommand.STOP, "stop", None, None),
        (scanner.SerialCommand.UNKNOWN, "garbage", None, None),
        (scanner.SerialCommand.INFO, "info 4 3", {"fname": "John", "lname": "Doe", "dob": "1/1/2000"},
         "John\nDoe\n1/1/2000\n"),
        (scanner.SerialCommand.TEMPLATE, "template 3", {"template": [1.3, 53.1, -10.2]}, "1.3 53.1 -10.2 "),
    ]
)
def test_next_input_serial(scanner_serial, portal_serial, command, command_str, expected_data, additional_data):
    scanner_serial.write(str.encode(command_str + "\n"))
    if additional_data is not None:
        scanner_serial.write(str.encode(additional_data))

    command_return, data_return = scanner.next_input(portal_serial, portal_serial)

    assert command_return == command
    assert data_return == expected_data


def test_next_input_print_debug_empty(scanner_serial, portal_serial):
    scanner_serial.write(b"print 5\nhello")
    scanner_serial.write(b"debug 5\ndebug")
    scanner_serial.write(b"\n")

    command, data = scanner.next_input(portal_serial, return_empty=True)

    assert command == scanner.SerialCommand.EMPTY
    assert data is None
