from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
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

    comments = []
    # loads comments from that subreddit
    for comment in reddit.subreddit(sub).comments(limit=5):
        comments.append(comment.body)

    json_comments = JsonResponse(comments, safe=False)
    return HttpResponse(json_comments, content_type="application/json")
