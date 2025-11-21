# pc_client.py
# Real-time Brachiograph plot with joint angle labels, pen tip marker, page boundary, and full reset on 'r'

import socket
import time
import math
import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- CONFIG ---
PICO_IP = "192.168.4.1"
PORT = 8765
L1, L2 = 155.0, 155.0
INCH_TO_MM = 25.4
PLOT_WIDTH = 8.5 * INCH_TO_MM
PLOT_HEIGHT = 11 * INCH_TO_MM
PIVOT_X = -INCH_TO_MM
PIVOT_Y = PLOT_HEIGHT / 2
MAX_POINTS = 10000

# --- Globals ---
trace_x, trace_y = [], []
shoulder = elbow = 0.0
pen = 0
client_registered = False
last_keepalive = time.time()

# --- Socket ---
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(0.05)

def log(msg):
    print("[PC]", msg)

def send_hello():
    global client_registered
    try:
        sock.sendto(b"HELLO", (PICO_IP, PORT))
        log("HELLO sent")
    except:
        pass

def keepalive():
    global last_keepalive
    if time.time() - last_keepalive > 5 and client_registered:
        try:
            sock.sendto(b"KEEPALIVE", (PICO_IP, PORT))
        except:
            pass
        last_keepalive = time.time()

def receive_data():
    global shoulder, elbow, pen, client_registered
    try:
        data, addr = sock.recvfrom(1024)
        msg = data.decode().strip()
        if msg == "WELCOME":
            client_registered = True
            log(f"Registered with Pico: {addr}")
        elif msg.startswith("{"):
            d = json.loads(msg)
            shoulder = d.get("shoulder", 0)
            elbow = d.get("elbow", 0)
            pen = d.get("pen", 0)
    except:
        pass

# --- Kinematics ---
def forward_kinematics():
    x1 = PIVOT_X + L1 * math.cos(math.radians(shoulder))
    y1 = PIVOT_Y + L1 * math.sin(math.radians(shoulder))
    x2 = x1 + L2 * math.cos(math.radians(shoulder + elbow))
    y2 = y1 + L2 * math.sin(math.radians(shoulder + elbow))
    return x1, y1, x2, y2

def append_trace(x2, y2):
    if pen:
        trace_x.append(x2)
        trace_y.append(y2)
    else:
        trace_x.append(None)
        trace_y.append(None)
    if len(trace_x) > MAX_POINTS:
        trace_x.pop(0)
        trace_y.pop(0)

# --- Plot setup ---
def setup_plot():
    fig, ax = plt.subplots(figsize=(8,11))
    ax.set_xlim(-INCH_TO_MM*2, PLOT_WIDTH + INCH_TO_MM*2)
    ax.set_ylim(-INCH_TO_MM*2, PLOT_HEIGHT + INCH_TO_MM*2)
    ax.set_aspect('equal')
    ax.set_title("Brachiograph (press 'r' to reset)")

    # Arm and trace lines
    arm_line, = ax.plot([], [], 'g-', lw=2)
    trace_line, = ax.plot([], [], 'b-', lw=1)

    # Joint angle text labels
    shoulder_text = ax.text(PIVOT_X, PIVOT_Y, "", color='red', fontsize=10)
    elbow_text = ax.text(PIVOT_X, PIVOT_Y, "", color='blue', fontsize=10)

    # Pen tip marker (conditionally updated)
    pen_marker, = ax.plot([], [], 'ro', markersize=6)

    # Page boundary (8.5" x 11") dotted
    ax.plot([0, PLOT_WIDTH, PLOT_WIDTH, 0, 0],
            [0, 0, PLOT_HEIGHT, PLOT_HEIGHT, 0],
            'k:', lw=1)

    return fig, ax, arm_line, trace_line, shoulder_text, elbow_text, pen_marker

# --- Full reset ---
def reset_plot():
    global trace_x, trace_y
    trace_x = []
    trace_y = []
    arm_line.set_data([], [])
    trace_line.set_data([], [])
    shoulder_text.set_text("")
    elbow_text.set_text("")
    pen_marker.set_data([], [])
    log("Plot fully reset")

# --- Key press handling ---
def on_key(event):
    if event.key.lower() == 'r':
        reset_plot()

# --- Initialize plot ---
fig, ax, arm_line, trace_line, shoulder_text, elbow_text, pen_marker = setup_plot()
fig.canvas.mpl_connect('key_press_event', on_key)

# --- Animation update ---
def update(_):
    if not client_registered:
        send_hello()
    receive_data()

    x1, y1, x2, y2 = forward_kinematics()
    append_trace(x2, y2)

    # Update arm and trace
    arm_line.set_data([PIVOT_X, x1, x2], [PIVOT_Y, y1, y2])
    trace_line.set_data(trace_x, trace_y)

    # Update joint angle text
    shoulder_text.set_position((PIVOT_X, PIVOT_Y))
    shoulder_text.set_text(f"{shoulder:.1f}°")
    elbow_text.set_position((x1, y1))
    elbow_text.set_text(f"{elbow:.1f}°")

    # Update pen tip marker (show only if pen is down)
    if pen:
        pen_marker.set_data([x2], [y2])
    else:
        pen_marker.set_data([], [])

    keepalive()
    return arm_line, trace_line, shoulder_text, elbow_text, pen_marker

ani = FuncAnimation(fig, update, interval=50, blit=False)

# Immediately reset plot at start
reset_plot()

plt.show()
