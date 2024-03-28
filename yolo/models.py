from django.db import models
from django.contrib.auth.models import User

class YQuestion(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    imgfile = models.ImageField(null=True, upload_to="yolo/question/%Y%m%d", blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question_yolo')
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question_yolo')
    def __str__(self):
        return self.subject

class YAnswer(models.Model):
    question = models.ForeignKey(YQuestion, on_delete=models.CASCADE)
    content = models.TextField()
    imgfile = models.ImageField(null=True, upload_to="", blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer_yolo')
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer_yolo')

class YComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='voter_comment_yolo')
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(YQuestion, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(YAnswer, null=True,blank=True,on_delete=models.CASCADE)
