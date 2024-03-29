

from pystubit.nw import CreateWLAN
import umail
import urequests
import time
import sys
import json
import socket
import io
import machine

import _thread

def __nwled_on():
    nwpin = machine.Pin(12, machine.Pin.OUT)
    nwpin.value(1)


def __nwled_off():
    nwpin = machine.Pin(12, machine.Pin.OUT)
    nwpin.value(0)


req_th_exit = False
th_alive = False
def __blink():
    global th_alive
    th_alive = True
    is_on = False
    while not req_th_exit:
        if is_on:
            __nwled_off()
        else:
            __nwled_on()
        is_on = not is_on
        time.sleep(0.5)
    th_alive = False
    _thread.exit()


"""
WIFI
"""
wifi_sta = None
wifi_ap = None
wifi_info = {"ssid": "", "pwd": ""}
# WiFi configuration
def wifi_config(ssid, pwd):
    global wifi_info
    wifi_info["ssid"] = ssid
    wifi_info["pwd"] = pwd


# WiFi connection
def wifi_connect(ssid=None, pwd=None, trytime=None):
    global wifi_sta, wifi_info, req_th_exit

    req_th_exit = False
    _thread.start_new_thread(__blink, ())

    _ssid = ssid if ssid is not None else wifi_info["ssid"]
    _pwd = pwd if pwd is not None else wifi_info["pwd"]
    _trytime = trytime if trytime is not None else 1

    # Connect to WiFi router
    wifi_sta = CreateWLAN()
    wifi_sta.active(True)
    count = 0
    while _trytime > count:
        if not wifi_sta.connect(_ssid, _pwd):
            count += 1
        else:
            break

    if count < _trytime:
        req_th_exit = True
        while th_alive:
            print('wait...')
            time.sleep(1)

        __nwled_on()
        return True
    else:
        req_th_exit = True
        while th_alive:
            print('wait...')
            time.sleep(1)

        wifi_sta.active(False)
        __nwled_off()
        raise RuntimeError('It executed up to number of trials.')

    req_th_exit = True
    while th_alive:
        print('wait...')
        time.sleep(1)

    __nwled_on()
    return True


# WiFi disconnection
def wifi_disconnect():
    global wifi_sta
    if wifi_sta is not None:
        wifi_sta.disconnect()
        wifi_sta.active(False)
    __nwled_off()


def wifi_ifconfig(ip_info=None):
    global wifi_sta, wifi_ap
    if wifi_sta is not None:
        if (ip_info is not None):
            return wifi_sta.ifconfig(ip_info)
        else:
            return wifi_sta.ifconfig()
    if wifi_ap is not None:
        if (ip_info is not None):
            return wifi_ap.ifconfig(ip_info)
        else:
            return wifi_ap.ifconfig()


def wifi_start_ap(ssid=None, pwd=None):
    global wifi_ap, wifi_info

    _ssid = ssid if ssid is not None else wifi_info["ssid"]
    _pwd = pwd if pwd is not None else wifi_info["pwd"]

    wifi_ap = CreateWLAN(mode="AP")
    wifi_ap.active(True)
    wifi_ap.config(essid=_ssid, authmode=3, password=_pwd)
    __nwled_on()


def wifi_stop_ap():
    if wifi_ap is not None:
        wifi_ap.active(False)
    __nwled_off()


"""
Send Mail
"""
smtp_info = {
    "host": "smtp.gmail.com",
    "port": 587,
    "ssl": False,
    "username": "",  # GMail login name
    "password": "",  # GMail login password
}
# SMTP configuration
def smtp_config(*, host=None, port=None, ssl=None, username=None, password=None):
    global smtp_info
    # curl.options(verbose=True)
    if host is not None:
        if type(host) != str:
            raise TypeError("host must be string")
        smtp_info["host"] = host
    if port is not None:
        if type(port) != int:
            raise TypeError("port must be integer")
        smtp_info["port"] = port
    if ssl is not None:
        if type(ssl) != bool:
            raise TypeError("ssl must be boolean")
        smtp_info["ssl"] = ssl
    if username is not None:
        if type(username) != str:
            raise TypeError("username must be string")
        smtp_info["username"] = username
    if password is not None:
        if type(password) != str:
            raise TypeError("password must be string")
        smtp_info["password"] = password


def sendmail(to, title, message):
    global smtp_info
    smtp = umail.SMTP(
        smtp_info["host"],
        smtp_info["port"],
        smtp_info["ssl"],
        smtp_info["username"],
        smtp_info["password"],
    )
    smtp.to(to)
    smtp.write("Content-Type: text/plain; charset=utf-8\n")
    smtp.write("From: " + smtp_info["username"] + "\n")
    smtp.write("To: " + to + "\n")
    smtp.write("Subject: " + title + "\n")
    smtp.write(message + "\n")
    smtp.send()
    smtp.quit()


"""
HTTP
"""


def get_request(url, param=None):
    if param != None:
        query = ""
        for k, v in param.items():
            query += k + "=" + str(v) + "&"
        query = query[:-1]
        res = urequests.get(url + "?" + query)
        return res.text
    else:
        res = urequests.get(url)
        return res.text


def post_request(url, payload=None):
    if payload != None:
        if type(payload) == dict:
            res = urequests.post(url, json=payload)
        else:
            res = urequests.post(url, data=payload)
        return res.text
    else:
        res = urequests.post(url)
        return res.text


