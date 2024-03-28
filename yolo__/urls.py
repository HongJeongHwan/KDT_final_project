from django.urls import path
from .views import yolo_base_views, yolo_question_views, yolo_answer_views, yolo_comment_views, yolo_vote_views
# from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'yolo'

urlpatterns = [
    # path('', views.index, name='index'),
    # base_views.py
    path('', yolo_base_views.yolo_index, name='yolo_index'),
    path('<int:yolo_question_id>/', yolo_base_views.yolo_detail, name='yolo_detail'),
    # question_views.py
    path('question/create/', yolo_question_views.yolo_question_create, name='yolo_question_create'),
    path('question/modify/<int:yolo_question_id>/', yolo_question_views.yolo_question_modify, name='yolo_question_modify'),
    path('question/delete/<int:yolo_question_id>/', yolo_question_views.yolo_question_delete, name='yolo_question_delete'),
    # answer_views.py
    path('answer/create/<int:yolo_question_id>/', yolo_answer_views.yolo_answer_create, name='yolo_answer_create'),
    path('answer/modify/<int:yolo_answer_id>/', yolo_answer_views.yolo_answer_modify, name='yolo_answer_modify'),
    path('answer/delete/<int:yolo_answer_id>/', yolo_answer_views.yolo_answer_delete, name='yolo_answer_delete'),
    # comment_views.py
    path('comment/create/question/<int:yolo_question_id>/', yolo_comment_views.yolo_comment_create_question, name='yolo_comment_create_question'),
    path('comment/modify/question/<int:yolo_comment_id>/', yolo_comment_views.yolo_comment_modify_question, name='yolo_comment_modify_question'),
    path('comment/delete/question/<int:yolo_comment_id>/', yolo_comment_views.yolo_comment_delete_question, name='yolo_comment_delete_question'),
    path('comment/create/answer/<int:yolo_answer_id>/', yolo_comment_views.yolo_comment_create_answer, name='yolo_comment_create_answer'),
    path('comment/modify/answer/<int:yolo_comment_id>/', yolo_comment_views.yolo_comment_modify_answer, name='yolo_comment_modify_answer'),
    path('comment/delete/answer/<int:yolo_comment_id>/', yolo_comment_views.yolo_comment_delete_answer, name='yolo_comment_delete_answer'),
    # vote_views.py
    path('vote/question/<int:yolo_question_id>/', yolo_vote_views.yolo_vote_question, name='yolo_vote_question'),
    path('vote/answer/<int:yolo_answer_id>/', yolo_vote_views.yolo_vote_answer, name='yolo_vote_answer'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)