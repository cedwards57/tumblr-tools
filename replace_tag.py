from src.authblog import AuthBlog
import argparse

parser = argparse.ArgumentParser(description="Specify blog, old tag, and replacement tag")
parser.add_argument(
    dest="blog",
    action="store",
    metavar="blog-username",
    help="specify blog username"
)
parser.add_argument(
    dest="old_tag",
    action="store",
    metavar="\"old-tag\"",
    help="the tag to be replaced"
)
parser.add_argument(
    dest="new_tag",
    action="store",
    metavar="\"new-tag\"",
    help="the updated tag"
)
parser.add_argument(
    "-a",
    "--append",
    required=False,
    dest="append",
    action="store_true",
    help="append tag instead of replace"
)
parser.add_argument(
    "-s",
    "--sideblog",
    required=False,
    dest="sideblog",
    action="store",
    help="if replacing tags on a sideblog, specify url"
)
args = parser.parse_args()

blog = AuthBlog(args.blog)
blog.replace_tag(args.old_tag, args.new_tag, append=args.append, blog_url=args.sideblog)