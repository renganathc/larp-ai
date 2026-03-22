import serial

SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 115200

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)


def send_command(cmd: str):
    print(f"[MOTOR UART] Sending: {cmd}")
    ser.write((cmd + "\n").encode())



def forward():
    send_command("FORWARD")


def backward():
    send_command("BACKWARD")


def left():
    send_command("LEFT")


def right():
    send_command("RIGHT")



def turn_180():
    send_command("TURN_180")


def turn_360():
    send_command("TURN_360")