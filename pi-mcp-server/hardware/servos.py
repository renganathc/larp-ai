import serial
import time

SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 115200

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)


def send_command(cmd: str):
    print(f"[SERVO UART] {cmd}")
    ser.write((cmd + "\n").encode())
    time.sleep(0.05)



def head_up():
    send_command("HEAD_UP")


def head_down():
    send_command("HEAD_DOWN")


def head_center():
    send_command("HEAD_CENTER")


def head_left():
    send_command("HEAD_LEFT")


def head_right():
    send_command("HEAD_RIGHT")




def nod_yes():
    send_command("NOD_YES")


def nod_no():
    send_command("NOD_NO")