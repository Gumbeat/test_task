import string

import requests
import random
import secrets
import json

with open("../../config/bot_env", "r") as read_conf:
    line1, line2, line3 = read_conf.read().split('\n')
    number_of_users = int(line1.split('=')[1])
    max_posts_per_user = int(line2.split('=')[1])
    max_likes_per_user = int(line3.split('=')[1])
    prob_max_posts = number_of_users * max_posts_per_user
    if max_likes_per_user > prob_max_posts:
        max_likes_per_user = prob_max_posts
        print(f'Max likes per user were too high. Its new value is {prob_max_posts}')


post_themes = [
    'Art',
    'Music',
    'Food',
    'Sport',
    'Politics',
    'IT',
    'Travelling',
]
host = 'http://localhost:8000'
users = []
posts = []
signup_endpoint = '/api/auth/users/'
token_endpoint = '/api/auth/jwt/create/'
create_post_endpoint = '/api/posts/create/'
like_endpoint = '/api/like_post/'


def generate_random_string(n):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(n))


def generate_username_and_password():
    username = f'User_{secrets.token_hex(10)}'
    password = secrets.token_hex(8)
    return username, password


for i in range(number_of_users):
    username, password = generate_username_and_password()
    sign_up_response = requests.post(f'{host}{signup_endpoint}', data={'username': username, 'password': password})
    while sign_up_response.status_code == 400 and sign_up_response.text == \
            '{"username":["A user with that username already exists."]}':
        username, password = generate_username_and_password()
        sign_up_response = requests.post(f'{host}{signup_endpoint}', data={'username': username, 'password': password})
    if not sign_up_response.status_code == 201:
        raise Exception('Something went wrong during sign up')
    auth_token_response = requests.post(f'{host}{token_endpoint}', data={'username': username, 'password': password})
    if auth_token_response.status_code == 200:
        auth_data = json.loads(auth_token_response.text)
        access_token = auth_data['access']
        access_token_header = {'Authorization': f'Bearer {access_token}'}
        users.append(access_token_header)
    else:
        raise Exception('Something went wrong while receiving a token')
    post_count = random.randint(1, max_posts_per_user)
    for j in range(post_count):
        theme = post_themes[random.randint(0, len(post_themes) - 1)]
        create_post_response = requests.post(f'{host}{create_post_endpoint}',
                                             headers=access_token_header, data={'theme': theme})
        if not create_post_response.status_code == 201:
            raise Exception('Something went wrong during sign up')
        post_id = json.loads(create_post_response.text)['post_id']
        posts.append(post_id)
for user in users:
    like_count = random.randint(1, max_likes_per_user)
    random.shuffle(posts)
    for i in range(like_count):
        like_post_response = requests.post(f'{host}{like_endpoint}',
                                             headers=user, data={'post_id': posts[i]})
        if not like_post_response.status_code == 201:
            raise Exception('Something went wrong during sign up')
print('Bot job ended successfully!')

# 1. signup users (number provided in config)
# 2. each user creates random number of posts with any content (up to
# max_posts_per_user)
# 3. After creating the signup and posting activity, posts should be liked randomly, posts
# can be liked multiple times
#

