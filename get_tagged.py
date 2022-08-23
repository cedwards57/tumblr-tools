from src.authblog import AuthBlog
import argparse

parser = argparse.ArgumentParser(description="Specify blog and list of tags")
parser.add_argument(
    dest="blog",
    action="store",
    metavar="blog-username",
    help="specify main blog username"
)
parser.add_argument(
    dest="tag_list",
    action="store",
    metavar="\"tag 1,tag 2,tag 3\"",
    help="the tag to be replaced"
)
parser.add_argument(
    "-s",
    "--sideblog",
    required=False,
    dest="sideblog",
    action="store",
    help="if searching a sideblog, specify url"
)
args = parser.parse_args()

tag_list = args.tag_list.split(",")

if len(tag_list) == 1:
    url_tail = tag_list[0].replace(" ","%20")
    print(f"You could just go to http://{args.blog}.tumblr.com/tagged/{url_tail}, but...")

blog = AuthBlog(args.blog)
blog.get_tagged(args.tag_list)