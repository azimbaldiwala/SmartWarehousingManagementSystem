import qrcode


SERVER_NAME = 'localhost:5050'

def generate(data):
    data_ = "{SERVER_NAME}/qrcode/" + data + "/"
    return qrcode.make(data_)
