from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView

from .models import ScorePost, Category
from .forms import ScorePostForm





# 商品一覧ビュー (全ての商品を表示)
class AllScoreView(ListView):
    model = ScorePost
    template_name = 'all_score.html'  # 使用するテンプレート
    context_object_name = 'score_posts'  # テンプレートで使用する変数名
    ordering = ['condition']  # 学生番号順で並び替え
    paginate_by = 9  # 1ページに9件表示

    def get_queryset(self):
        return ScorePost.objects.all().order_by('condition')  # 学生番号順に並び替え

    


class JapanScoreView(ListView):
    model = ScorePost
    template_name = 'japan.html'  # 使用するテンプレート
    context_object_name = 'score_posts'  # テンプレートで使用する変数名
    paginate_by = 9  # 1ページに9件表示

    def get_queryset(self):
        # 国語の成績をフィルタリングし、点数（price）の降順で並べ替え
        return ScorePost.objects.filter(day='国語').order_by('-price')
    

class EnglishScoreView(ListView):
    model = ScorePost
    template_name = 'english.html'  # 使用するテンプレート
    context_object_name = 'score_posts'  # テンプレートで使用する変数名
    paginate_by = 9  # 1ページに9件表示

    def get_queryset(self):
        # 英語の成績をフィルタリングし、点数（price）の降順で並べ替え
        return ScorePost.objects.filter(day='英語').order_by('-price')


class MathScoreView(ListView):
    model = ScorePost
    template_name = 'math.html'  # 使用するテンプレート
    context_object_name = 'score_posts'  # テンプレートで使用する変数名
    paginate_by = 9  # 1ページに9件表示

    def get_queryset(self):
        # 数学の成績をフィルタリングし、点数（price）の降順で並べ替え
        return ScorePost.objects.filter(day='数学').order_by('-price')



# 商品作成ビュー (商品を作成)
class CreateScoreView(CreateView):
    form_class = ScorePostForm
    template_name = 'buy.html'  # 商品作成フォームのテンプレート
    success_url = reverse_lazy('scoreapp:all_score')  # 商品作成後の遷移先

    def form_valid(self, form):
        postdata = form.save(commit=False)
        postdata.user = self.request.user  # 現在のユーザーを設定
        postdata.save()
        return super().form_valid(form)




# 成功メッセージを表示するためのテンプレートビュー
class PostDoneView(TemplateView):
    template_name = 'all_score.html'  # 商品作成後の成功ページ

# インデックスページのビュー (全ての商品を表示)
class IndexView(ListView):
    model = ScorePost
    template_name = 'index.html'
    context_object_name = 'score_posts'
    queryset = ScorePost.objects.order_by('-posted_at')
    paginate_by = 9

# フォームを使って商品を作成するための汎用ビュー
def your_view(request):
    if request.method == 'POST':
        form = ScorePostForm(request.POST, request.FILES)  # request.FILESを渡して画像を受け取る
        if form.is_valid():
            form.save()  # フォームを保存して新しい商品を作成
            return redirect('success_url')  # 送信後のリダイレクト先
    else:
        form = ScorePostForm()
    
    return render(request, 'your_template.html', {'form': form})
