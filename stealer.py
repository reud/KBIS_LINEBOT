import os
from google_drive_downloader import GoogleDriveDownloader as gdd
import requests

URL = "https://docs.google.com/uc?export=download"


# https://stackoverflow.com/questions/38511444/python-download-files-from-google-drive-using-url
# お借りしました

def download_file_from_google_drive(id, destination):
    session = requests.Session()

    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)


if __name__ == "__main__":
    print(os.getenv('KBIS_TEST'))
    gdd.download_file_from_google_drive(file_id=os.getenv('KBIS_TEST'),
                                        dest_path='./mnists.txt')
