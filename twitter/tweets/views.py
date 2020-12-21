import random
from django.conf import settings
from django.http import HttpResponse,Http404,JsonResponse
from django.shortcuts import render,redirect
from django.utils.http import is_safe_url

from .forms import TweetForm
from .models import Tweet
from .serializers import TweetSerializer

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.
def home_view(request, *args, **kwargs):
    # return HttpResponse(f"<h1>HELLO TWITTER {kwargs['tweet_id']}</h1>")
    return render(request,"pages/home.html", context={}, status=200)

def tweet_create_view(request):
    # print(request.POST)
    serializer = TweetSerializer(data=request.POST or None)
    if serializer.is_valid():
        print(request.user)# gns
        obj = serializer.save(user = request.user)
        print("@@obj@@",obj) #@@obj@@ again
        print(serializer.data)
        return JsonResponse(serializer.data, status = 201)
    return JsonResponse({}, status=400)

def tweet_create_view_pure_django(request, *args, **kwargs):
    user = request.user
    if not user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status = 401)
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        # not commited to do other form related logic
        obj.user = user
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status = 201)# 201 for created
        if next_url != None and is_safe_url(next_url,ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status = 400)
    return render(request, 'components/form.html', context={"form":form})

def tweet_list_view(request, *args, **kwargs):
    """
    REST API VIEW
    Consume by JavaScript or Swift/Java/iOS/Andriod
    return json data
    """
    qs = Tweet.objects.all()
    # likes are coming back because of this 
    # because serialize is defined in the models.py Tweet model
    # and there while serializing it return a random number for like
    tweets_list = [x.serialize() for x in qs]
    data = {
        "isUser": False,
        "response": tweets_list
    }
    return JsonResponse(data)


def tweet_detail_view(request, tweet_id, *args, **kwargs):
    """
    REST API VIEW
    Consume by JavaScript or Swift/Java/iOS/Andriod
    return json data
    """
    data = {
        "id": tweet_id,
    }
    status = 200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
    except:
        data['message'] = "Not found"
        status = 404
    return JsonResponse(data, status=status) # json.dumps content_type='application/json'

# def detailView(request,tweet_id, *args, **kwargs):
#     # Rest API view
#     data = {"id" : tweet_id}
#     status = 200
#     try:
#         obj = Tweet.objects.get(id = tweet_id)
#         data["content"] = obj.content
#     except:
#         # raise Http404 
#         data['message'] = "Not Found"
#         status = 404
#     # return HttpResponse(f"<h1>{tweet_id} : {obj.content}</h1>")
#     return JsonResponse(data,status = status)

# def listView(request, *args, **kwargs):
#     # Rest API view
#     tweets = Tweet.objects.all()
#     tweetsList = [{"id":tweet.id, "content":tweet.content, "likes": random.randint(0,122)} for tweet in tweets]
#     data = {"isUser" : False, "response": tweetsList}
#     print(data)
#     return JsonResponse(data)