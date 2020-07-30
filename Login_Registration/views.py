from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.

def index(request):

    return render(request, 'index.html')


def register(request):

    errors = User.objects.registerValidator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            print("ERROR MESSAGE")
        return redirect('/')

    else:

        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        print(pw_hash)

        User.objects.create(password = pw_hash.decode(), birthday = request.POST['birthday'], first_name = request.POST['fname'], last_name = request.POST['lname'], email = request.POST['email'])

        # loggedIn = User.objects.get(email = request.POST['logInEmail'])
        # request.session['LIUFName'] = loggedIn.first_name
        request.session['LoggedInEmail'] = request.POST['email']

        return redirect('/success')

def login(request):

    errors = User.objects.loginValidator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            print("ERROR MESSAGE")
        return redirect('/')
    else:  
        user = User.objects.filter(email = request.POST['logInEmail'])

        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['logInPassword'].encode(), logged_user.password.encode()):
                request.session['userid'] = logged_user.id 

                loggedIn = User.objects.get(email = request.POST['logInEmail'])
                request.session['LoggedInEmail'] = loggedIn.email

                return redirect ('/success')
        return redirect('/')

def success(request):

    if 'LoggedInEmail' not in request.session:
        return redirect('/') 
    loggedIn = User.objects.get(email = request.session['LoggedInEmail'])
    thisUser = loggedIn.first_name
    thisUser_id = loggedIn.id

    # messages = Message.objects.all(user = loggedIn)
    # messages = loggedIn.messages.all()
    messages = Message.objects.all()
    comments = Comment.objects.all()
    # some_message = Message.objects.get(id=1)
    # print(some_message.reply.all())
    


    context = {
        'thisUser_id' : thisUser_id,
        'first_name': thisUser,
        'all_messages' : messages,
        'comments' : comments
    }

    return render(request, 'success.html', context)



def logout(request):

    request.session.clear()

    return redirect('/')



def post_message(request):

    errors = User.objects.messageValidator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            print("ERROR MESSAGE")
        return redirect('/success')

    else:
            
        loggedIn = User.objects.get(email = request.session['LoggedInEmail'])
        # thisUser = loggedIn.id
        messagePosted = request.POST['message']
        print(messagePosted)
        # print(thisUser)
        Message.objects.create(message = messagePosted, user = loggedIn)

        return redirect('/success')


def post_comment(request):

    errors = User.objects.commentValidator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            print("ERROR MESSAGE")
        return redirect('/success')
    else:
        print('POSTING A COMMENT')
        loggedIn = User.objects.get(email = request.session['LoggedInEmail'])
        # thisUser = loggedIn.id
        commentPosted = request.POST['comment']
        # print(commentPosted)
        # print(thisUser)
        messageId = request.POST['message_id']
        # print(messageId)
        repliedTo = Message.objects.get(id = messageId)

        Comment.objects.create(user = loggedIn, message = repliedTo, this_comment = commentPosted)

        return redirect('/success')


def delete_message(request):

    if User.objects.get(email = request.session['LoggedInEmail']) == User.objects.get(id = request.POST['user_id']):
        this_message = Message.objects.get(id = request.POST['message_id'])
        this_message.delete()
        # this_user = User.objects.get(email = request.session['loggedInEmail'])
        # print(request.POST['user_id'])
        # print(request.session['LoggedInEmail'])
        # print(this_user.first_name)

    return redirect('/success')

def delete_comment(request):

    if User.objects.get(email = request.session['LoggedInEmail']) == User.objects.get(id = request.POST['user_id']):
        this_comment = Comment.objects.get(id = request.POST['comment_id'])
        this_comment.delete()

    return redirect('/success')