from .lerplus_config import API_URLBASE
from qgis.core import *
import json
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QInputDialog


def is_valid_json(my_string):
    try:
        json.loads(my_string)
        return True
    except json.JSONDecodeError:
        return False


def inDebugMode():
    settings = QgsSettings()
    if settings.value("lerplusdock/debugmode") == "1":
        return True
    else:
        return False

def make_api_call(self, apifunction, data=''):
    settings = QgsSettings()
    token = settings.value("lerplusdock/apitoken")
    # QMessageBox.information(self, 'Token', token)
    API_ENDPOINT = API_URLBASE + '/' + apifunction + '?apitoken=' + token
    r = requests.post(url=API_ENDPOINT, data=data)
    response_text = r.text
    #QMessageBox.information(self, 'Invalid API-response', r.text)
    if not is_valid_json(response_text):
        QMessageBox.information(self, 'Invalid API-response', r.text)
        return False
    data = json.loads(response_text)
    if "error" in response_text.lower():
        if inDebugMode():
            QMessageBox.information(self, 'ERROR! API-response', response_text)
        else:
            error = data["data"]["errortext"]

            QMessageBox.information(self, 'Fejl', "Der skete en fejl ved kald af " + apifunction + ": \n" + error)
        return False
    if inDebugMode():
        QMessageBox.information(self, 'API-response', response_text)

    return data

def get_download_token(self, ssid):
    data = {
        'ssid': ssid
    }
    apiresponse = make_api_call(self, "getdownloadtoken", data)
    if apiresponse is False:
        return False
    token = apiresponse['data']['token']
    return token

