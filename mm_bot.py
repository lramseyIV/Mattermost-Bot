import requests
import json

with open('mm_botconfig.json', 'r') as f:
    CONFIG = json.loads(f.read())

access_key = CONFIG["key"]
base_url =CONFIG["url"]
bot_id = CONFIG["bot_id"]
header = {'Authorization': f'Bearer {access_key}'}
recipients = CONFIG["usernames"]
URL='https://v2.jokeapi.dev/joke/Miscellaneous,Dark,Pun'

def make_request():
    try:
        res = requests.get(URL)
    except requests.HTTPError:
        exit()
    return res.json()

def extract_joke(result):
    if result['type'] == "twopart":
        setup = result['setup']
        delivery = result['delivery']
        joke_string = f'Setup: {setup}\n Delivery: {delivery}'
    else:
        joke_string = result['joke']
    return joke_string

def find_user (username):
    data = {
        "term": f"{username}"
    }
    r = requests.post(f'{base_url}/users/search', headers=header, json=data)
    return json.loads(r.text)[0]["id"]

def get_channel_id(user_id):
    data = [bot_id, user_id]
    r = requests.post(f'{base_url}/channels/direct', headers=header, json=data)
    return json.loads(r.text)["id"]

def send_messages(joke):
    for r in recipients:
        uid = find_user(r)
        chan_id = get_channel_id(uid)
        msg = {
            "channel_id": chan_id,
            "message": f"**JOKE OF THE DAY** \n ______________ \n {joke}"
        }
        requests.post(f'{base_url}/posts', headers=header, json=msg)

if __name__=="__main__":
    result = make_request()
    joke = extract_joke(result)
    send_messages(joke)
