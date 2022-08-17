from django.core.paginator import Paginator
from django.http.response import Http404
from django.shortcuts import render, redirect
from .models import Board
from accounts.models import Member
from .forms import BoardForm

# Create your views here.
def board_list(request) :
    all_boards  = Board.objects.all().order_by('-id')
    page        = int(request.GET.get('p', 1))
    # p라는 값으로 받을거고, 없으면 첫번째 페이지로
    pagenator   = Paginator(all_boards, 10)
    # Paginator 함수를 적용하는데, 첫번째 인자는 위에 변수인 전체 오브젝트, 2번째 인자는
    # 한 페이지당 오브젝트 10개씩 나오게 설정
    boards      = pagenator.get_page(page)
    return render(request, 'board/board_list.html', {"boards" : boards})


def board_write(request):

    

    if request.method == "board":
        form = BoardForm(request.board)

        if form.is_valid():
            # form의 모든 validators 호출 유효성 검증 수행
            user = request.user
            member = Member.objects.get(user=user)
            
            board = Board()
            board.title     = form.cleaned_data['title']
            board.contents  = form.cleaned_data['contents']
            # 검증에 성공한 값들은 사전타입으로 제공 (form.cleaned_data)
            # 검증에 실패시 form.error 에 오류 정보를 저장
            
            board.writer    = user
            board.save()

            return redirect('/board/list/')

    else:
        form = BoardForm()

    return render(request, 'board/board_write.html', {'form': form})

def board_detail(request, pk):
    try:
        board = Board.objects.get(pk=pk)
        all_comments = board.comments.all().order_by('-created_at')
    except Board.DoesNotExist:
        raise Http404('게시글을 찾을 수 없습니다')

    return render(request, 'board/board_detail.html', {'board':board,'comments':all_comments})



