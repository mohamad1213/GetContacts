import requests
import os, sys
import bs4
import os
import time
import json
import urllib.request
import base64
import hmac
import hashlib
import binascii
import json
from bs4 import BeautifulSoup
from termcolor import colored
from Crypto import Random
from Crypto.Cipher import AES

def main_menu():
	os.system("clear")
	print(colored("Berlangganan di PHONE PARSER v1.1", 'green'))
	print(colored("Pengembang - CyberUSA", "red"))
	print("\n")
	print(colored("1 - Search AVITO", "yellow"))
	print(colored("Search AVITO", "yellow"))
	print("")
	print(colored("2 - Search GETCONTACT", 'yellow'))
	print(colored("Search GETCONTACT", "yellow"))
	print("")
	print(colored("3 - Search STANDART", 'yellow'))
	print(colored("Search standard data", "yellow"))
	print("")
	print(colored("4 - Search TELEGRAM", 'yellow'))
	print(colored("Search account TELEGRAM", "yellow"))
	print("")
	print('\n')
	
	action = input(colored("Choose a point Search: ", 'green'))
	if action == "1":
		os.system("clear")
		pars_avito()
	elif action == "2":
		os.system("clear")
		pars_getcontact()
	elif action == "3":
		os.system("clear")
		pars_simcard()
	elif action == "4":
		os.system("clear")
		pass
	elif action == "5":
		os.system("clear")
		pass
	else:
		os.system("clear")
		main_menu()
		
		
	
	
AES_KEY = 'faac7a03dbcb45fc4f016a5b02175c45535ee89e505d834bca11d9eadd6ce68e' 
TOKEN = 'NpMfb52bdd184e93dfe0759097d8f22e7bcffacdf7bbc5f92e5a0fc7679'

key = b'2Wq7)qkX~cp7)H|n_tc&o+:G_USN3/-uIi~>M+c ;Oq]E{t9)RC_5|lhAA_Qq%_4'


class AESCipher(object):

    def __init__(self, AES_KEY): 
        self.bs = AES.block_size
        self.AES_KEY = binascii.unhexlify(AES_KEY)

    def encrypt(self, raw):
        raw = self._pad(raw)
        cipher = AES.new(self.AES_KEY, AES.MODE_ECB)
        return base64.b64encode(cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.AES_KEY, AES.MODE_ECB)
        return self._unpad(cipher.decrypt(enc)).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]


aes = AESCipher(AES_KEY)

def sendPost(url, data, sig, ts):
    
    headers = {'X-App-Version': '4.9.1',
        'X-Token':TOKEN,
        'X-Os': 'android 5.0',
        'X-Client-Device-Id': '32F5D46E403F84E0',
        'Content-Type': 'application/json; charset=utf-8',
        'Accept-Encoding': 'deflate',
        'X-Req-Timestamp': ts,
        'X-Req-Signature': sig,
        'X-Encrypted': '1'}
    
    r = requests.post(url, data=data, headers=headers, verify=True)
    return json.loads(aes.decrypt(r.json()['data']))

def getByPhone(phone):
    
    ts = str(int(time.time()))
    
    req = f'"countryCode":"RU","source":"search","token":"{TOKEN}","phoneNumber":"{phone}"'
    req = '{'+req+'}'
    string = str(ts)+'-'+req
    
    sig = base64.b64encode(hmac.new(key, string.encode(), hashlib.sha256).digest()).decode()
    crypt_data = aes.encrypt(req)
    
    return sendPost('https://pbssrv-centralevents.com/v2.5/search',
                    b'{"data":"'+crypt_data+b'"}', sig, ts)

def getByPhoneTags(phone):
    
    ts = str(int(time.time()))
    
    req = f'"countryCode":"RU","source":"details","token":"{TOKEN}","phoneNumber":"{phone}"'
    req = '{'+req+'}'
    
    string = str(ts)+'-'+req
    sig = base64.b64encode(hmac.new(key, string.encode(), hashlib.sha256).digest()).decode()
    crypt_data = aes.encrypt(req)
    
    return sendPost('https://pbssrv-centralevents.com/v2.5/number-detail',
                    b'{"data":"'+crypt_data+b'"}', sig, ts)



##Получаем GETCONTACT
def pars_getcontact():
	
	phone = input(colored("enter your number: ", 'yellow'))
	
	if '+' not in phone:
		phone = '+'+phone
	
	print(colored('\n========GETCONTACT========', 'yellow'))
	finfo = getByPhone(phone)
	
	try:
		if finfo['result']['profile']['displayName']:
			print(colored(finfo['result']['profile']['displayName'], 'green'))
			print(colored('name detected: '+str(finfo['result']['profile']['tagCount']), 'yellow'))
			
			try:
				print('\n'.join([i['tag'] for i in getByPhoneTags(phone)['result']['tags']]))
			except KeyError:
				if finfo['result']['profile']['tagCount'] > 0:
					print('Name found, but premium required to view it')
					print('Telegram - @CyberUSA')
				else:
					pass
		else:
			print('Not found!')
	except:
		print('Not found!')


def pars_avito():
	
	phone = input(colored("enter your number: ", 'yellow'))
	os.system("clear")
	
	page = requests.get('https://mirror.bullshit.agency/search_by_phone/'+phone)
	soup = BeautifulSoup(page.text, 'html.parser')
	
	print(colored("========PARSER AVITO=======", 'yellow'))
	print("\n")
	
	#tag html search and class = name 
	classsell=soup.find(class_='media-heading')
	namesell= soup.find_all('h4')
	
	#for tag = name
	for classsell in namesell:
		print(colored("Advertisement name: ", 'green'), classsell.text)
	
	#tag html search and class = adresat
	classtext = soup.find(class_='text-muted')
	nametext = soup.find_all('span')
	
	#for tag = adresat
	for classtext in nametext:
		print(colored("Found address and date \n", 'green'), classtext.text)
		
def pars_simcard():
	phone = input(colored("enter your number: ", 'yellow'))
	try:
		getInfo = "https://htmlweb.ru/geo/api.php?json&telcod=" + str(phone)
		try:
			infoPhone = urllib.request.urlopen( getInfo )
		except:
			print( "\nPhone not found\n" )
		infoPhone = json.load( infoPhone )
		print( u"The country:", infoPhone["country"]["name"] )
		print( u"Region:", infoPhone["region"]["name"] )
		print( u"County:", infoPhone["region"]["okrug"] )
		print( u"Operator:", infoPhone["0"]["oper"] )
		print( u"locations:", infoPhone["country"]["location"] )
	except:
		print(colored("Not found!", "white"))
main_menu()
