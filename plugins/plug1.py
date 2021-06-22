import time

print("imported")


def start():
    print("LOL I STARTED THIS SICK")
    time.sleep(3)
    print("3 sec")


def getstartdata():
    return {
        "priority": 0.5,
        "type": "background",
        "startmethod": start
    }
