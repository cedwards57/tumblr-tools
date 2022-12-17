# Tumblr Tools
A Python app for interacting with the Tumblr API.

## Getting Started

### Cloning the Repository
```
git clone https://github.com/thestarjar/tumblr-app
cd tumblr-app
pip install -r requirements.txt
```

### Setting Up with Tumblr
You'll need to [register an application with Tumblr](https://www.tumblr.com/oauth/apps). Then create a file in the root of your repository called `.env` and give it these contents:

```
export CONSUMER_KEY="your_key_here"
export CONSUMER_SECRET="your_secret_key_here"
```

Additionally, if you want to use this app locally out-of-box, you'll want to set your app's callback URL to `http://localhost:8080/callback`.

### Adding your Blogs
Now that you've set up, you can go about authorizing your specific blogs:

1. Log in to your tumblr account.
2. run `python addblog.py`
3. A link to a tumblr authentication screen should automatically open in your browser.
4. Click "Allow".
5. You're done! Your authorization keys have been logged, and you can read/write to blogs on that account. If you have multiple accounts, you can repeat these steps for each one to be authorized for all of them.

### Using This App
Run `python -m t -h` from the root directory to view available commands. Use `python -m t <command> -h` to view usage of a given command.


## Documentation
This code attempts to be as modular and accessible as possible, so you can add your own functions as desired.

- `src.t_requester.TAuthorizer`: Contains the tools for first-time OAuth2 authorization of a single blog.
    - `TAuthorizer.get_authorize_url()` returns a URL where you can log in to your Tumblr account and choose whether to allow this app access, using Tumblr's [/oauth2/authorize](https://www.tumblr.com/docs/en/api/v2#oauth2authorize---authorization-request) endpoint. Afterwards, the user is returned to the app's callback URL with an authorization code.
    - `TAuthorizer.get_tokens(code, state)`: exchanges an authorization code for an access token and refresh token, using Tumblr's [/v2/oauth2/token](https://www.tumblr.com/docs/en/api/v2#v2oauth2token---authorization-code-grant-request) endpoint.
        - `code: str`: The code sent by Tumblr in the API callback.
        - `state: str`: The state sent by Tumblr in the API callback.

- `src.t_requester.TRequester`: Contains the tools for a single OAuth2-authenticated blog to make requests to tumblr's endpoints.
    - `TRequester(consumer_key, consumer_secret, access_token, refresh_token, blog_url, expires=0)`: Initializing a TRequester object:
        - `consumer_key: str`: the client ID of your application.
        - `consumer_secret: str`: the client secret of your application.
        - `access_token: str`: the OAuth2 access token for the authenticated blog.
        - `refresh_token: str`: the OAuth2 refresh token for the authenticated blog.
        - `blog_url: str`: the username of the authenticated blog. Cannot be a side blog.
        - `expires: int`: a unix timestamp of the estimated expiration time. Defaults to zero, 
    - `TRequester.request(endpoint, method='GET', blog_url=None, params=None, extra_path_param=None)`: Makes a request to one of Tumblr's endpoints for authorized blogs.
        - `endpoint: str`: a Blog, User, or Tagged endpoint from [Tumblr's API](https://www.tumblr.com/docs/en/api/v2), such as `'/info'`.
        - `method: str`: GET or POST, as specified in Tumblr's documentation for the endpoint.
        - `blog_url: str`: The username of the desired blog. Should be included IF AND ONLY IF the endpoint is a Blog method, meaning it requires a "{blog-identifier}" as a path parameter according to Tumblr's documentation.
        - `params: dict`: Query parameters from Tumblr's documentation.
        - `extra_path_param: str`: Any request path parameters ASIDE from blog-identifier, such as the "size" parameter for the `/avatar` endpoint, which could be provided here as `'96'`.
    - `TRequester.get(...)` and `TRequester.post(...)` are both wrappers of the `request` function, which just specify the request `method`, and require all of the other parameters as normal.
    - `TRequester.refresh_tokens()`: Attempts to refresh the blog's tokens. This method is called automatically if the token seems to be expired or nearly expired.

- `src.t_error.TumblrError`: a custom Exception function for when the Tumblr API returns an error response.

- `src.blog.Blog`: a class to call more complex functions using a TRequester on an authorized blog.
    - `Blog(blog_url)`: Initializing a Blog object:
        - `blog_url: str`: the username of the authenticated blog. Cannot be a side blog.
    - `Blog.follow(urls)`: follows all blogs in a given list.
        - `urls: list`: A list of blog usernames to follow.
    - `Blog.unfollow(urls)`: unfollows all blogs in a given list.
        - `urls: list`: A list of blog usernames to unfollow.
    - `Blog.last_response(post_id, partner=None)`: Identifies the last reblogger of a certain post.
        - `post_id: int`: ID of the post to track.
        - `partner_url: str`: The URL of a reblogger. If included, this function returns whether the original poster or the specified partner was last to reblog. If left as `None`, this function returns the last reblogger of the post in general.
    - `Blog.get_activity(month=None, year=None, min_activity=2, ic_tag=None, blog_url=None, time_zone='EST')`: Returns a statement on how many posts have been made within a specific month.
        -  `month: int`: The month number to search within. Defaults to the current month.
        - `year: int`: The year number to search within. Defaults to the current year.
        - `min_activity: int`: The minimum number of posts to mark as passing activity.
        - `ic_tag: str`: If specified, only posts with the given tag will be counted.
        - `blog_url: str`: The username of the blog to search. Defaults to the authenticated blog in use.
        - `time_zone: str`: A standard abbreviation of the desired time zone, used to decide the exact start and end of the month.
    - `Blog.get_blogs()`: Returns a list of blogs the authenticated user has access to (main and side blogs).
    - `Blog.get_following()`: Returns a list of blogs the authenticated user is following.
    - `Blog.replace_tag(old_tag, new_tag, append=False, blog_url=None)`: Replaces a specific tag with another tag on a blog the authenticated user has access to.
        - `old_tag: str`: The tag to be replaced.
        - `new_tag: str`: The new tag to add.
        - `append: bool`: If True, the old tag will not be deleted on the posts found.
        - `blog_url: str`: The username of the blog to perform the operation on. Defaults to the main authenticated blog, but may also be set to a sideblog the user has access to.
    - `Blog.append_tag(post_id, new_tag, blog_url=None)`: Appends a tag to a single post.
        - `post_id: int`: ID of the post to be updated.
        - `new_tag: str`: The tag to add.
        - `blog_url: str`: The username of the blog to perform the operation on. Defaults to the main authenticated blog, but may also be set to a sideblog the user has access to.
    - `Blog.remove_tag(post_id, new_tag, blog_url=None)`: Removes a tag from a single post.
        - `post_id: int`: ID of the post to be updated.
        - `old_tag: str`: The tag to remove.
        - `blog_url: str`: The username of the blog to perform the operation on. Defaults to the main authenticated blog, but may also be set to a sideblog the user has access to.
    - `Blog.get_tagged(tag_list, blog_url=None)`: returns a set of post IDs from one blog which contain all the tags in a given list.
        - `tag_list`: the list of tags to search for.
        - `blog_url: str`: The username of the blog to search.
    - `Blog.get_reblog_tags(post_id, blog_url=None)`: returns two dicts, where the keys are the IDs of posts containing tags. In the first, the values are the lists of tags on each post. In the second, the values are the usernames of the rebloggers.
        - `post_id`: the ID of the post to search.
        - `blog_url: str`: The username of the blog the post is from.
    - `Blog.save_avatar(location='./avatar.jpg', blog_url=None, dims=64)`: saves the avatar image of a specified blog.
        - `location: str`: the file location to save the avatar.
        - `blog_url: str`: The username of the blog to pull the avatar from.
        - `dims: int`: The singular width/length value for the image (always a square). Must be one of the values: 16, 24, 30, 40, 48, 64, 96, 128, 512.

- `src.get_args.get_args()`: A supplementary function to `t.py`. Creates the subparsers for each command.

- `add_blog.py`: Run this file to authenticate a new blog. The app's callback URL must be set to `http://localhost:8080/callback`. It will automatically open a link in your browser with which to authenticate your account.

- `t.py`: Implements some of the `Blog` class functions as command-line utilities.
    - Try `python t.py -h` for a list of commands.
    - Try `python t.py {command} -h` with any of the given commands for specific syntax.

- `requirements.txt`: The set of Python libraries required to use this repository. Run `pip install -r requirements.txt` in the terminal to install all of them at once.