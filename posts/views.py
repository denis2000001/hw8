from django.shortcuts import render, redirect, get_object_or_404
from posts.models import Post, Comment
from posts.forms import PostForms, CommentForms
from posts.constants import PAGINATION_LIMIT
from django.views.generic import ListView, CreateView, DetailView, UpdateView

def get_user_from_request(request):
    return request.user if not request.user.is_anonymous else None

class MainView(ListView):
    queryset = Post.objects.all()
    template_name = 'posts.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            'posts': self.queryset,
            'user': get_user_from_request(self.request)
        }

    def get(self, request, **kwargs):
        page = int(request.GET.get('page', 1))
        start_post = PAGINATION_LIMIT * page if page != 1 else 0
        end_post = start_post + PAGINATION_LIMIT
        max_page = len(self.queryset) / PAGINATION_LIMIT
        if max_page > round(max_page):
            max_page = round(max_page) + 1
        else:
            max_page = round(max_page)
        context = {
            'posts': self.queryset[start_post:end_post],
            "user": get_user_from_request(self.request),
            'pages': range(1, (self.queryset.__len__() // PAGINATION_LIMIT) + 1)
        }
        return render(request, self.template_name, context=context)
    # def get(self, request, **kwargs):
    #     page = int(request.GET.get('page', 1))
    #     start_post = (len(self.queryset) // ((len(self.queryset) // PAGINATION_LIMIT) + 1)) * page - 1 if page > 1 else 0
    #     end_posts = start_post + PAGINATION_LIMIT
    #     data = {
    #         "posts": self.queryset[start_post:end_posts],
    #         'user': get_user_from_request(request),
    #         'pages': range(1, (self.queryset.__len__() // PAGINATION_LIMIT) + 1)
    #     }
    #
    #     return render(request, self.template_name, context=data)

# def post_detail(request, id):
#     if request.method == 'GET':
#         post = Post.objects.get(id=id)
#         comments = Comment.objects.filter(post=post)
#         data = {
#             'post': post,
#             'comments': comments,
#             'comment_form': CommentForms,
#             'user': get_user_from_request(request)
#                 }
#         return render(request, 'detail.html', context=data)
#
#     if request.method == 'POST':
#         form = CommentForms(request.POST)
#         if form.is_valid():
#             Comment.objects.create(
#                 author=form.cleaned_data.get('author'),
#                 text=form.cleaned_data.get('text'),
#                 post_id=id
#             )
#             return redirect(f'/posts/{id}/')
#         else:
#             return render(request, 'detail.html', context={
#                 'comment_form': form,
#                 'user': get_user_from_request(request)
#             })

class PostDetailView(DetailView):
    queryset = Post.objects.all()
    context_object_name = 'post'
    template_name = 'detail.html'

class CreatePostView(ListView, CreateView):
    model = Post
    template_name = 'create_post.html'
    form_class = PostForms

    def get(self, request, **kwargs):
        if get_user_from_request(request):
            return render(request, self.template_name, context={
                'post_form': self.form_class,
            })
        return redirect('/')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            Post.objects.create(
                title=form.cleaned_data.get("title"),
                description=form.cleaned_data.get("description"),
                stars=form.cleaned_data.get("stars"),
                type=form.cleaned_data.get("type")
            )
            return redirect('/')
        else:
            return render(request, self.template_name, context={
                'post_form': form
            })

class EditPostView(ListView, CreateView):
    template_name = 'edit_post.html'
    queryset = Post.objects.all()
    form_class = PostForms

    def get(self, request, pk, *args):
        return render(request, self.template_name, context={
            'post_form': self.form_class,
            'pk': pk
        })

    def post(self, request, pk, **kwargs):
        form = self.form_class(request.POST)
        instance = get_object_or_404(Post, pk=pk)
        if form.is_valid():
            instance.title = form.cleaned_data.get('title')
            instance.description = form.cleaned_data.get('description')
            instance.stars = form.cleaned_data.get('stars')
            instance.type = form.cleaned_data.get('type')
            instance.save()
            return redirect('/')
        else:
            return render(request, self.template_name, context={
                'post_form': self.form_class,
                'pk': pk
            })