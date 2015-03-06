from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.core import serializers
from django.core.urlresolvers import reverse


# Django auth
from django.contrib.auth.decorators import login_required

# Handles login
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

# Emain confirmation
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

# django transactions
from django.db import transaction

## Other usefule django imports
from django.utils import timezone

## Social network imports 
from socialnetwork.forms import RegistrationForm, EditForm
from socialnetwork.models import *

## To handle json
import json
from datetime import tzinfo, timedelta

## import the S3 functions
from socialnetwork.s3 import s3_upload

## Heroku imports
import sendgrid
import os

# Create your views here.
@login_required
def frontPage(request, inheritedErrors=[]):
    context = {}
    errors = inheritedErrors
    context['errors'] = errors
    index = 'socialnetwork/frontPage.html'

    squeaks = Posts.objects.all().order_by('-dateTime')
    which_squeaks = Posts.objects.values_list('id', flat=True).distinct()

    ## Does a segmented query only pulling comments to single post and appending them to context dict
    # for squeak_id in which_squeaks:
    #     if Comments.objects.filter(postID=squeak_id).exists():
    #         comments = Comments.objects.filter(postID=squeak_id).order_by('postID')
    #         keyname = "comment" + str(squeak_id)
    #         context[keyname] = comments
    comments = Comments.objects.all().order_by('postID')
    context['comments'] = comments

    ## Add's posts to response
    context['squeaks'] = squeaks
    context['logged_in_user'] = str(request.user)

    print context

    return render(request,index,context)

@login_required
@transaction.atomic
def profile(request, account, inheritedErrors=[]):
    context = {}
    errors = inheritedErrors
    
    print account
    context['errors'] = errors
    profile = 'socialnetwork/profile.html'

    if not User.objects.filter(username=account).exists():
        errors.append("Well this is weird, " + account + " is not a registered username.")
        return frontPage(request, errors)

    accountInfo = Profiles.objects.get(username=account)
    print accountInfo

    context['firstname'] = accountInfo.firstname
    context['lastname'] = accountInfo.lastname
    context['age'] = accountInfo.age
    context['bio'] = accountInfo.bio
    context['user'] = account
    context['picture'] = accountInfo.picture
    context['logged_in_user'] = str(request.user)

    ## Get all squeaks for user
    squeaks = Posts.objects.filter(user=account).order_by('-dateTime')
    context['squeaks'] = squeaks

    ## Get all comments
    comments = Comments.objects.all().order_by('postID')
    context['comments'] = comments
    
    ## Get List of accounts followed by user
    following = Follow.objects.filter(user=account)
    context['following'] = following
    print context

    # Get following squeaks
    following_squeaks = Posts.objects.filter(user__in=following.values('following')).order_by('-dateTime')
    context['following_squeaks'] = following_squeaks

    # Checks to see if follow already exists
    if Follow.objects.filter(user=request.user,following=account).exists():
        context['current_follow'] = True

    return render(request,profile,context)

@login_required
@transaction.atomic
def squeak(request):
    context = {}
    index = 'socialnetwork/frontPage.html'
    errors = []
    context['errors'] = errors

    squeak = request.POST['squeak']

    if not 'squeak' in request.POST or len(squeak) == 0:
        errors.append("Squeak louder! You didn't type anything in the box above.")
    if len(squeak) > 160:
        errors.append("How did you do that? Sneaky you tried to post a squeak larger than 160 characters. Our eyes will be on you!")
    if errors:
        return frontPage(request,errors)

    ## Create Profile object since user is a many-to-one field.
    user_profile = Profiles.objects.get(username=request.user)
    new_post = Posts(dateTime=timezone.now(),user=user_profile,content=request.POST['squeak'])

    new_post.save()

    return redirect('/frontPage')


@login_required
@transaction.atomic
def follow(request, account):
    context = {}
    errors = []
    profile = 'socialnetwork/profile.html'
    print account

    # Returns request if not a POST
    if request.method == 'GET':
        return render(request, 'socialnetwork/profile.html', context)

    ## Create Profile object since user is a many-to-one field.
    username = Profiles.objects.get(username=request.user)
    follow_user = Profiles.objects.get(username=account)

    # Checks to see if follow already exists
    if Follow.objects.filter(user=username,following=account).exists():
        errors.append("Already following")
        #return profile(request, account)
    else:
        new_follow = Follow(user=username,following=follow_user)
        new_follow.save()

    return redirect('/account/' + account)
    #return render(request,profile,context)

@login_required
@transaction.atomic
def edit_profile(request):
    context = {}
    
    # Reutrns form fields with old data prefilled
    if request.method == 'GET':
        user_profile = get_object_or_404(Profiles, username=request.user)
        print user_profile.picture
        context['form'] = EditForm(instance=user_profile)
        #print context['form']
        return render(request, 'socialnetwork/edit_profile.html', context)

    # select record to update
    profile = Profiles.objects.get(username=request.user)
    oldPic = str(profile.picture)
    form = EditForm(request.POST, request.FILES)

    # Checks whether form is valid
    if not form.is_valid():
        print "hi"
        context = { 'entry': profile, 'form': form }
        return render(request, 'socialnetwork/edit_profile.html', context)
    else:
        cd = form.cleaned_data
        profile.firstname = cd.get('firstname')
        profile.lastname = cd.get('lastname')
        profile.age = cd.get('age')
        profile.bio = cd.get('bio')

        if form.cleaned_data['picture_file']:
            print str(form.cleaned_data['picture_file'])
            url = s3_upload(form.cleaned_data['picture_file'], str(request.user))
            profile.picture = url
        profile.save()

    return redirect('/account/' + str(request.user))


@login_required
@transaction.atomic
def get_photo(request, account):
    item = get_object_or_404(Profiles, username=account)
    print item
    if not item.picture:
        raise Http404
    return HttpResponse(item.picture, content_type=item.image_type)


@transaction.atomic
def register(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'socialnetwork/register.html', context)

    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validates form.
    if not form.is_valid():
        return render(request, 'socialnetwork/register.html', context)

    # Adds account to User's model
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password1'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'],
                                        email=form.cleaned_data['email'])
    ## Make the user in active so they can't log in until they click on the email
    new_user.is_active = False
    new_user.save()

    new_profile = Profiles(username=form.cleaned_data['username'],
                            firstname=form.cleaned_data['first_name'],
                            lastname=form.cleaned_data['last_name'])
    new_profile.save()

    ## Handles creating/sending the email 
    ## One time token to send email
    token = default_token_generator.make_token(new_user)

    ## Creats email
    email_body = """
    Welcome to Squeak! Please click the link below to
    verify your email address and complete the registration of your account:
    
    http://%s%s
    """ % (request.get_host(), reverse('confirm', args=(new_user.username, token)))

    ## Sends email
    # send_mail(subject="Verify your email address", message= email_body,
    #     from_email="squeakconfirmation@gmail.com", recipient_list=[new_user.email])
    sg = sendgrid.SendGridClient(os.environ.get('SG-user'),os.environ.get('SG-password'))
    message = sendgrid.Mail()
    message.add_to(new_user.email)
    message.set_subject('Confirm your email address')
    message.set_text(email_body)
    message.set_from('squeak@noreply')
    status, msg = sg.send(message)
    # Logs in the new user and redirects to his/her todo list
    # new_user = authenticate(username=form.cleaned_data['username'],
    # password=form.cleaned_data['password1'])
    # login(request, new_user)

    # return redirect('/frontPage')
    context['email'] = form.cleaned_data['email']
    return render(request, 'socialnetwork/needs_confirmed.html', context)


def confirm_registration(request, username, token):
    user = get_object_or_404(User, username=username)

    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404

    # Otherwise token was valid, activate the user.
    user.is_active = True
    user.save()

    return render(request, 'socialnetwork/confirmed.html', {})



def get_posts_json(request):
    ## number of posts on user's page
    num_posts = int(request.GET.get("num_posts"))

    ## number of posts on backend
    num_server_posts = Posts.objects.all().order_by('-dateTime').count()

    ## if the posts on the page matches the posts on server then do nothing
    if num_posts == num_server_posts:
        print "No need to update page"
        posts = ""
        response_text = serializers.serialize('json', posts)
    else:
        ## When there is new post, calculate which posts are needed and get it
        posts_needed = range(num_posts, num_server_posts, 1)
        posts_needed = [x+1 for x in posts_needed]
        print posts_needed
        posts = Posts.objects.filter(pk__in=posts_needed).order_by('-dateTime')

        ## jsonify the queryset before we send it off.
        response_text = serializers.serialize('json', posts)

        # ## load json as dict so I can add additional fields
        rt = json.loads(response_text)
        for i in range(len(rt)):
            ## add picture path to response
            rt[i]['fields']['user_profile_image'] = str(posts[i].user.picture)

            ## used to format datetime to be readable
            dt = posts[i].dateTime - timedelta(hours=5)
            date = dt.strftime("%b. %w, %Y, ")
            hour24 = dt.strftime("%H")
            if int(hour24) < 12:
                ampm = " a.m."
            else:
                ampm = " p.m."
            hour12 = dt.strftime("%I:")
            hour = list(hour12)
            if "0" == hour[0]:
                hour[0] = ""
            hour = "".join(hour)
            minute = dt.strftime("%M")
            rt[i]['fields']['dateTime'] = date + hour + minute + ampm


            response_text = json.dumps(rt)

    return HttpResponse(response_text, content_type='application/json')

def get_posts_xml(request):
    context = { 'squeaks': Posts.objects.all().order_by('-dateTime') }
    return render(request, 'socialnetwork/items.xml', context, content_type='application/xml')

@login_required
def comment(request,post_id):
    response_text = {}
    errors = []

    comment = request.POST.get('comment')
    user_profile = request.user

    print comment
    print str(comment)
    print len(str(comment))
    print post_id

    if len(str(comment)) == 0:
        print "nothing said..."
        errors.append("You gotta type something in there dude/dudette!")
    if len(str(comment)) > 160:
        errors.append("How did you do that? Sneaky you tried to post a squeak larger than 160 characters. Our eyes will be on you!")
    if errors:
        print "errors sent..."
        return frontPage(request,errors)

    print "check..."
    ## Create Profile object since user is a many-to-one field.
    user_profile = Profiles.objects.get(username=request.user)
    new_comment = Comments(dateTime=timezone.now(),user=user_profile,comment=str(comment),postID=post_id)
    new_comment.save()

    response_text['user'] = new_comment.user.username
    response_text['user_profile_image'] = str(new_comment.user.picture)
    response_text['comment'] = new_comment.comment
    response_text['post_id'] = new_comment.postID

    ## used to format datetime to be readable
    dt = new_comment.dateTime - timedelta(hours=5)
    date = dt.strftime("%b. %w, %Y, ")
    hour24 = dt.strftime("%H")
    if int(hour24) < 12:
        ampm = " a.m."
    else:
        ampm = " p.m."
    hour12 = dt.strftime("%I:")
    hour = list(hour12)
    if "0" == hour[0]:
        hour[0] = ""
    hour = "".join(hour)
    minute = dt.strftime("%M")
    response_text['dateTime'] = date + hour + minute + ampm

    print str(new_comment.dateTime)
    
    return HttpResponse(json.dumps(response_text),content_type="application/json")

