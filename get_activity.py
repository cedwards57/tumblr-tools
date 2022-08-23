'''Check RP activity on a specific blog.'''

from src.authblog import AuthBlog
import argparse

parser = argparse.ArgumentParser(description="Specify blog")
parser.add_argument(
    dest="blog",
    action="store",
    metavar="blog-username",
    help="specify blog username"
)
parser.add_argument(
    "-m",
    "--month",
    dest="month",
    action="store",
    metavar="month",
    type=int,
    help="specify month to check activity for (default current)"
)
parser.add_argument(
    "-y",
    "--year",
    dest="year",
    action="store",
    metavar="year",
    type=int,
    help="specify 4-digit year to check activity for (default current)"
)
parser.add_argument(
    "-n",
    "--min-activity",
    dest="min_activity",
    action="store",
    metavar="min-activity",
    type=int,
    help="number of posts you should have in a month (default 2)"
)
args = parser.parse_args()

blog = AuthBlog(args.blog)
print(blog.activity(month=args.month, year=args.year, min_activity=args.min_activity))