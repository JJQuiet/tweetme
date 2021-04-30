from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
import random
from django.utils.http import is_safe_url
from django.conf import settings
# Create your views here.
from .models import Tweet
from .forms import TweetForm
from .serializers import TweetSerializer, TweetCreateSerializer
# from rest_framework import response   # 'module' object is not callable
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


@api_view(['POST']) ## http mehtod the client === POST 
# @authentication_classes([SessionAuthentication, MyCustomAuth]) # only SessionAuthentication can be permission, combine with next @permission
@permission_classes([IsAuthenticated])
def tweet_action_view(request, *args, **kwargs):
    serializer = TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get("id")
        action = data.get("action")
        content = data.get("content")
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
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "retweet":
            new_tweet = Tweet.objects.create(
                    user=request.user, 
                    parent=obj,
                    content=content,
                    )
            serializer = TweetSerializer(new_tweet)
            return Response(serializer.data, status=201)
    return Response({}, status=200)

@api_view(['POST']) # http method the client == POST
# @authentication_classes([SessionAuthentication, MyCustomAuth])
@permission_classes([IsAuthenticated]) # REST API course
def tweet_create_view(request, *args, **kwargs):
    print('request.data is: ', request.data)
    serializer = TweetCreateSerializer(data=request.POST or None)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=500)


@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message": "You can not delete this tweet!"}, status=401)
    obj = qs.first()
    obj.delete()
    return Response(serializer.data, status=200)

@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    # print('Tweet.objects.first(): ', Tweet.objects.first().content)
    serializer = TweetSerializer(qs, many=True)
    # tweet_list = [x.serialize() for x in qs]
    # data = {
    #     "isUser": False,
    #     "response": tweet_list
    # }
    return Response(serializer.data)

    
def tweet_create_pure_view(request, *args, **kwargs):
    '''
    REST API Create View Django Rest Framework
    '''
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    # print(abc)
    # 上面这句话会报错 500 (Internal Server Error)
    form = TweetForm(request.POST or None)
    # 上面的一句相当于判断if method == POST
    # print('post data is: ', request.POST)
    if form.is_valid():
        next_url = request.POST.get('next') or None
        # print('next_url:   ', next_url)
        # print(form)
        obj = form.save(commit=False)
        print(obj)
        obj.user = user # Annon User
        # do other form related logic
        obj.save()
        print(obj)
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201) # 201 == created items
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            print('it is a save url')
            return redirect(next_url)
            # return redirect('/')
        # form.save()
        form = TweetForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
    return render(request, 'components/form.html', context={'form': form})


def tweet_list_view_pure_django(request, *args, **kwargs):
    '''
    REST API VIEW
    Consume by JavaScript or Swift/Java/iOS/Andriod
    return json data
    '''
    qs = Tweet.objects.all()
    # tweet_list = [{"id": x.id, "content": x.content, "likes": random.randint(0, 200)} for x in qs]
    tweet_list = [x.serialize() for x in qs]
    data = {
        "isUser": False,
        "response": tweet_list
    }
    return JsonResponse(data)


def tweet_detail_view_pure_django(request, tweet_id, *args, **kwargs):
    print(args, kwargs)
    data = {
        "id": tweet_id,
        # "content": obj.c6ontent,
    }
    status = 200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
    except:
        # raise Http404
        data['message'] = "Not found"
        status = 404
    # return HttpResponse(f"<h1>id{tweet_id}</h1><p>{obj.content}</p>")
    # HttpResponse前面需要加上f，如果有变量的话 
    return JsonResponse(data, status=status) # json.dumps content_type='app111




def home_view(request, *args, **kwargs):
    # print('request user is:    ', request.user or None)
    # print(args, kwargs)
    # return HttpResponse("<h1>Hello World</h1>")
    return render(request, "pages/home.html", context={}, status=200)



