from django.shortcuts import render
import praw


# Create your views here.
def home(request):
    return render(request, 'comment_stream/home.html')


# this is the comment stream
def stream(request):
    def dict_pull(dict, column):
        data = []
        for i in dict:
            data.append(dict[i][column])
        return data

    # creates reddit instance
    reddit = praw.Reddit('bot1',
                         user_agent='comment_bot_agent')

    # gets subreddit
    sub = request.GET['fulltext']

    # creates empty dicts
    comments = {}

    # loads comments from that subreddit
    for comment in reddit.subreddit(sub).comments():
        comments[comment.id] = {
                                'body': comment.body,
                                'auth': comment.author,
                                'comment_time': comment.created_utc
                                }

    # finds average character lentth of a comment
    avg_len = sum(len(s) for s in dict_pull(comments, 'body')) / len(comments)

    # finds num of unique users
    auth = set(dict_pull(comments, 'auth'))

    # finds date/time range, avg comments/min
    times = dict_pull(comments, 'comment_time')
    rng = (max(times) - min(times)) / 60
    comment_min = float("{0:.2f}".format(len(comments) / rng))

    return render(request, 'comment_stream/comments.html',
                  {'subname': sub,
                   'comments': dict_pull(comments, 'body'),
                   'count': len(comments),
                   'comment_length': avg_len,
                   'user_count': len(auth),
                   'cmt_rng': rng,
                   'comment_min': comment_min,
                   }
                  )
