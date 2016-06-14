tumblr-export.py will dump all of the posts from a Tumblr blog into JSON files in a directory.

# Installation
```
pip3 install -r requirements.txt
```

# Usage
Set the following environment variables (or use a dotenv file):
```
TUMBLR_API_KEY=api key from api.tumblr.com
TUMBLR_BLOG_IDENTIFIER=example.tumblr.com
```
Then run:
```shell
python3 tumblr-export.py [OUTPUT_DIR]
```

If no OUTPUT_DIR is specified, JSON files will be created in the ```tumblr-posts``` directory.

# Output Format
One JSON file per post, in the specified output directory. Files are named ```<post number>.json```. Each file contains the JSON response from https://www.tumblr.com/docs/en/api/v2#posts.
