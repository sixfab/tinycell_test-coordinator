"""Module for detecting and connecting to serial ports."""

from serial.tools import list_ports
from .config import logger, device_list
from .device import Device

port_list = []
is_changed = False


def is_device_list_changed():
    """Returns if the device list is changed."""
    global is_changed
    if is_changed:
        is_changed = False
        return True
    return False


def has_micropython_bootloader(device):
    """Checks if the device has a micropython bootloader."""
    if device.vid == 11914 and device.pid == 5:
        return True
    return False


def get_serial_port_list():
    """Returns a list of serial ports of tinycell devices."""
    tinycell_ports = []
    all_ports = list_ports.comports()

    for port in all_ports:
        if has_micropython_bootloader(port):
            tinycell_ports.append(port)

    return tinycell_ports


def diagnose_ports():
    """Diagnose the serial ports."""
    ports = get_serial_port_list()
    for port in ports:
        print("Port: ", port.device)
        print("*************************")
        for var in vars(port):
            print(var, ":", getattr(port, var))
        print("*************************")
        print("\n")


def create_unique_name(device):
    """Creates a unique name for the device."""
    if device.serial_number is not None:
        return f"tinycell-{device.serial_number[-5:]}"
    return "tinycell-00000"


def update_device_list():
    """Updates the device list with the current serial ports."""
    global is_changed
    ports = get_serial_port_list()

    # Add new ports to the list
    for port in ports:
        if port not in port_list:
            port_list.append(port)
            logger.info("New device found: %s", port.device)
            device_name = create_unique_name(port)
            device_list.append(Device(device_name, port.device, True))
            is_changed = True

    remove_port_list = []
    # Detect ports that are no longer connected
    for port in port_list:
        if port not in ports:
            remove_port_list.append(port)
            logger.info("Device detached: %s", port.device)

    # Remove ports from the list after iteration ends
    for port in remove_port_list:
        port_list.remove(port)

        remove_device_list = []
        # Detect device no longer connected from device list
        for device in device_list:
            if device.port == port.device:
                remove_device_list.append(device)
                is_changed = True

        # Remove device from the list after iteration ends
        for device in remove_device_list:
            device_list.remove(device)

    return device_list
