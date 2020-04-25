import requests
import random
import secrets
import json
from dotenv import load_dotenv
import os


env_data = load_dotenv(dotenv_path='../../config/bot_env')
number_of_users = int(os.environ['number_of_users'])
max_posts_per_user = int(os.environ['max_posts_per_user'])
max_likes_per_user = int(os.environ['max_likes_per_user'])
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
host = os.environ['host']
users = []
posts = []
signup_endpoint = '/api/auth/users/'
token_endpoint = '/api/auth/jwt/create/'
create_post_endpoint = '/api/posts/create/'
like_endpoint = '/api/like_post/'


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
    if sign_up_response.status_code != 201:
        raise Exception('Something went wrong during sign up')
    auth_token_response = requests.post(f'{host}{token_endpoint}', data={'username': username, 'password': password})
    if auth_token_response.status_code != 200:
        raise Exception('Something went wrong while receiving a token')
    auth_data = json.loads(auth_token_response.text)
    access_token = auth_data['access']
    access_token_header = {'Authorization': f'Bearer {access_token}'}
    users.append(access_token_header)
    post_count = random.randint(1, max_posts_per_user)
    for j in range(post_count):
        theme = post_themes[random.randint(0, len(post_themes) - 1)]
        create_post_response = requests.post(f'{host}{create_post_endpoint}',
                                             headers=access_token_header, data={'theme': theme})
        if create_post_response.status_code != 201:
            raise Exception('Something went wrong during sign up')
        post_id = json.loads(create_post_response.text)['post_id']
        posts.append(post_id)
for user in users:
    like_count = random.randint(1, max_likes_per_user)
    if like_count > len(posts):
        like_count = len(posts)
    random.shuffle(posts)
    for i in range(like_count):
        like_post_response = requests.post(f'{host}{like_endpoint}',
                                             headers=user, data={'post_id': posts[i]})
        if like_post_response.status_code != 201:
            raise Exception('Something went wrong during sign up')
print('Bot job ended successfully!')

