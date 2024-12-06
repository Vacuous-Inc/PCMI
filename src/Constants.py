import requests

def MainIP():
    #return requests.get("https://go.uvm.edu/pcmi",verify=False).url.split("/"[-2])
    return "127.0.0.1:5000"
def CameraIP():
    return requests.get("https://go.uvm.edu/pcmi-cam",verify=False).url
