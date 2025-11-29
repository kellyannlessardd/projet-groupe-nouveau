import network
import socket
import time
import ujson
import os
import random

from main.adc_reader import read_potentiometers, read_switch
from main.inverse_kinematics import cinematique_inverse
from main.Global_Variables import POS_X, POS_Y, LEN_E, LEN_B

# ---------- CONFIG ----------
PORT = 8765
DEBUG = True
FILENAME = "ssid.txt"

LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"
ALPHANUM = LETTERS + DIGITS

# ---------- GLOBALS ----------
client_addr = None
pen_state = 0
last_announce = 0

# Keep previous valid solution in case IK fails
prev_shoulder = 0.0
prev_elbow = 0.0


def log(msg):
    if DEBUG:
        t = time.localtime()
        print(f"[PICO][{t[3]:02d}:{t[4]:02d}:{t[5]:02d}] {msg}")


# ---------- SSID / PASSWORD ----------
def generate_SSID():
    """Prompt user for 3-letter prefix and generate SSID + random password"""
    while True:
        prefix = input("Enter 3-letter SSID prefix (A-Z or a-z only): ").strip()
        if len(prefix) == 3 and all(ch.isalpha() for ch in prefix):
            break
        print("Invalid input. Must be exactly 3 letters A-Z or a-z.")

    suffix = "{:05d}".format(random.randint(0, 99999))
    ssid = prefix + suffix
    password = "".join(random.choice(ALPHANUM) for _ in range(8))

    try:
        with open(FILENAME, "w") as f:
            f.write(f"{ssid}\n{password}\n")
        print(f"Created SSID: {ssid}, PASSWORD: {password}")
    except Exception as e:
        print(f"Error writing {FILENAME}: {e}")

    return ssid, password


def load_ssid_file():
    """Load SSID/password from file, or generate new if missing"""
    if FILENAME in os.listdir():
        try:
            with open(FILENAME, "r") as f:
                lines = [line.strip() for line in f if line.strip()]
                ssid = lines[0]
                password = lines[1] if len(lines) > 1 else generate_SSID()[1]
                log(f"Loaded SSID: {ssid}")
                return ssid, password
        except Exception as e:
            print(f"Error reading {FILENAME}: {e}")
            return generate_SSID()
    else:
        return generate_SSID()


# ---------- WIFI SETUP ----------
def setup_wifi(ssid, password):
    import network  # keep local to avoid issues if module missing in tests
    wlan = network.WLAN(network.AP_IF)
    wlan.active(True)
    wlan.config(essid=ssid, password=password)
    wlan.ifconfig(('192.168.4.1', '255.255.255.0', '192.168.4.1', '8.8.8.8'))
    log(f"WiFi AP active: SSID={ssid}, IP=192.168.4.1")
    return wlan


# ---------- NETWORK ----------
def setup_network():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("0.0.0.0", PORT))
    s.settimeout(0.05)
    log(f"UDP server listening on port {PORT}")
    return s


def handle_incoming_message(sock):
    """Register client and process KEEPALIVE"""
    global client_addr
    try:
        data, addr = sock.recvfrom(1024)
        msg = data.decode().strip()
        if msg == "HELLO":
            client_addr = addr
            sock.sendto(b"WELCOME", addr)
            log(f"Client {addr} registered")
        elif msg == "KEEPALIVE":
            client_addr = addr
    except OSError:
        # No data, ignore
        pass


def stream_current_arm_state(sock, shoulder, elbow):
    """Send joint positions to client"""
    global client_addr, last_announce, pen_state
    if client_addr is None:
        return

    payload = ujson.dumps({
        "shoulder": shoulder,
        "elbow": elbow,
        "pen": pen_state
    })

    try:
        sock.sendto(payload.encode(), client_addr)
    except OSError as e:
        log(f"Send failed: {e}")
        client_addr = None
        return

    now = time.ticks_ms()
    if time.ticks_diff(now, last_announce) > 1000:
        log(f"Streaming to {client_addr}: "
            f"S={shoulder:.1f}, E={elbow:.1f}, pen={pen_state}")
        last_announce = now


# ---------- MAIN ----------
SSID, PASSWORD = load_ssid_file()
wlan = setup_wifi(SSID, PASSWORD)
sock = setup_network()

while True:
    # 1) Handle HELLO / KEEPALIVE
    handle_incoming_message(sock)

    # 2) Read desired X,Y from the potentiometers (like in adc_reader.read_potentiometers)
    x, y = read_potentiometers()

    # 3) Pen state: use the same toggle logic as in your main program
    #    read_switch() returns True/False; convert to 1/0 for JSON.
    pen_state = 1 if read_switch() else 0

    # 4) Inverse kinematics: (x, y) -> (shoulder, elbow) angles
    try:
        shoulder, elbow = cinematique_inverse(POS_X, POS_Y, x, y, LEN_E, LEN_B)
        prev_shoulder, prev_elbow = shoulder, elbow
    except Exception as e:
        # If IK fails (point unreachable, rounding issue), keep previous angles
        log(f"IK error for x={x:.1f}, y={y:.1f}: {e}. Using previous angles.")
        shoulder, elbow = prev_shoulder, prev_elbow

    # 5) Stream the current arm state to the PC
    stream_current_arm_state(sock, shoulder, elbow)

    # 6) Small delay to limit frequency (~20 Hz)
    time.sleep(0.05)
