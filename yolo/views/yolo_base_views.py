from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from ..models import YQuestion
import logging
loger = logging.getLogger('yolo')

# Create your views here.
def yolo_index(request):
    # loger.info("INFO 레벨로 출력")
    # 입력인자
    page = request.GET.get('page', 1)
    kw = request.GET.get('kw', '')
    so = request.GET.get('so', 'recent')
    # 정렬
    if so == 'recommend':
        yolo_question_list = (YQuestion.objects.annotate(num_voter=Count('voter'))
                              .order_by('-num_voter', '-create_date'))
    elif so == 'popular':
        yolo_question_list = (YQuestion.objects.annotate(num_answer=Count('yanswer'))
                              .order_by('-num_answer', '-create_date'))
    else:   # recent
        yolo_question_list = YQuestion.objects.order_by('-create_date')
    # 조회
    # question_list = Question.objects.order_by('-create_date')
    if kw:
        yolo_question_list = yolo_question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(yanswer__author__username__icontains=kw)
        ).distinct()

    # 페이징 처리
    paginator = Paginator(yolo_question_list, 10)
    page_obj = paginator.get_page(page)

    context = {'yolo_question_list': page_obj, 'page': page, 'kw': kw, 'so': so}
    return render(request, 'yolo/yolo_question_list.html', context)

def yolo_detail(request, yolo_question_id):
    yolo_question = get_object_or_404(YQuestion, pk=yolo_question_id)
    context = {'yolo_question':yolo_question}
    return render(request, 'yolo/yolo_question_detail.html', context)
