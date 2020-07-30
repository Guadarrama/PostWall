from django.db import models

# Create your models here.

class userManager(models.Manager):
    def registerValidator(self, postData):
        errors={}

        if len(postData['fname']) < 2:
            errors['fname'] = 'first name must be at least 2 characters'
        if len(postData['lname']) < 2:
            errors['lname'] = 'last name must be at least 2 characters'

        if postData['password'] != postData['pwconfirm']:
            errors['password'] = 'passwords don`t match!'
        if len(postData['password']) < 8:
            errors['password2'] = 'password is too short!'
        emailsInDatabase = User.objects.filter(email = postData['email'])
        if len(emailsInDatabase) > 0:
            errors['email'] = 'This email already exists!'

        return errors
    
    def loginValidator(self, postData):
        errors={}

        if len(postData['logInEmail']) < 2:
            errors['logInEmail'] = 'email does not exist'
        if len(postData['logInPassword']) < 8:
            errors['logInPassword'] = 'password does not exist'
            
        return errors
    
    def messageValidator(self, postData):
        errors={}

        if len(postData['message']) < 1:
            errors['message'] = 'enter message!'
        return errors

    def commentValidator(self, postData):
        errors={}

        if len(postData['comment']) < 1:
            errors['comment'] = 'enter comment!'
        return errors
        



class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birthday = models.DateTimeField(null = True)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = userManager()

class Message(models.Model):
    message = models.TextField()
    user = models.ForeignKey(User, related_name="messages", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    
    this_comment = models.TextField()

    user = models.ForeignKey(User, related_name="comments", on_delete = models.CASCADE)
    message = models.ForeignKey(Message, related_name="reply", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)