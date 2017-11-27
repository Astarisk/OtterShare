import requests
import base64
import win32clipboard
from io import BytesIO

url = "https://api.imgur.com/3/image"


def upload_img(img, client_id):
    buffered = BytesIO()
    img.save(buffered, format="png")

    headers = {'authorization': 'Client-ID ' + client_id}
    data = {'image': base64.b64encode(buffered.getvalue()),
            'type:': 'base64'
            }

    response = requests.post(url, headers=headers, data=data)
    # TODO: Add in error checking based upon response code
    # <Response [200]>
    js = response.json()
    # TODO: Save link + delete hash to a file.
    save_to_clipboard(js['data']['link'])


def save_to_clipboard(url):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(url)
    win32clipboard.CloseClipboard()



