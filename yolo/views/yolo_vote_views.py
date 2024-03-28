from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from ..models import YQuestion, YAnswer

# Create your views here.
@login_required(login_url='common:login')
def yolo_vote_question(request, yolo_question_id):
    yolo_question = get_object_or_404(YQuestion, pk=yolo_question_id)
    if request.user == yolo_question.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다.')
    else:
        yolo_question.voter.add(request.user)
    return redirect('yolo:yolo_detail', yolo_question_id=yolo_question.id)

@login_required(login_url='common:login')
def yolo_vote_answer(request, yolo_answer_id):
    yolo_answer = get_object_or_404(YAnswer, pk=yolo_answer_id)
    if request.user == yolo_answer.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다.')
    else:
        yolo_answer.voter.add(request.user)
    return redirect('yolo:yolo_detail', yolo_question_id=yolo_answer.question.id)