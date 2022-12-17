import os
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())
from src.t_requester import TRequester
from datetime import datetime, timezone
from dateutil import tz
import json
from math import ceil
import time


class Blog():
    def __init__(self, blog_url):
        '''Class which stores the URL and authorization of a given blog.'''
        self.url = blog_url
        consumer_key = os.getenv("CONSUMER_KEY")
        consumer_secret = os.getenv("CONSUMER_SECRET")
        access_token = os.getenv(f"{self.url.upper()}_ACCESS_TOKEN")
        refresh_token = os.getenv(f"{self.url.upper()}_REFRESH_TOKEN")
        expires = (int(os.getenv(f"{self.url.upper()}_EXPIRES"))  if os.getenv(f"{self.url.upper()}_EXPIRES") is not None else 0)
        if access_token is None or refresh_token is None:
            raise Exception('You are missing a {USERNAME}_ACCESS_TOKEN or {USERNAME}_REFRESH_TOKEN for this blog in your .env file.')
        self.t = TRequester(consumer_key, consumer_secret, access_token, refresh_token, blog_url, expires=expires)
    
    def follow(self, urls):
        '''Accepts a single string or a list of blog names to follow.'''
        if isinstance(urls,str):
            self.t.post('/user/follow', params={"url": f"{urls}.tumblr.com"})
            return f"Followed {urls}."
        for url in urls:
            try:
                self.t.post('/user/follow', params={"url": f"{url}.tumblr.com"})
            except Exception as e:
                print(f"Could not follow {url} due to:\n{e}")
        return f"Followed up to {len(urls)} blogs."
    
    def unfollow(self, urls):
        '''Accepts a single string or a list of blog names to follow.'''
        if isinstance(urls,str):
            self.t.post('/user/unfollow', params={"url": f"{urls}.tumblr.com"})
            return f"Unfollowed {urls}."
        for url in urls:
            try:
                self.t.post('/user/unfollow', params={"url": f"{url}.tumblr.com"})
            except Exception as e:
                print(f"Could not unfollow {url} due to: \n{e}")
        return f"Unfollowed up to {len(urls)} blogs."
    
    def last_response(self, post_id, partner=None):
        '''Returns the user and time of the last post in an RP thread.'''
        post = self.t.get("/notes", blog_url=self.url, params={
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
        op = self.t.get("/posts", blog_url=self.url, params={"id": post_id})
        dt = datetime.fromtimestamp(op["posts"][0]["timestamp"])
        return f"Original posted on {dt}"

    def get_activity(
        self,
        month=None,
        year=None,
        min_activity=2,
        ic_tag=None,
        blog_url=None,
        time_zone='EST'
    ):
        '''Returns how many posts you've made with your listed IC tag within the month. Defaults to current month.'''
        if not blog_url: blog_url = self.url
        if not month: month = int(datetime.now().strftime('%m'))
        if not year: year = int(datetime.now().strftime('%Y'))
        if not min_activity: min_activity = 2

        month_next = (1 if month == 12 else month + 1)
        year_next = (year if month_next != 1 else year + 1)

        start_date = int(datetime(year,month,1,0,0,0, tzinfo=tz.gettz(time_zone)).timestamp())
        end_date = int(datetime(year_next,month_next,1,0,0,0, tzinfo=tz.gettz(time_zone)).timestamp())
        response = self.t.get("/posts", blog_url=self.url, params={
            "before": end_date,
            "tag": ic_tag,
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
        info = self.t.post("/user/info")
        blogs = [i["name"] for i in info['user']['blogs']]
        return blogs
    
    def get_following(self):
        following = self.t.get("/user/following", params={"offset":0})
        total_blogs = following["total_blogs"]
        blogs = set()
        for i in range(ceil(total_blogs/20)):
            offset = i * 20
            batch = self.t.get("/user/following", params={"offset":offset})
            batch = [i["name"] for i in batch["blogs"]]
            batch = set(batch)
            blogs.update(batch)
        print(len(blogs))
        return batch
    
    def replace_tag(self, old_tag, new_tag, append=False, blog_url=None):
        '''Finds every post with a specific tag, then replaces or appends with the new tag.'''
        if not blog_url: blog_url = self.url
        tagged_posts = self.t.get("/posts", blog_url=blog_url, params={"tag": old_tag})
        num_posts = tagged_posts["total_posts"]
        for i in range(ceil(num_posts/20)):
            batch = self.t.get("/posts", blog_url=blog_url, params={
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
                self.t.post("/post/edit", blog_url=blog_url, params={
                    "id": ids[i],
                    "tags": post_tags
                    })
    
    def append_tag(self, post_id, new_tag, blog_url=None):
        '''Appends a tag to a post with a given ID.'''
        if not blog_url: blog_url = self.url
        post = self.t.get("/posts", blog_url=blog_url, params={"id": post_id})
        id = post_id
        tags = post["posts"][0]["tags"]
        tags.append(new_tag)
        post_tags = ",".join(tags)
        self.t.post("/post/edit", blog_url=blog_url, params={
            "id": id,
            "tags": post_tags
            })

    def remove_tag(self, post_id, old_tag, blog_url=None):
        '''Removes tag from post with a given ID.'''
        if not blog_url: blog_url = self.url
        post = self.t.get("/posts", blog_url=blog_url, params={"id": post_id})
        id = post_id
        tags = post["posts"][0]["tags"]
        tags.remove(old_tag)
        post_tags = ",".join(tags)
        self.t.post("/post/edit", blog_url=blog_url, params={
            "id": id,
            "tags": post_tags
            })
    
    def get_tagged(self, tag_list, blog_url=None):
        '''Returns a set of IDs of posts that each have all the listed tags.'''
        if not blog_url: blog_url = self.url
        if isinstance(tag_list, str):
            tag_list = [tag_list]
        id_sets = []
        for tag in tag_list:
            tagged_posts = self.t.get("/posts", blog_url=blog_url, params={"tag": tag})
            num_posts = tagged_posts["total_posts"]
            ids = set()
            for i in range(0, num_posts, 20):
                batch = self.t.get("/posts", blog_url=blog_url, params={"tag": tag, "offset": i})
                ids.update([j["id"] for j in batch["posts"]])
            id_sets.append(ids)

        full_set = id_sets[0]
        for i in range(len(id_sets)-1):
            full_set = full_set.intersection(id_sets[i+1])
        return full_set
    
    def get_reblog_tags(self, post_id, blog_url=None):
        '''Returns a list of tags from the reblogs of posts.'''
        if not blog_url: blog_url = self.url
        tags = {}
        urls = {}
        op = self.t.get('/posts', blog_url=blog_url, params={'id': post_id})
        op_timestamp = op['posts'][0]['timestamp']
        time_marker = time.time()
        while time_marker > op_timestamp:
            notes = self.t.get('/notes', blog_url=blog_url, params={'id': post_id, 'before_timestamp': time_marker, 'mode': 'all'})
            for note in notes['notes']:
                if note['type'] == 'reblog':
                    n_url = note['blog_name']
                    n_id = note['post_id']
                    new = self.t.get('/posts', blog_url=n_url, params={'id': n_id})
                    n_tags = new['posts'][0]['tags']
                    if n_tags != []:
                        tags[n_id] = n_tags
                        urls[n_id] = n_url
                if note['timestamp'] < time_marker: time_marker = note['timestamp']
            if note['timestamp'] < (op_timestamp + 5): break # some leeway given to timestamp comparison as it sometimes doesn't perfectly match the listed OP timestamp
        return tags, urls
    
    def save_avatar(self, location='./avatar.jpg', blog_url=None, dims=64):
        if not blog_url: blog_url = self.url
        img = self.t.get('/avatar', blog_url=blog_url, extra_path_param=dims)
        with open(location, 'wb') as f:
            f.write(img)
