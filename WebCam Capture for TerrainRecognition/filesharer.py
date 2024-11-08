from filestack import Client
class FileSharer():
    def __init__(self, filepath: str, api_key= 'AdG9aDa0nS0mZnP8S3sFwz'):
        self.filepath = filepath
        self.api_key = api_key

    def upload(self):
        client = Client(apikey= self.api_key)
        file_link = client.upload(filepath= self.filepath)
        return file_link.url
