from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from ..models import YQuestion, YAnswer, YComment
from ..forms import YCommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
@login_required(login_url='common:login')
def yolo_comment_create_question(request, yolo_question_id):
    yolo_question = get_object_or_404(YQuestion, pk=yolo_question_id)
    if request.method == "POST":
        form = YCommentForm(request.POST)
        if form.is_valid():
            yolo_comment = form.save(commit=False)
            yolo_comment.author = request.user
            yolo_comment.create_date = timezone.now()
            yolo_comment.question = yolo_question
            yolo_comment.save()
            return redirect('{}#yolo_comment_{}'.format(resolve_url('yolo:yolo_detail',
                yolo_question_id=yolo_comment.question.id), yolo_comment.id))
    else:
        form = YCommentForm()
    context = {'form': form}
    return render(request, 'yolo/yolo_comment_form.html', context)

@login_required(login_url='common:login')
def yolo_comment_modify_question(request, yolo_comment_id):
    yolo_comment = get_object_or_404(YComment, pk=yolo_comment_id)
    if request.user != yolo_comment.author:
        messages.error(request, '댓글수정권한이 없습니다.')
        return redirect('yolo:yolo_detail', yolo_question_id=yolo_comment.question.id)
    if request.method == 'POST':
        form = YCommentForm(request.POST, instance=yolo_comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('{}#yolo_comment_{}'.format(resolve_url('yolo:yolo_detail',
                yolo_question_id=yolo_comment.question.id), yolo_comment.id))
    else:
        form = YCommentForm(instance=yolo_comment)
    context = {'form': form}
    return render(request, 'yolo/yolo_comment_form.html', context)

@login_required(login_url='common:login')
def yolo_comment_delete_question(request, yolo_comment_id):
    yolo_comment = get_object_or_404(YComment, pk=yolo_comment_id)
    if request.user != yolo_comment.author:
        messages.error(request, '댓글삭제권한이 없습니다.')
        return redirect('yolo:yolo_detail', yolo_question_id=yolo_comment.question.id)
    else:
        yolo_comment.delete()
    return redirect('yolo:yolo_detail', yolo_question_id=yolo_comment.question.id)

@login_required(login_url='common:login')
def yolo_comment_create_answer(request, yolo_answer_id):
    """
    pybo 답글댓글등록
    """
    yolo_answer = get_object_or_404(YAnswer, pk=yolo_answer_id)
    if request.method == "POST":
        form = YCommentForm(request.POST)
        if form.is_valid():
            yolo_comment = form.save(commit=False)
            yolo_comment.author = request.user
            yolo_comment.create_date = timezone.now()
            yolo_comment.answer = yolo_answer
            yolo_comment.save()
            return redirect('{}#yolo_comment_{}'.format(resolve_url('yolo:yolo_detail',
                yolo_question_id=yolo_comment.answer.question.id), yolo_comment.id))
    else:
        form = YCommentForm()
    context = {'form': form}
    return render(request, 'yolo/yolo_comment_form.html', context)


@login_required(login_url='common:login')
def yolo_comment_modify_answer(request, yolo_comment_id):
    yolo_comment = get_object_or_404(YComment, pk=yolo_comment_id)
    if request.user != yolo_comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('yolo:yolo_detail', yolo_question_id=yolo_comment.answer.question.id)

    if request.method == "POST":
        form = YCommentForm(request.POST, instance=yolo_comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('{}#yolo_comment_{}'.format(resolve_url('yolo:yolo_detail',
                yolo_question_id=yolo_comment.answer.question.id), yolo_comment.id))
    else:
        form = YCommentForm(instance=yolo_comment)
    context = {'form': form}
    return render(request, 'yolo/yolo_comment_form.html', context)

@login_required(login_url='common:login')
def yolo_comment_delete_answer(request, yolo_comment_id):
    yolo_comment = get_object_or_404(YComment, pk=yolo_comment_id)
    if request.user != yolo_comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('yolo:yolo_detail', yolo_question_id=yolo_comment.answer.question.id)
    else:
        yolo_comment.delete()
    return redirect('yolo:yolo_detail', yolo_question_id=yolo_comment.answer.question.id)
