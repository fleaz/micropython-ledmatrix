import socket
from config import PORT, LED_COUNT
import network
import ure
import machine, neopixel


def setPixel(strip, data):
    # data = index:r,g,b
    index, rgb = data.split(":")
    r, g, b = rgb.split(",")
    strip[int(index)] = (int(g), int(r), int(b))


def clear(strip, count):
    for i in range(count):
        strip[i] = (0, 0, 0)
    strip.write()


def main():
    print("Setup socket...")
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    station = network.WLAN(network.STA_IF)
    ip = station.ifconfig()[0]
    s.bind((ip, PORT))

    print("Setup LED strip...")
    np = neopixel.NeoPixel(machine.Pin(4), LED_COUNT)
    clear(np, LED_COUNT)

    print("Waiting for data...")
    pattern = ure.compile("\d+:\d+,\d+,\d+")
    while True:
        data = s.recv(1024)
        lines = data.decode().split(";")
        for l in lines:
            if pattern.match(l):
                setPixel(np, l)
            elif l != "":
                print("Invalid data: {}".format(l))

        np.write()


if __name__ == "__main__":
    main()
