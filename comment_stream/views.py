from django.shortcuts import render
import praw


# Create your views here.
def home(request):
    return render(request, 'comment_stream/home.html')


# this is the comment stream
def stream(request):
    # creates reddit instance
    reddit = praw.Reddit('comment_bot',
                         user_agent='comment_bot_agent')

    # gets subreddit
    sub = request.GET['fulltext']

    # creates empty dicts
    comments = {}
    comments_len = {}

    # loads comments from that subreddit
    for comment in reddit.subreddit(sub).comments():
        comments[comment.body] = 1
        comments_len[len(comment.body)] = 1

    # finds average length of comment
    avg_len = sum(comments_len) / len(comments_len)

    return render(request, 'comment_stream/comments.html', {'subname': sub,
                                                            'comments': comments,
                                                            'count': len(comments),
                                                            'comment_length': round(avg_len, 0),
                                                            }
                  )

