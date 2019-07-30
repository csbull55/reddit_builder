from django.shortcuts import render
import praw


# Create your views here.
def home(request):
    return render(request, 'comment_stream/home.html')


# this is the comment stream
def stream(request):
    # creates reddit instance
    reddit = praw.Reddit('bot1',
                         user_agent='comment_bot_agent')

    # gets subreddit
    sub = request.GET['fulltext']

    # creates empty dicts
    comments = {}
    # auth = {}
    # comment_time = {}

    # loads comments from that subreddit
    for comment in reddit.subreddit(sub).comments():
        comments[comment.id] = {
                                'body': comment.body,
                                'auth': comment.author,
                                'comment_time': comment.created_utc
                                }

    # finds average length of comment
    # avg_len = sum(comments_len) / len(comments_len)

    return render(request, 'comment_stream/comments.html',
                  {'subname': sub,
                   'comments': list(comments),
                   'count': len(comments),
                   # 'comment_length': round(avg_len, 0),
                   # 'user_count': len(auth),
                   }
                  )
