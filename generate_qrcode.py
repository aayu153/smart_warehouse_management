import qrcode

def generate(data):
    return qrcode.make(data)

def scan(qrcode):
    pass