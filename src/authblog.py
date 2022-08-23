import os
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())
from tumblpy import Tumblpy
from tumblpy.exceptions import TumblpyError
from datetime import datetime, timezone
from dateutil import tz
import json
from math import ceil

CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
CURRENT_MONTH = int(datetime.now().strftime('%m'))
CURRENT_YEAR = int(datetime.now().strftime('%Y'))
TZ = tz.gettz("EST")
parent_dir = os.path.dirname(os.path.abspath(__file__))
json_file = os.path.join(parent_dir, "../json", "tags.json")
TAGS = json.load(open(json_file, "r"))

class AuthBlog():
    def __init__(self, url):
        '''Class which stores the URL and authorization of a given blog.'''
        self.url = url
        oauth_token = os.getenv(f"{self.url.upper()}_OAUTH_TOKEN")
        oauth_token_secret = os.getenv(f"{self.url.upper()}_OAUTH_TOKEN_SECRET")
        self.t = Tumblpy(CONSUMER_KEY, CONSUMER_SECRET, oauth_token, oauth_token_secret)
        if self.url in TAGS:
            self.ic_tag = TAGS[self.url]["ic"]
        else:
            self.ic_tag = "ic"
    
    def follow(self, urls):
        '''Accepts a single string or a list of blog names to follow.'''
        following = self.get_following()
        if isinstance(urls,str):
            self.t.post('user/follow', params={"url": f"{urls}.tumblr.com"})
            return f"Followed {urls}."
        for url in urls:
            try:
                self.t.post('user/follow', params={"url": f"{url}.tumblr.com"})
            except TumblpyError:
                print(f"Could not follow {url}")
        return f"Followed up to {len(urls)} blogs."
    
    def last_response(self, post_id, partner=None):
        '''Returns the user and time of the last post in an RP thread.'''
        post = self.t.get("notes", blog_url=self.url, params={
            "id": int(post_id),
            "mode": "reblogs_with_tags"
        })
        for note in post["notes"]:
            reblogger = note["blog_name"]
            dt = datetime.fromtimestamp(note["timestamp"])
            if reblogger == partner:
                return f"Partner {partner} replied on {dt}"
            if partner == None and reblogger != self.url:
                return f"{reblogger} replied on {dt}"
            if reblogger == self.url:
                return f"You replied on {dt}"
        op = self.t.get("posts", blog_url=self.url, params={"id": post_id})
        dt = datetime.fromtimestamp(op["posts"][0]["timestamp"])
        return f"Original posted on {dt}"


    def activity(self, month=CURRENT_MONTH, year=CURRENT_YEAR, min_activity=2):
        '''Returns how many posts you've made with your listed IC tag within the month.'''
        if month == None: month = CURRENT_MONTH
        if year == None: year = CURRENT_YEAR
        if min_activity == None: min_activity = 2
        start_date = int(datetime(year,month,1,0,0,0, tzinfo=TZ).timestamp())
        end_date = int(datetime(year,month+1,1,0,0,0, tzinfo=TZ).timestamp())
        response = self.t.get("posts", blog_url=self.url, params={
            "before": end_date,
            "tag": self.ic_tag,
            "limit": 10
        })
        symbol = "❌"
        num_posts = 0
        active_date = None
        for post in response["posts"]:
            if post["timestamp"] < start_date:
                break
            num_posts = num_posts + 1
            if num_posts == min_activity:
                active_date = datetime.fromtimestamp(post["timestamp"]).strftime('%m.%d.%y')
        if num_posts >= min_activity:
            symbol = "✅"
        return(f"{symbol} {self.url} has made at least {num_posts} IC posts this month. Be sure to post within a month of {active_date}!")
    
    def get_blogs(self):
        info = self.t.post("user/info")
        blogs = [i["name"] for i in info['user']['blogs']]
        return blogs
    
    def get_following(self):
        following = self.t.get("user/following", params={"offset":0})
        total_blogs = following["total_blogs"]
        blogs = set()
        for i in range(ceil(total_blogs/20)):
            offset = i * 20
            batch = self.t.get("user/following", params={"offset":offset})
            batch = [i["name"] for i in batch["blogs"]]
            batch = set(batch)
            blogs.update(batch)
        print(len(blogs))
        return batch
    
    def replace_tag(self, old_tag, new_tag, append=False, blog_url=None):
        '''Finds every post with a specific tag, then replaces or appends with the new tag.'''
        if not blog_url:
            blog_url = self.url
        tagged_posts = self.t.get("posts", blog_url=blog_url, params={"tag": old_tag})
        num_posts = tagged_posts["total_posts"]
        for i in range(ceil(num_posts/20)):
            batch = self.t.get("posts", blog_url=blog_url, params={
                "tag": old_tag,
            })
            ids = [i["id"] for i in batch["posts"]]
            tags = [i["tags"] for i in batch["posts"]]
            for tag_list in tags:
                if append is False:
                    tag_list_lower = [tag.lower() for tag in tag_list]
                    idx = tag_list_lower.index(old_tag.lower())
                    tag_list[idx] = new_tag
                else:
                    tag_list.append(new_tag)
            for i in range(len(ids)):
                post_tags = ",".join(tags[i])
                self.t.post("post/edit", blog_url=blog_url, params={
                    "id": ids[i],
                    "tags": post_tags
                    })
    
    def get_tagged(self, tag_list, blog_url=None):
        '''Returns a list of IDs of posts that each have all the listed tags.'''
        if not blog_url:
            blog_url = self.url
        tagged_posts = self.t.get("posts", blog_url=blog_url, params={"tag": tag_list})
        num_posts = tagged_posts["total_posts"]
        print(num_posts)

