import requests
import json
import sys
import mwparserfromhell
import pathlib
import time

wiki = 'https://runescape.wiki/api.php'
index = wiki.replace('api.php', 'index.php')

s = None
def makesession():
    global s
    s = requests.Session()
    with pathlib.Path('~/bot_login.json').expanduser().open('r', encoding='utf-8') as f:
        d = json.load(f)
        s.headers.update(d['oauthheader'])

edittoken = ''
def login(username, password):
    global edittoken
    token_data = {
    'action': 'query',
    'meta': 'tokens',
    'type': 'login',
    'format': 'json'
    }
    login_data = { 
    'action'    :  'login',
    'lgname'    : username, 
    "lgpassword": password,
    'lgtoken': '',
    'format'    : 'json'
    }
    response = s.get(wiki, params = token_data)
    content = response.json()
    login_data['lgtoken'] = content['query']['tokens']['logintoken']
    response = s.post(wiki, data = login_data)
    content = response.json()
    print('Login: %s' % content['login']['result'])
    input('Enter to continue, ctrl-c to cancel')
    token_data['type'] = 'csrf'
    response = s.get(wiki, params = token_data)
    content = response.json()
    edittoken = content['query']['tokens']['csrftoken']

def getedittoken():
    global edittoken
    token_data = {
    'action': 'query',
    'meta': 'tokens',
    'type': 'csrf',
    'format': 'json'
    }
    response = s.get(wiki, params = token_data)
    content = response.json()
    edittoken = content['query']['tokens']['csrftoken']

#def relogin():
    #login(loginname, loginpwd)
makesession()
#loginname = input("Username: ")
#loginpwd = input("Password: ")
getedittoken() #relogin()
def get_text(page):
    page = page.replace(" ", "_")
    t = s.get(index, params={'action':'raw', 'title':page}, headers={'Authorization':''}).text
    if t.startswith('<!DOCTYPE html>'):
        return ''
    return t

def edit(page, text, summary=''):
    global edittoken
    data = {'action': 'edit',
    'title': page,
    'assert': 'user',
    'bot': 1,
    'minor': 1,
    'text': text,
    'summary': summary,
    'token': edittoken,
    'format':'json'
    }
    time.sleep(0.2)
    resp = s.post(wiki, data=data)
    if resp.json().get('error') is not None:
        if resp.json().get('error').get('code') in ['badtoken', 'assertuserfailed']:
            print('Error "'+resp.json().get('error').get('code')+'", relogging in and trying again')
            relogin()
            return edit(page, text, summary)
        else:
            raise InterruptedError('Failed to edit: %s: %s' % (resp.json().get('error').get('code'), resp.json().get('error').get('info')))
    return resp
