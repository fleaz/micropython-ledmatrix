import network
from config import WIFI_SSID, WIFI_PASS
from time import sleep

sta_if = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)
if ap_if.active():
    ap_if.active(False)
if not sta_if.isconnected():
    print("connecting to network...")
    sta_if.active(True)
    sta_if.connect(WIFI_SSID, WIFI_PASS)
    while not sta_if.isconnected():
        sleep(1)

print("Network configuration:", sta_if.ifconfig())
