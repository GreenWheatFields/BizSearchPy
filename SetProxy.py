import requests
import Keys
from stem import Signal
from stem.control import Controller


def get_tor_session(count):
    global session
    session = requests.session()
    session.proxies = {'http': Keys.tor_proxy(),
                       'https': Keys.tor_proxy()}
    if count == 1:
        print("Connected to TOR proxy")
        print(session.get("http://httpbin.org/ip").text)
    return session


def renew_connection():
    print("getting new TOR connection")

    with Controller.from_port(port=Keys.tor_port()) as controller:
        controller.authenticate(password=Keys.tor_pass())
        controller.signal(Signal.NEWNYM)
        print("New TOR connection")
        print(session.get("http://httpbin.org/ip").text)
        # would like to log the location as well as the ip, or just create at log for data analysis
        # speeds request per minute etc.
        # time between switching, etc
