from django.shortcuts import render,redirect
from social.forms import CommentForm
from social.models import *
from social.forms import *

from django.core.exceptions import ObjectDoesNotExist

def index(request):
    if 'email' in request.session:
        email = request.session['email']
        all_data=UserRegister.objects.all()
        # try:
        data = UserRegister.objects.get(email=email)  
        # common posts section
        if UserPost.objects.exists() :
            all_posts = UserPost.objects.order_by('-post_date', '-post_time')
        else:
            all_posts = None
        # # create new post
        if UserPost.objects.filter(user=data).exists():
            user_posts = UserPost.objects.filter(user=data)
        else:
            user_posts = None

        # post_comments=Comment.objects.all()
        post_comments = []
        for post in all_posts:
            # print(post.user) 
            comments = Comment.objects.filter(post_user_id=post.id)

            post_comments.append({
                'post':post, 
                'comments':comments
            })

        if 'post' in request.POST:
            post = request.POST['post']
            media_file = request.FILES.get('media', None)

            new_post = UserPost(user=data, post=post)

            if media_file:
                if media_file.content_type.startswith('image'):
                    new_post.post_image = media_file
                elif media_file.content_type.startswith('video'):
                    new_post.post_video = media_file
            new_post.save()
            return redirect('/')
        else:
            pass
        # about section
        if(AboutUser.objects.filter(user=data).exists() == False):
            user_about = AboutUser(user=data)
            user_about.save()
        user_about=AboutUser.objects.get(user=data)

        # Suggest following
        button_text='Follow'
        # user_following = len(FollowersCount.objects.filter(follower=data.name))
        following=[]
        for i in FollowersCount.objects.filter(follower=data.name):
            print(i.user)
            print(UserRegister.objects.get(name=i.user))
            following.append(UserRegister.objects.get(name=i.user))
            if FollowersCount.objects.filter(follower=data.name, user=i.user).first():
                button_text = 'Follow'
            else:
                button_text = 'Unfollow'

        context = {
            'all_data':all_data,
            'data': data,
            'all_posts': all_posts,
            'user_posts': user_posts,
            'user_about': user_about,
            'post_comments':post_comments,
            'following':following,
            'button_text':button_text,
        }
        return render(request, 'index.html',context)
        # except ObjectDoesNotExist:
        #     return render(request, 'login.html', {'message': 'User not found.'})
    else:
        return render(request, 'login.html', {'message': 'User Not Found'})


from django.http import JsonResponse
def like_post(request, post_id):
    post = UserPost.objects.get(id=post_id)
    user = UserRegister.objects.get(email=request.session['email'])

    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)

    like_count = post.likes.count()  # Get the updated like count
    is_liked = post.likes.filter(email=request.session['email']).exists()

    return JsonResponse({'redirect_url': '/', 'like_count': like_count, 'is_liked':is_liked})  # Return the updated like count

    # return redirect('/', post_id=post_id)

def register(request):
    if request.method=="POST":
        name1=request.POST['name']
        uname1=request.POST['uname']
        email1=request.POST['email']
        password1=request.POST['password']
        rpassword1=request.POST['rpassword']
        phone1=request.POST['phone']
        print(name1,uname1,email1,password1,rpassword1,phone1)
        if(password1==rpassword1):
            data=UserRegister(name=name1,uname=uname1,email=email1,password=password1,phone=phone1,rpassword=rpassword1)
            a=UserRegister.objects.filter(email=email1)
            b=UserRegister.objects.filter(uname=uname1)
            if len(a)==0 and len(b)==0:
                data.save()
                return redirect('login1')
            else:
                return render(request,'register.html',{'message':"user alredy exist OR username alredy exist"}) 
        else:
            return render(request,'register.html',{'message':"password does not match"})
    return render(request,'register.html')  

def login(request):
    if request.method == "POST":
        email1 = request.POST['email']
        password1 = request.POST['password']
        try:
            data = UserRegister.objects.get(email=email1, password=password1)
            if data:
                request.session['user_id'] = data.id
                request.session['email'] = data.email
                return redirect('/')
            else:
                return render(request, 'login.html', {'message': 'Invalid email or password'})
        except:
            return render(request, 'login.html', {'message': 'Invalid email or password'})
    return render(request, 'login.html')

def logout(request):
    try:
        del request.session['email']
    except:
        pass
    return redirect('login1')

from django.core.mail import send_mail
import random
def forgot(request):
    if request.POST:
        useremail=request.POST['email']
        try:
            data=UserRegister.objects.get(email=useremail)
            otp = random.randint(100000, 999999)
            if data:
                send_mail(
                "Forgot Password",
                "Dear " +str(data.name)+"\n Your OTP is :"+str(otp),
                "youremail",
                [useremail],
                fail_silently=False,
                )
                request.session['otp'] = otp  # Store OTP in session
                return redirect('verify')
                # return render(request, 'verify.html', {'otp': otp,'email':data, 'message':'OTP is sent to your mail'})  # Render the verify.html template with otp
            else:
                return render(request,'forgot.html',{'message':'Email Id Not Found'})
        except:
            return render(request,'forgot.html',{'message':'Email Id Not There'})
    return render(request,'forgot.html')

def verify(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)
        otp = request.POST.get('otp')
        if otp == str(request.session.get('otp')):
            print(otp)
            del request.session['otp']
            request.session['email']=email
            print(request.session['email'])
            return redirect('index')
        else:
            return render(request,'verify.html',{'message':'Invalid OTP'})
    
    return render(request, 'verify.html')
        
def profile(request,user_id):
    if 'email' in request.session:
        email = request.session['email']
        user_id = user_id
        try:
            data = UserRegister.objects.get(email=email)
            user_posts=UserPost.objects.filter(user=data)
            user_about=AboutUser.objects.get(user=data)

            user_followers = len(FollowersCount.objects.filter(user=data.name))
            followers=[]
            for i in FollowersCount.objects.filter(user=data.name):
                followers.append(UserRegister.objects.get(name=i.follower))
            # print(user_followers)
            user_following = len(FollowersCount.objects.filter(follower=data.name))
            following=[]
            button_text=''
            for i in FollowersCount.objects.filter(follower=data.name):
                following.append(UserRegister.objects.get(name=i.user))
                if FollowersCount.objects.filter(follower=data.name, user=i.user).first():
                    button_text = 'Unfollow'
                else:
                    button_text = 'Follow'

            # print(len(user_posts))
            context = {
                'data': data,
                'user_posts': user_posts,
                'user_about':user_about,
                'user_id':user_id,
                'followers':followers,
                'following':following,
                'user_followers':user_followers,
                'user_following':user_following,
                'button_text': button_text,
            }
            print(user_about)
            return render(request, 'profile.html', context)
        except ObjectDoesNotExist:
            return render(request, 'index.html', {'message': 'User not found.'})
    else:
        return render(request, 'index.html')
    
    
from django.contrib import messages
def edit_profile(request):
    if 'email' in request.session:
        email = request.session['email']
        profile =UserRegister.objects.get(email=email)
        if request.method == 'POST':
            name = request.POST.get('name')
            uname = request.POST.get('uname')
            bio = request.POST.get('bio')
            phone = request.POST.get('phone')
            portfolio_img = request.FILES.get('portfolio_img')
            bg_img = request.FILES.get('bg_img')

            # Update the profile attributes
            # profile.name = name
            profile.uname = uname
            profile.bio = bio
            profile.phone = phone

            # Check if a new portfolio image is uploaded
            if portfolio_img:
                profile.portfolio_img = portfolio_img

            if bg_img:
                print("bg_img")
                profile.bg_img = bg_img
            # Save the changes
            profile.save()

            messages.success(request, 'Profile updated successfully.')
            return redirect('profile1',user_id=profile.id)

        context = {
            'name': profile.name,
            'uname': profile.uname,
            'bio': profile.bio,
            'phone': profile.phone,
            'portfolio_img': profile.portfolio_img,
            'bg_image': profile.bg_img,
        }
        return render(request, 'profile.html', context)
    else:
        return render(request, 'login.html')

def edit_about(request):
    if 'email' in request.session:
        email = request.session['email']
        user1 =UserRegister.objects.get(email=email)
        if AboutUser.objects.filter(user=user1).exists():
            user_about=AboutUser.objects.get(user=user1)
        else:
            user_about=AboutUser(user=user1)
            user_about.save()

        if request.method == 'POST':
            study = request.POST.get('study')
            work = request.POST.get('work')
            live = request.POST.get('live')
            from1 = request.POST.get('ufrom')

            # Update the profile attributes
            user_about.study = study
            user_about.work = work
            user_about.live = live
            user_about.ufrom = from1

            # Save the changes
            user_about.save()

            messages.success(request, 'Updated your About Section!')
            return redirect('/')

        context = {
            'study': user_about.study,
            'work': user_about.work,
            'live': user_about.live,
            'ufrom': user_about.ufrom,
        }
        return render(request, 'editabout.html', context)
    else:
        return render(request, 'login.html')

from django.db.models import Q
def searchview(request):
    # SEARCH POST
    # search_post = request.GET.get('search')
    # if search_post:
    #     posts = UserPost.objects.filter(Q(user__name__icontains=search_post)).distinct()
    # else:
    #     # If not searched, return default posts
    #     print("NOT FOUND")
    #     posts = UserPost.objects.all().order_by("-date_created")

    # email = request.session['email']
    # data = UserRegister.objects.get(email=email) 
    # about = AboutUser.objects.get(user=data)
    # context = {
    #     'all_posts': posts,
    #     'data': data,
    #     'user_about': about,
    # }
    # return render(request,'index.html',context)  

    # SEARCH PROFILE
    query = request.GET.get('q')
    # print(query)
    data=UserRegister.objects.get(email=request.session['email'])
    results_user=UserRegister.objects.filter(Q(name__icontains=query) | Q(uname__icontains=query)).first()
    results_about=AboutUser.objects.filter(user=results_user)
    results_post=UserPost.objects.filter(user=results_user)

    follower = data.name
    user = results_user.name

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(FollowersCount.objects.filter(user=user))
    followers=[]
    for i in FollowersCount.objects.filter(user=user):
        followers.append(UserRegister.objects.get(name=i.follower))
    # print(user_followers)
    user_following = len(FollowersCount.objects.filter(follower=user))
    following=[]
    for i in FollowersCount.objects.filter(follower=user):
        following.append(UserRegister.objects.get(name=i.user))
    context = {
        'results_user': results_user,
        'results_about': results_about,
        'results_post': results_post,
        'data': data,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
        'q': query,
        'followers': followers,
        'following': following,
    }
    return render(request,'searchprofile.html',context)

from django.shortcuts import reverse
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']
        query=''
        if request.POST.get('q'):
            query = request.POST.get('q')

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            # return redirect()
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            # return redirect(reverse('search_profile'))
        if(query):
            return redirect(reverse('search_profile') + '?search=&q=' + query)     
        return redirect('/')         
    return redirect('/')

def add_comment(request):
    if request.method == 'POST':
        user_data = UserRegister.objects.get(email=request.session['email'])
        text = request.POST.get('text')
        user = user_data
        post_user_id = request.POST.get('post')
        # h=UserPost.objects.
        post_user=UserPost.objects.get(id=post_user_id)
        new_comment = Comment.objects.create(user=user, text=text, post_user_id=post_user_id, post_user=post_user)
        new_comment.save()

        comments = Comment.objects.filter(post_user_id=post_user_id)
        content = {
            'comments': comments,
        }
        print(comments)
        
    return redirect('/')
    # return render(request, 'index.html', {'content': content})

def message(request):
    return render(request,'message.html')

def about(request):
    return render(request,'about.html')