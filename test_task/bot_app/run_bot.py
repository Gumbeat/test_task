import string

import requests
import random
import secrets
import json

with open("../../config/bot_env", "r") as read_conf:
    line1, line2, line3 = read_conf.read().split('\n')
    number_of_users = int(line1.split('=')[1])
    max_posts_per_user = int(line2.split('=')[1])
    max_likes_per_user = int(line3.split('=')[1])  # toDo: добавить проверку

host = 'http://localhost:8000'
users = []
signup_endpoint = '/api/auth/users/'
token_endpoint = '/api/auth/jwt/create/'
create_post_endpoint = '/api/posts/create/'


def generate_random_string(n):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(n))


def generate_username_and_password():
    username = f'User_{secrets.token_hex(10)}'
    password = secrets.token_hex(8)
    return username, password


for i in range(number_of_users):
    username, password = generate_username_and_password()
    sign_up_response = requests.post(f'{host}{signup_endpoint}', data={'username': username, 'password': password})
    while sign_up_response.status_code == 400 and sign_up_response.text == '{"username":["A user with that username already exists."]}':
        username, password = generate_username_and_password()
        sign_up_response = requests.post(f'{host}{signup_endpoint}', data={'username': username, 'password': password})
    if not sign_up_response.status_code == 201:
        raise Exception('Something went wrong during sign up')
    auth_token_response = requests.post(f'{host}{token_endpoint}', data={'username': username, 'password': password})
    if auth_token_response.status_code == 200:
        auth_data = json.loads(auth_token_response.text)
        access_token = auth_data['access']
        access_token_header = {'Authorization': f'Bearer {access_token}'}
    else:
        raise Exception('Something went wrong while receiving a token')
    post_count = random.randint(1, max_posts_per_user)
    for j in range(post_count):
        create_post_response = requests.post(f'{host}{create_post_endpoint}', headers=access_token_header)
        if not create_post_response.status_code == 201:
            raise Exception('Something went wrong during sign up')




#
# 1. signup users (number provided in config)
# 2. each user creates random number of posts with any content (up to
# max_posts_per_user)
# 3. After creating the signup and posting activity, posts should be liked randomly, posts
# can be liked multiple times
#
#
