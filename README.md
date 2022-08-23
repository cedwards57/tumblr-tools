## About

This is a set of code for setting up API access for Tumblr blogs, for use by command line. Built-in features include mass-following a given list of blogs, and features like checking if a minimum number of posts were made in a month, or using a tag replacer.

## Getting Started

```
git clone https://github.com/thestarjar/tumblr-app
cd tumblr-app
pip install -r requirements.txt
```

You'll need to [register an application with Tumblr](https://www.tumblr.com/oauth/apps). Then create a file in the root of your repository called `.env` and give it these contents:

```
export CONSUMER_KEY="your_key_here"
export CONSUMER_SECRET="your_secret_key_here"
```

Now that you've set up, you can go about authorizing your specific blogs:

1. Log in to your tumblr account.
2. run `addblog.py`
3. Above all the Flask run text, your console should print out `Connect with Tumblr via: <url>`. Go to that URL.
4. Click "Allow".
5. You're done! Your authorization keys have been logged, and you can read/write to blogs on that account. If you have multiple accounts, you can repeat these steps for each one to be authorized for all of them.

## Using this repository

`src/authblog.py`: A class for app-authorized blogs. Contains various handy functions. You can tweak them to your needs or add more. The activity function is based on the needs of RP blogs in groups that have active posting requirements.

`get_activity.py`: Checks the activity on a main RP blog, for role-play communities that check for that. Takes one argument for the blog username.

`replace_tag.py`: takes 3 arguments (main blog, old tag, new tag). Options `-s sideblog-url` if replacing tags on a sideblog, and `-a` if you want to append the new tag rather than replace the old one.

The `TAGS` variable referenced in `authblog.py` expects a file `json/tags.json` at the root, with contents that specify the tag you want to track for each blog's url:
```
{
    "your_url_1": {
        "ic": "your_tag_here"
    },
    "your_url_2": {
        "ic": "your_tag_here"
    }
}
```

However, you can also just remove the "tag" parameter from the request altogether, to get a count of all posts within the current month.