import argparse

def get_args():
    parser = argparse.ArgumentParser(description="Specify Command")
    subparsers = parser.add_subparsers(dest='cmd')

    sub_get_activity = subparsers.add_parser('get-activity')
    sub_get_activity.add_argument(
        dest="blog",
        action="store",
        metavar="blog-username",
        help="specify your main authenticated blog's username"
    )
    sub_get_activity.add_argument(
        "-m",
        "--month",
        dest="month",
        action="store",
        metavar="month",
        type=int,
        help="specify month to check activity for (default current)"
    )
    sub_get_activity.add_argument(
        "-y",
        "--year",
        dest="year",
        action="store",
        metavar="year",
        type=int,
        help="specify 4-digit year to check activity for (default current)"
    )
    sub_get_activity.add_argument(
        "-n",
        "--min-activity",
        dest="min_activity",
        action="store",
        metavar="min-activity",
        type=int,
        help="number of posts you should have in a month (default 2)"
    )
    sub_get_activity.add_argument(
        "-t",
        "--tag",
        dest="ic_tag",
        default='ic',
        action="store",
        metavar="tags-file",
        type=str,
        help="The tag to check for activity. Default 'ic'. Specify 'none' to check all posts."
    )

    sub_get_tagged = subparsers.add_parser('get-tagged')
    sub_get_tagged.add_argument(
        dest="blog",
        action="store",
        metavar="blog-username",
        help="specify your main authenticated blog's username"
    )
    sub_get_tagged.add_argument(
        dest="tag_list",
        action="store",
        metavar="\"tag 1,tag 2,tag 3\"",
        help="the tags to search for"
    )
    sub_get_tagged.add_argument(
        "-b",
        "--sideblog",
        required=False,
        dest="sideblog",
        action="store",
        help="if searching a sideblog, or someone else's blog, specify url"
    )

    sub_replace_tag = subparsers.add_parser('replace-tag')
    sub_replace_tag.add_argument(
        dest="blog",
        action="store",
        metavar="blog-username",
        help="specify blog username"
    )
    sub_replace_tag.add_argument(
        dest="old_tag",
        action="store",
        metavar="\"old-tag\"",
        help="the tag to be replaced"
    )
    sub_replace_tag.add_argument(
        dest="new_tag",
        action="store",
        metavar="\"new-tag\"",
        help="the updated tag"
    )
    sub_replace_tag.add_argument(
        "-a",
        "--append",
        required=False,
        dest="append",
        action="store_true",
        help="append tag instead of replace"
    )
    sub_replace_tag.add_argument(
        "-b",
        "--sideblog",
        required=False,
        dest="sideblog",
        action="store",
        help="if replacing tags on a sideblog, specify url"
    )

    sub_get_reblog_tags = subparsers.add_parser('get-reblog-tags')
    sub_get_reblog_tags.add_argument(
        dest="blog",
        action="store",
        metavar='blog-username',
        help="specify your main authenticated blog's username"
    )
    sub_get_reblog_tags.add_argument(
        dest="post_id",
        action="store",
        metavar = 'post_ID',
        help="specify post ID"
    )
    sub_get_reblog_tags.add_argument(
        "-b",
        "--sideblog",
        required=False,
        dest="sideblog",
        action="store",
        help="if viewing tags of a post by a sideblog, or someone else's blog, specify url"
    )

    sub_follow = subparsers.add_parser('follow')
    sub_follow.add_argument(
        dest="blog",
        action="store",
        metavar="blog-username",
        help="specify your main authenticated blog's username"
    )
    sub_follow.add_argument(
        dest="url_list",
        action="store",
        metavar="\"blog 1,blog 2,blog 3\"",
        help="the blogs to follow"
    )

    sub_follow = subparsers.add_parser('unfollow')
    sub_follow.add_argument(
        dest="blog",
        action="store",
        metavar="blog-username",
        help="specify your main authenticated blog's username"
    )
    sub_follow.add_argument(
        dest="url_list",
        action="store",
        metavar="\"blog 1,blog 2,blog 3\"",
        help="the blogs to unfollow"
    )

    args = parser.parse_args()
    return args