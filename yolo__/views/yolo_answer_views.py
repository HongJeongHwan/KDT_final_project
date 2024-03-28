from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from ..models import YQuestion, YAnswer
from ..forms import YAnswerForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

@login_required(login_url='common:login')
def yolo_answer_create(request, yolo_question_id, yolo_predict_file, yolo_result):
    yolo_question = get_object_or_404(YQuestion, pk=yolo_question_id)
    if request.method == 'POST':
        form = YAnswerForm(request.POST)
        if form.is_valid():
            yolo_answer = form.save(commit=False)
            yolo_answer.content = yolo_result
            yolo_answer.imgfile = yolo_predict_file
            yolo_answer.author = request.user
            yolo_answer.create_date = timezone.now()
            yolo_answer.question = yolo_question
            yolo_answer.save()
            return redirect('{}#yolo_answer_{}'.format(
                resolve_url('yolo:yolo_detail', yolo_question_id=yolo_question.id), yolo_answer.id))
    else:
        form = YAnswerForm()
    context = {'yolo_question': yolo_question, 'form': form}
    return render(request, 'yolo/yolo_question_detail.html', context)

@login_required(login_url='common:login')
def yolo_answer_modify(request, yolo_answer_id):
    yolo_answer = get_object_or_404(YAnswer, pk=yolo_answer_id)
    if request.user != yolo_answer.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('yolo:yolo_detail', yolo_question_id=yolo_answer.question.id)
    if request.method == 'POST':
        form = YAnswerForm(request.POST, instance=yolo_answer)
        if form.is_valid():
            yolo_answer = form.save(commit=False)
            yolo_answer.author = request.user
            yolo_answer.modify_date = timezone.now()
            yolo_answer.save()
            return redirect('{}#yolo_answer_{}'.format(
                resolve_url('yolo:yolo_detail', yolo_question_id=yolo_answer.question.id), yolo_answer.id))
    else:
        form = YAnswerForm(instance=yolo_answer)
    context = {'yolo_answer': yolo_answer, 'form': form}
    return render(request, 'yolo/yolo_answer_form.html', context)

@login_required(login_url='common:login')
def yolo_answer_delete(request, yolo_answer_id):
    yolo_answer = get_object_or_404(YAnswer, pk=yolo_answer_id)
    if request.user != yolo_answer.author:
        messages.error(request, '삭제권한이 없습니다.')
    else:
        messages.error(request, '삭제권한이 있습니다.')
        yolo_answer.delete()
    return redirect('yolo:yolo_detail', yolo_question_id=yolo_answer.question.id)
