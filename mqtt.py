import socket
import netifaces as ni

def get_ip_address(interface):
    try:
        ni.ifaddresses(interface)
        ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
        return ip
    except Exception:
        return '127.0.0.1'