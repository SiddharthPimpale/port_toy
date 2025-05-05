import pytest

from port_toy.utils import validate_port, clear_screen
from port_toy.port_scanner import scan_port, scan_by_process_name
from port_toy.process_manager import kill_process, kill_ports
from unittest.mock import patch
from types import SimpleNamespace

# Test for clear screen
def test_clear_screen_windows():
    with patch('os.system') as mock_system:
        with patch('platform.system', return_value='Windows'):
            clear_screen()
            mock_system.assert_called_once_with('cls')

def test_clear_screen_unix():
    with patch('os.system') as mock_system:
        with patch('platform.system', return_value='Linux'):
            clear_screen()
            mock_system.assert_called_once_with('clear')

# Test for `validate_port()`
def test_valid_ports():
    valid_ports = [0, 1, 65535]  # Lower and upper boundary ports
    for port in valid_ports:
        assert validate_port(port) == port

def test_invalid_port_non_integer():
    with pytest.raises(ValueError):
        validate_port("abc")  # Non-numeric input

def test_invalid_port_out_of_range():
    with pytest.raises(ValueError):
        validate_port(70000)  # Port outside valid range

def test_invalid_port_negative():
    with pytest.raises(ValueError):
        validate_port(-1)  # Negative port

# Test for `scan_port()`
@patch("port_toy.port_scanner.check_port")
@patch("port_toy.port_scanner.get_process_from_port")
@patch("builtins.input", return_value="8080")  # Mock input to provide port
def test_scan_port(mock_input, mock_get_process, mock_check_port):
    # Mock successful port scan with process found
    mock_check_port.return_value = True
    mock_get_process.return_value = (1234, "test_process")

    with patch("builtins.print") as mock_print:
        scan_port()  # Simulate scanning a valid port

    # Check if the expected prints were made
    mock_print.assert_any_call(f"[+] Port 8080 is OPEN.")
    mock_print.assert_any_call(f"    PID: 1234, Name: test_process")

# Test for `scan_by_process_name()`
@patch("psutil.net_connections")
def test_scan_by_process_name(mock_net_connections):
    # Mock laddr as an object with a 'port' attribute
    laddr1 = SimpleNamespace(ip="127.0.0.1", port=8080)
    laddr2 = SimpleNamespace(ip="127.0.0.1", port=9090)

    # Simulate mock network connections
    mock_net_connections.return_value = [
        SimpleNamespace(laddr=laddr1, pid=1234),
        SimpleNamespace(laddr=laddr2, pid=5678),
    ]

    # Mock psutil.Process to return process names
    with patch("psutil.Process") as mock_process:
        mock_process.return_value.name.return_value = "test_process"

        with patch("builtins.print") as mock_print:
            scan_by_process_name("test")
            mock_print.assert_any_call("[+] Port 8080 -- PID 1234 -- Name: test_process")
            mock_print.assert_any_call("[+] Port 9090 -- PID 5678 -- Name: test_process")


# Test for `kill_process()`
@patch("psutil.Process")
def test_kill_process(mock_process):
    # Simulate successful process termination
    mock_proc = mock_process.return_value
    mock_proc.terminate.return_value = None
    mock_proc.wait.return_value = None

    result = kill_process(1234)
    assert result is True

    # Simulate failure to terminate process
    mock_proc.terminate.side_effect = Exception("Error")
    result = kill_process(1234)
    assert result is False


# Test for `kill_ports()`
@patch("port_toy.process_manager.check_port")
@patch("port_toy.process_manager.get_process_from_port")
@patch("port_toy.process_manager.kill_process")
def test_kill_ports(mock_kill_process, mock_get_process, mock_check_port):
    # Simulate process found and ready for kill
    mock_check_port.return_value = True
    mock_get_process.return_value = (1234, "test_process")
    mock_kill_process.return_value = True

    # Simulate input: first the port number, then 'y' for confirmation
    with patch("builtins.input", side_effect=["8080", "y"]):
        with patch("builtins.print") as mock_print:
            kill_ports()
            mock_print.assert_any_call("✔ Killed process 1234")

    # Simulate failure to kill process
    mock_kill_process.return_value = False
    with patch("builtins.input", side_effect=["8080", "y"]):
        with patch("builtins.print") as mock_print:
            kill_ports()
            mock_print.assert_any_call("✘ Failed to kill process 1234")
