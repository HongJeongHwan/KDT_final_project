from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from ..models import YQuestion
from ..forms import YQuestionForm
from .yolo_answer_views import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
from django.utils import timezone
from ultralytics import YOLO
import os

# 파일업로드시에 호출하는 함수
def yolo_predict_cli(filename, user):
    used_model = './media/yolo/models/robo_best_20240314_6class_per100.pt'
    # if os.path.exists('./yolo_media/models/robo_best_20240314_6class_per100.pt') == True:
    #     print('./yolo_media/models/robo_best_20240314_6class_per100.pt')

    # from_dir = './yolo_media/from'
    # source_file = './yolo_media/from/303_15_eb2afc35-8b99-4b1f-a746-19b70367ace5.JPG'
    source_file = './media/' + str(filename)
    # to_dir = './yolo_media/to'
    project_fld = './media/yolo/answer'
    # models의 upload_to에서 직접 지정하는 것으로 변경
    # name = timezone.now().strftime("%Y-%m-%d").replace('-','') + '_' +\
    #        str(user) + '_' + \
    #        str(filename) + '_'
    # name = timezone.now().strftime("%Y-%m-%d").replace('-','')
    # name = timezone.now().strftime("%Y%m%d%H%M%S")
    name = timezone.localtime(timezone.now()).strftime("%Y%m%d%H%M%S")

    # command = "yolo task=segment mode=predict model='./yolo_media/models/robo_best_20240314_6class_per100.pt' conf=0.15 source='./yolo_media/from/303_15_eb2afc35-8b99-4b1f-a746-19b70367ace5.JPG' project='./yolo_media/to' name='20240325' save=True"
    command = "yolo task=segment mode=predict \
        model='" + used_model + "' \
        conf=0.15 \
        source='" + source_file + "' \
        project='" + project_fld + "' \
        name='" + name + "' \
        save=True save_txt=True"
    os.system(command)
    is_success = True
    return name

# 일업로드시에 호출하는 함수
def yolo_predict(filename, user):

    used_model = YOLO('./media/yolo/models/robo_best_20240314_6class_per100.pt')  # pretrained YOLOv8n model
    source_file = './media/' + str(filename)
    project_fld = './media/yolo/answer'
    # models의 upload_to에서 직접 지정하는 것으로 변경
    name = timezone.localtime(timezone.now()).strftime("%Y%m%d%H%M%S")
    results = used_model.predict(source=source_file,
                                project=project_fld,
                                name=name,
                                save=True,
                                save_txt=True,
                                conf=0.15)

    return name



@login_required(login_url='common:login')
def yolo_question_create(request):
    # if request.FILES['imgfile'] is None:
    #     messages.error(request, '이미지 파일을 등록해야 합니다.')
    #     return redirect('yolo:yolo_index')

    if request.method == 'POST':
        form = YQuestionForm(request.POST, request.FILES)
        if form.is_valid():
            yolo_question = form.save(commit=False)
            yolo_question.imgfile = request.FILES['imgfile']
            yolo_question.author = request.user
            yolo_question.create_date = timezone.now()
            yolo_question.save()

            # Yolo Predict
            # name = yolo_predict_cli(yolo_question.imgfile, request.user)
            name = yolo_predict(yolo_question.imgfile, request.user)

            # 자동으로 답변 달아주기
            imgfile = str(yolo_question.imgfile)
            imgfile = imgfile[imgfile.rfind('/') + 1:]
            result = yolo_question.imgfile
            yolo_answer_create(request, yolo_question.id, 'yolo/answer/' + name + '/' + imgfile, result)

            return redirect('yolo:yolo_index')
        else:
            messages.error(request, '이미지 파일을 등록해야 합니다.')
            return redirect('yolo:yolo_detail', yolo_question_id=yolo_question_id)
        # form = YQuestion(
        #     subject=request.POST['subject'],
        #     content = request.POST['content'],
        #     imgfile = request.FILES['imgfile'],
        #     author = request.user,
        #     create_date = timezone.now(),
        # )
        # form.save()
        return redirect('yolo:yolo_index')
    else:
        form = YQuestionForm()
    context = {'form': form}
    return render(request, 'yolo/yolo_question_form.html', context)

@login_required(login_url='common:login')
def yolo_question_modify(request, yolo_question_id):
    yolo_question = get_object_or_404(YQuestion, pk=yolo_question_id)

    if request.user != yolo_question.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('yolo:yolo_detail', yolo_question_id=yolo_question_id)

    if request.method == "POST":
        form = YQuestionForm(request.POST, instance=yolo_question)
        if form.is_valid():
            yolo_question = form.save(commit=False)
            yolo_question.imgfile = request.FILES['imgfile']
            yolo_question.author = request.user
            yolo_question.modify_date = timezone.now()
            yolo_question.save()
            return redirect('yolo:yolo_detail', yolo_question_id=yolo_question.id)
    else:
        form = YQuestionForm(instance=yolo_question)

    context = {'form': form}
    return render(request, 'yolo/yolo_question_form.html', context)

@login_required(login_url='common:login')
def yolo_question_delete(request, yolo_question_id):
    yolo_question = get_object_or_404(YQuestion, pk=yolo_question_id)
    if request.user != yolo_question.author:
        messages.error(request, '삭제권한이 없습니다.')
        return redirect('yolo:yolo_detail', yolo_question_id=yolo_question.id)
    yolo_question.delete()
    return redirect('yolo:yolo_index')
