from django.db import models

class UserRegister(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    uname = models.CharField(max_length=200, default="")
    email = models.EmailField()
    password = models.CharField(max_length=200)
    rpassword = models.CharField(max_length=200)
    phone = models.IntegerField()
    friends = models.ManyToManyField('self', blank=True)
    bio = models.CharField(max_length=200, default="I am a new user.")
    portfolio_img=models.ImageField(upload_to="portfolio_images",default="default_pro_pic.jpg")
    bg_img=models.ImageField(upload_to="bg_images",default="default_bg_img.jpg")

class UserPost(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserRegister, on_delete=models.CASCADE)
    post = models.CharField(max_length=200)
    likes = models.ManyToManyField(UserRegister, through='Like', related_name='liked_posts')
    post_date = models.DateField(auto_now_add=True)
    post_time = models.TimeField(auto_now_add=True)
    post_image = models.ImageField(upload_to="post_images", default="",blank=True, null=True)
    post_video = models.FileField(upload_to="post_videos", default="",blank=True, null=True)
    # post_comments=models.ForeignKey(Comment,on_delete=models.CASCADE)
        

class Like(models.Model):
    user = models.ForeignKey(UserRegister, on_delete=models.CASCADE)
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
class AboutUser(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserRegister, on_delete=models.CASCADE)
    live = models.CharField(max_length=200, default="",blank=True, null=True)
    work = models.CharField(max_length=200, default="",blank=True, null=True)
    study = models.CharField(max_length=200, default="",blank=True, null=True)
    ufrom = models.CharField(max_length=200, default="",blank=True, null=True)

class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user
    
class Comment(models.Model):
    user = models.ForeignKey(UserRegister, on_delete=models.CASCADE)
    post_user = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name='comments')  # Assuming you have a Post model
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
    
