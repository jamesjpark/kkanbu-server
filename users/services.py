import base64
import configparser
import hashlib
import hmac
import time
import requests
from django_redis import get_redis_connection
from django.core.cache import cache



config = configparser.ConfigParser()
config.read('config.ini')

server_ip = config['server']['server_ip']
server_port = config['server']['server_port']
sms_url = config['sms']['sms_url']
sms_access_key = config['sms']['sms_access_key']
sms_secret_key = config['sms']['sms_secret_key']
sms_type = config['sms']['sms_type']
sms_from_countryCode = config['sms']['sms_from_countryCode']
sms_from_number = config['sms']['sms_from_number']
sms_uri = config['sms']['sms_uri']


class UserServices(object):


    def make_signature(self, access_key, secret_key, method, uri, timestmap):
        timestamp = str(int(time.time() * 1000))
        secret_key = bytes(secret_key, 'UTF-8')

        message = method + " " + uri + "\n" + timestamp + "\n" + access_key
        message = bytes(message, 'UTF-8')
        signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
        return signingKey

    def send_sms(self, phone_number, subject, message):
        #  URL
        url = sms_url 
        # access key
        access_key = sms_access_key 
        # secret key
        secret_key = sms_secret_key
        # uri
        timestamp = str(int(time.time() * 1000))
        uri = sms_uri
        body = {
           "type":sms_type,
           "contentType":"COMM",
           "countryCode":sms_from_countryCode,
           "from":sms_from_number,
           "content": message,
           "messages":[
              {
                  "to": phone_number,
                  "subject": subject,
                  "content": message
              }
            ]
           }

        key = self.make_signature(access_key, secret_key, 'POST', uri, timestamp)
        headers = {
          'Content-Type': 'application/json; charset=utf-8',
          'x-ncp-apigw-timestamp': timestamp,
          'x-ncp-iam-access-key': access_key,
          'x-ncp-apigw-signature-v2': key
        }   


        res = requests.post(url, json=body, headers=headers)
        print(res.json())
        return res.json()

    def save_cert_number(self, phone_number, cert_number):
        cert_number = cache.set(phone_number, cert_number)
        return cert_number

    def validate_cert_number(self, phone_number, cert_number):
        if phone_number is None or cert_number is None:
            return False
        if cert_number == cache.get(phone_number):
            return True
        return False

