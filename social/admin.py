from django.contrib import admin
from social.models import *

class userregister(admin.ModelAdmin):
    list_display=['name','uname','email','phone','bio','portfolio_img','bg_img']

admin.site.register(UserRegister,userregister)

class userpost(admin.ModelAdmin):
    list_display=['id','post', 'post_time','post_date','post_image','post_video']

admin.site.register(UserPost,userpost)

class aboutuser(admin.ModelAdmin):
    list_display=['id','user','live','work','study','ufrom']
admin.site.register(AboutUser,aboutuser)

admin.site.register(Like)
class followercount(admin.ModelAdmin):
    list_display=['user', 'follower']
admin.site.register(FollowersCount, followercount)

admin.site.register(Comment)