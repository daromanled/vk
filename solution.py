import json
import requests
from urllib.parse import urlencode, urlparse

AUTHORIZE_URL = 'https://oauth.vk.com/authorize'
VERSION = '5.62'
APP_ID = 5960781

auth_data = {
    'v' : VERSION,
    'client_id' : APP_ID,
    'display' : 'mobile',
    'response_type' : 'token',
}
print('?'.join((AUTHORIZE_URL, urlencode(auth_data))))
token_url = 'https://oauth.vk.com/blank.html#access_token=fb8573d151801d9b71461bd1d2ce6b72bdac5cc1f5d53c81a2554de22cee4d43abbc80d688a1dda7ca7f3&expires_in=86400&user_id=406304856'
o = urlparse(token_url)
fragments = dict((i.split('=') for i in o.fragment.split('&')))
access_token = fragments['access_token']

params = {'access_token': access_token,
          'v': VERSION,
        }

def get_friends(user_id):
    if user_id:
        params['user_id'] = user_id
    r = requests.get('https://api.vk.com/method/friends.get', params)
    return r.json()

def get_all():
    my_friends = {}
    list_of_users = get_friends('406304856')
    for id in  list_of_users['response']['items']:
        if 'response' in get_friends(id):
            my_friends.update({id : get_friends(id)['response']['items']})
    return my_friends

def write_to_file(my_friends):
    with open('list_friends.json', 'w') as file:
        json.dump(my_friends, file)

def result():
    write_to_file(get_all())
    with open('list_friends.json') as file:
        data = json.load(file)

    for friend_id in data.keys():
        for id, fr_list in data.items():
            if id!=friend_id:
                print('Common friends '+friend_id+' & '+id+':',(set(data[friend_id]) & set(fr_list)))

result()
