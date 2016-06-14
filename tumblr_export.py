import requests
import dotenv
from bs4 import BeautifulSoup

import os
import sys
import json
import math
import urllib

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
	print('Fetching posts {} to {}'.format(offset, offset + REQUEST_RANGE), file=sys.stderr)
	posts_url = 'https://api.tumblr.com/v2/blog/{}/posts?api_key={}&offset={}'.format(BLOG_IDENTIFIER, API_KEY, offset)
	resp = get_request(posts_url)
	json_resp = resp.json()['response']
	return json_resp['posts']

# Get all the posts.

post_count = get_post_count()
offset = 0
posts = []
while offset < post_count:
	posts.extend(get_posts(offset))
	offset += REQUEST_RANGE

posts.reverse()

# Dump the posts and images.

os.makedirs(OUTPUT_DIR)

for idx, post in enumerate(posts):
	post_dir = os.path.join(OUTPUT_DIR, str(idx).zfill(math.ceil(math.log10(post_count))))
	os.makedirs(post_dir)
	with open(os.path.join(post_dir, '{}.json'.format(post['slug'])), 'w') as text_file:
		print(json.dumps(post, indent=4), file=text_file)

	soup = BeautifulSoup(post['body'], 'html.parser')
	imgs = soup.find_all('img')
	for img in imgs:
		img_url = img['src']
		filename = os.path.basename(urllib.parse.urlparse(img_url).path)
		print('Post {}: fetching {}...'.format(idx, filename), file=sys.stderr)
		urllib.request.urlretrieve(img_url, os.path.join(post_dir, filename))
