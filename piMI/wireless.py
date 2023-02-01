# Enable wireless support
from network import WLAN, STA_IF
# Enable wait timer
from time import sleep
# Get secrets
from secrets import SSID, PASS

# Connect to a wireless network


def connectWireless():
    # Set WLAN config
    wlan = WLAN(STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASS)

    # Check connection
    max_wait = 100
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        sleep(1)

    # If improper connection or never reached
    if wlan.status() != 3:
        raise RuntimeError('network connection failed')
    # Serial out the IP of the device TODO: Remove for final product
    else:
        status = wlan.ifconfig()
        # Return IP
        return status[0]
