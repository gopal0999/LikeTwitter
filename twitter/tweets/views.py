import random
from django.conf import settings
from django.http import HttpResponse,Http404,JsonResponse
from django.shortcuts import render,redirect
from django.utils.http import is_safe_url

from rest_framework.decorators import api_view, permission_classes,authentication_classes
# by default included in the settings
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from .forms import TweetForm
from .models import Tweet
from .serializers import TweetSerializer, TweetActionSerializer, TweetCreateSerializer

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request,"pages/home.html", context={}, status=200)

@api_view(['POST'])
@authentication_classes([SessionAuthentication]) # by default in rest_framework
@permission_classes([IsAuthenticated])
def tweet_create_view(request):
    serializer = TweetCreateSerializer(data=request.POST or None)
    if serializer.is_valid():
        serializer.save(user = request.user)
        return JsonResponse(serializer.data, status = 201)
    return JsonResponse({}, status=400)

@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    # To serialize a queryset or list of objects instead of a single object 
    # instance, you should pass the many=True flag when instantiating the serializer.
    # You can then pass a queryset or list of objects to be serialized.
    serializedTweets = TweetSerializer(qs, many=True)
    # print(serializedTweets.data)
    # return JsonResponse(data)
    # instead of JsonResponse will use just Response imported from rest_framework
    return Response(serializedTweets.data, status=200)

@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id = tweet_id)
    if not qs.exists():
        return Response({},status=404)
    obj = qs.first()
    serialisedTweet = TweetSerializer(obj)
    return Response(serialisedTweet.data, status=200)

@api_view(['DELETE','POST'])
@authentication_classes([SessionAuthentication]) # by default in rest_framework
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id = tweet_id)
    if not qs.exists():
        return Response({},status=404)
    if request.user != qs.first().user:
        return Response({'message':"unauthorised"},status=403)
    obj = qs.first()
    obj.delete()
    return Response({"message":"Tweet Removed"}, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view(request, *args, **kwargs):
    '''
    id is required.
    Action options are: like, unlike, retweet
    '''
    # 400 40 bad request error was due to tweet_id in place of just id in serializers.py
    serializer = TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get("id")
        action = data.get("action")
        # sorry this is the content of the original tweet
        content = data.get("content") #not this content will be used if we want to add something while retweeting any context
        qs = Tweet.objects.filter(id=tweet_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if action == "like":
            obj.likes.add(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "unlike":
            obj.likes.remove(request.user)
        elif action == "retweet":
            new_tweet = Tweet.objects.create(
                    user=request.user, 
                    parent=obj,
                    content=content,#therefore its used in retweet action
                    )
            serializer = TweetSerializer(new_tweet)
            return Response(serializer.data, status=200)
    return Response({}, status=200)

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

def tweet_list_view_pure_django(request, *args, **kwargs):
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


def tweet_detail_view_pure_django(request, tweet_id, *args, **kwargs):
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