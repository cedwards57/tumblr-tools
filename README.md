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
2. run `python3 addblog.py`
3. A link to a tumblr authentication screen should automatically open in your browser.
4. Click "Allow".
5. You're done! Your authorization keys have been logged, and you can read/write to blogs on that account. If you have multiple accounts, you can repeat these steps for each one to be authorized for all of them.

## Using this repository

Run `python3 -m t -h` from the root directory to view available commands. Use `python3 -m t <command> -h` to view usage of a given command.

The `get-activity` function expects a file `json/tags.json` at the root, with contents that specify the tag you want to track for each blog's url:
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

However, you can also just specify `--tags-file none` to get a count of all posts within the current month.

`get_tagged.py`: Searches a single blog for posts that contain ALL tags in a given list. Takes 2 arguments (main blog url, list of tags). If searching a sideblog, add the option `-b sideblog-url`.