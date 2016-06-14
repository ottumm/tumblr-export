import requests
import os
import dotenv
import sys
import json
import math

import pdb

class ApiError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

dotenv_file = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_file):
	dotenv.load_dotenv(dotenv_file)

API_KEY = os.environ['TUMBLR_API_KEY']
BLOG_IDENTIFIER = os.environ['TUMBLR_BLOG_IDENTIFIER']
REQUEST_RANGE = 20
OUTPUT_DIR = sys.argv[1] if len(sys.argv) > 1 else 'tumblr-posts'
if os.path.exists(OUTPUT_DIR):
	print('Error: output directory "{}" already exists.'.format(OUTPUT_DIR), file=sys.stderr)
	sys.exit(1)

def get_request(url):
	resp = requests.get(url)
	if resp.status_code != 200:
		raise ApiError('GET {} {}'.format(url, resp.status_code))

	return resp

def get_post_count():
	resp = get_request('https://api.tumblr.com/v2/blog/{}/posts?api_key={}'.format(BLOG_IDENTIFIER, API_KEY))
	json_resp = resp.json()['response']
	total_posts = json_resp['total_posts']
	print('{} posts'.format(total_posts), file=sys.stderr)
	return total_posts

def get_posts(offset):
	print('Getting posts {} to {}'.format(offset, offset + REQUEST_RANGE), file=sys.stderr)
	posts_url = 'https://api.tumblr.com/v2/blog/{}/posts?api_key={}&offset={}'.format(BLOG_IDENTIFIER, API_KEY, offset)
	resp = get_request(posts_url)
	json_resp = resp.json()['response']
	return json_resp['posts']

post_count = get_post_count()
offset = 0
posts = []
while offset < post_count:
	posts.extend(get_posts(offset))
	offset += REQUEST_RANGE

posts.reverse()

#pdb.set_trace()

os.makedirs(OUTPUT_DIR)

for idx, post in enumerate(posts):
	filename = '{}.json'.format(str(idx).zfill(math.ceil(math.log10(post_count))))
	path = os.path.join(OUTPUT_DIR, filename)
	with open(path, 'w') as text_file:
		print(json.dumps(post, indent=4), file=text_file)
