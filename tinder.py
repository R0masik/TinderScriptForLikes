"""Tinder like script"""

import requests
from robobrowser import RoboBrowser

tinder_api = 'api.gotinder.com'
host = f'https://{tinder_api}'


def run(login, password):
    def do_like(_id):
        resp = requests.get(f'{host}/like/{_id}', headers=headers)
        return resp.json()

    headers = {
        'Content-Type': 'application/json',
    }

    fb_tok = get_fb_token(login, password)
    fb_id = get_fb_id(fb_tok)
    tinder_tok = get_tinder_token(fb_tok, fb_id)

    headers['X-Auth-Token'] = tinder_tok

    likes_limit = False

    while not likes_limit:
        resp = requests.get(f'{host}/user/recs', headers=headers)
        if resp.status_code != 200:
            return resp.text

        girls_list = resp.json()['results']
        for girl in girls_list:
            print(girl)
            like = do_like(girl['_id'])
            print(like)
            if like['likes_remaining'] == 0:
                likes_limit = True
                break

    return 'Success'


def get_fb_token(login, password):
    fb_auth_url = 'https://www.facebook.com/v2.6/dialog/oauth?redirect_uri=fb464891386855067%3A%2F%2Fauthorize%2F&display=touch&state=%7B%22challenge%22%3A%22IUUkEUqIGud332lfu%252BMJhxL4Wlc%253D%22%2C%220_auth_logger_id%22%3A%2230F06532-A1B9-4B10-BB28-B29956C71AB1%22%2C%22com.facebook.sdk_client_state%22%3Atrue%2C%223_method%22%3A%22sfvc_auth%22%7D&scope=user_birthday%2Cuser_photos%2Cuser_education_history%2Cemail%2Cuser_relationship_details%2Cuser_friends%2Cuser_work_history%2Cuser_likes&response_type=token%2Csigned_request&default_audience=friends&return_scopes=true&auth_type=rerequest&client_id=464891386855067&ret=login&sdk=ios&logger_id=30F06532-A1B9-4B10-BB28-B29956C71AB1&ext=1470840777&hash=AeZqkIcf-NEW6vBd'
    s = RoboBrowser(parser="lxml")
    s.open(fb_auth_url)
    f = s.get_form()
    f["pass"] = password
    f["email"] = login
    s.submit_form(f)
    f = s.get_form()
    try:
        import re
        s.submit_form(f, submit=f.submit_fields['__CONFIRM__'])
        access_token = re.search(
            r"access_token=([\w\d]+)", s.response.content.decode()).groups()[0]
        return access_token
    except Exception as ex:
        print("access token could not be retrieved. Check your username and password.")
        print("Official error: %s" % ex)
        return {"error": "access token could not be retrieved. Check your username and password."}


def get_fb_id(access_token):
    resp = requests.get(f'https://graph.facebook.com/me?access_token={access_token}')
    return resp.json()['id']


def get_tinder_token(fb_token, fb_id):
    payload = {
        'facebook_token': fb_token,
        'facebook_id': fb_id
    }
    resp = requests.post(f'{host}/auth', data=payload)
    return resp.json()['token']


if __name__ == '__main__':
    # log and pass for facebook
    print(run(login, password))
