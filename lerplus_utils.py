from .lerplus_config import API_URLBASE
from qgis.core import *
import json
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QInputDialog

latest_api_error = ''
import locale
locale.setlocale(locale.LC_ALL, 'da_DK')

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

def make_api_call(self, apifunction, data='', timeout=60):
    settings = QgsSettings()
    token = settings.value("lerplusdock/apitoken")
    # QMessageBox.information(self, 'Token', token)
    API_ENDPOINT = API_URLBASE + '/' + apifunction + '?apitoken=' + token
    if inDebugMode():
        if data != '':
            jsdata = json.dumps(data, sort_keys=True, indent=4)
            QMessageBox.information(self, 'Sending to API', jsdata)
    try:
        r = requests.post(url=API_ENDPOINT, data=data, timeout=timeout)
        #print(r.raise_for_status())
        #r.raise_for_status()
    except requests.exceptions.Timeout:
        QMessageBox.information(self, 'The request timed out','')
        print("The request timed out")
        return False
    except requests.exceptions.RequestException as e:
        QMessageBox.information(self, f"An error occurred: ", e)
        print(f"An error occurred: {e}")
        return False
    #r = requests.post(url=API_ENDPOINT, data=data)

    if not is_valid_json(r.text):
        QMessageBox.information(self, 'Invalid API-response', r.text)
        return False
    data = json.loads(r.text)
    #QMessageBox.information(self, 'ERROR! API-response', r.text)
    if data["status"] != 'ok':
        if inDebugMode():
            QMessageBox.information(self, 'ERROR! API-response', r.text)
        else:
            error = data["data"]["errortext"]
            QMessageBox.information(self, 'LER+ backend returnerede en fejl', error)
            #QMessageBox.information(self, 'Fejl', "Der skete en fejl ved kald af " + apifunction + ": \n" + error)
        return False
    if inDebugMode():
        QMessageBox.information(self, 'API-response', r.text)

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

