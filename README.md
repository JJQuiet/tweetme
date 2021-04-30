# SETUP

## EDITOR

* python interpreter select

## GIT

* git
* git init
* git add --all
* git status
* git commit -m "Initial Commit"

# TODO

## Tweets

* User Permissions

  * Creating

    * Text

    * Image

  * Delete

  * Retweeting

  * Liking

## Users

* Register
* Login
* Logout
* Profile
  * Image?
  * Text?
  * Follow Button
* Feed
  * User's feed only?
  * User + who they follow?

## Following/Followers

## LongTermTodos

1. Notifications
2. DM
3. Explore -> finding hashtags

# Javascript

## FUNCTION

### Dynamic Load



# URL

## redirect

### safe redirect

# RECORD

2:52:00, 3:28:24

end: 5:04:10

# shell

## py manage.py shell

* objs = Tweet.objects.filter(user__username='myName')
* objs = Tweet.objects.filter(user=myid)
* ```objs = Tweet.objects.filter(user__username__iexact='myName')```
* objs = Tweet.objects.filter(content__iexact='abc')

# DEBUG

## views.py

* [serializer = TweetSerializer(data = request.POST or None)](https://img.imgdb.cn/item/607b091b8322e6675c86c504.jpg)

* [if后面缺少了:](https://img.imgdb.cn/item/607d255a8322e6675cefea04.jpg)

## admin.py

* [UnicodeDecodeError: 'gbk' codec can't decode byte 0xa6 in position 9737: illegal multibyte sequence](https://img.imgdb.cn/item/607d4ed18322e6675c432073.jpg)

# IMPORTANT

* class Meta:里的fields指定form要渲染的model的列

