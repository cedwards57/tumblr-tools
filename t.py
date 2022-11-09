from src.authblog import AuthBlog
from src.get_args import get_args

def get_activity(args):
    blog = AuthBlog(args.blog)
    print(blog.get_activity(month=args.month, year=args.year, min_activity=args.min_activity, tags_file=args.tags_file))

def get_tagged(args):
    tag_list = args.tag_list.split(",")
    if len(tag_list) == 1:
        url_tail = tag_list[0].replace(" ","%20")
        print(f"You could just go to http://{args.blog}.tumblr.com/tagged/{url_tail}, but...")
    blog = AuthBlog(args.blog)
    print(blog.get_tagged(tag_list, blog_url=args.sideblog))

def replace_tag(args):
    blog = AuthBlog(args.blog)
    blog.replace_tag(args.old_tag, args.new_tag, append=args.append, blog_url=args.sideblog)
    print("Tag replaced.")

def get_reblog_tags(args):
    blog = AuthBlog(args.blog)
    tags, urls = blog.get_reblog_tags(args.post_id, blog_url=args.sideblog)
    for id in tags.keys():
        print(f'{urls[id]}: {tags[id]}')

if __name__ == '__main__':
    args = get_args()
    if args.cmd == 'get-activity':
        get_activity(args)
    if args.cmd == 'get-tagged':
        get_tagged(args)
    if args.cmd == 'replace-tag':
        replace_tag(args)
    if args.cmd == 'get-reblog-tags':
        get_reblog_tags(args)
    
    
