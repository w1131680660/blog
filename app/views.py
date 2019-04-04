from django.shortcuts import render
from  django.db.models import Count ,F
from django.contrib import auth
from django.http import JsonResponse,HttpResponse
from app.myform import *
# Create your views here.
from app.geetest import GeetestLib
import os,json
from blog import settings
from django.contrib.auth.decorators import login_required
from bs4 import BeautifulSoup

pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"
mobile_geetest_id = "7c25da6fe21944cfe507d2f9876775a9"
mobile_geetest_key = "f5883f4ee3bd4fa8caec67941de1b903"


def main(request):
    name = request.user
    article_obj = Article.objects.values("user__username","category__title" ,"title", "create_time","desc","up_count")
    category_obj = Category.objects.values("title",)
    if name == "AnonymousUser":
        name=""
    return render(request, 'main.html',locals())


def not_fount(request):
    return render(request,"no_found.html")


def pcgetcaptcha(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)


def login(request):
    if request.is_ajax():
        response = {"user": None, "msg": None}
        username = request.POST.get("username")
        password = request.POST.get("password")
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]

        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        if result:
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                response["user"] = user.username
            else:
                response["msg"] = "用户密码错误" if username and password else "用户密码不能为空"

        return JsonResponse(response)
    return render(request, 'login.html')


def register(request):
    if request.is_ajax():
        form = UserForm(request.POST)
        response = {"user": None, "msg": None}
        avatar_obj = request.FILES.get("avatar")
        if not avatar_obj:avatar_obj ="/avatars/default.jpg"
        if form.is_valid():
            response["user"] = request.POST.get("user")
            user = form.cleaned_data.get("user")
            pwd = form.cleaned_data.get("pwd")
            email = form.cleaned_data.get("email")
            phone = form.cleaned_data.get("telephone")
            head_photo = request.FILES.get("avatar")
            Blog.objects.create(title=user)
            nid = Blog.objects.filter(title=user).values("nid").first()
            UserInfo.objects.create_user(username=user, password=pwd, email=email,telephone=phone,avatar=avatar_obj,
                                         blog_id=nid["nid"])
            response["user"] = user

        else:
            response["msg"] = form.errors  # 错误校检的字段信息
        return JsonResponse(response)
    form = UserForm()
    return render(request, 'register.html', locals())


def home_site(request,username, **kwargs):
    '''
        个人站点视图函数
    :param request:
    :param username:
    :return:
    '''

    ret = UserInfo.objects.filter(username=username).first()
    if not ret:
        return render(request, "no_found.html")
    else:

        blog_name = UserInfo.objects.filter(username=username).values("blog__title", "nid", "blog__nid").first()
        article_obj = Article.objects.filter(user=ret).values("user__username","nid","tags__title",
                                                                "title", "create_time",  "desc",
                                                        "up_count")
        """当前站点用户的分类以及文章数"""
        category = Category.objects.filter(blog__nid=blog_name["blog__nid"]).values("nid").annotate(
            num=Count("article__title")).values("title", "num")
        """当前站点用户的标签以及对于的文章数"""
        tag_obj = Tag.objects.filter(blog__nid=blog_name["blog__nid"]).values("nid").annotate(
            num=Count("article")).values("title", "num")
        """当前站点用户标签的每一个年月的文章表和文章数"""
        article_time_obj = Article.objects.extra(
            select={"create_time": "date_format(create_time,'%%Y-%%m-%%d')"}).values("create_time").annotate(
            num=Count("nid")).values("create_time", "num")

        if kwargs:
            condition = kwargs.get("condition")
            parm = kwargs.get("param")
            article_obj1 =Article.objects.filter(user_id=blog_name["nid"])
            if condition == "category":
                article_obj =article_obj.filter(category__title=parm).values("user__username","title", "create_time",
                                                                             "comment","nid",
                                                                                      "desc",
                                                                                      "up_count")

            elif condition == "tag":
                article_obj = article_obj.filter(tags__title=parm).values(
                    "user__username","nid",
                    "title", "create_time", "comment",
                    "desc",
                    "up_count")

            elif condition == "archive":
                year, month, day = parm.split("-")
                article_obj = article_obj.filter(create_time__year=year,create_time__month =month, create_time__day=day).values(
                    "user__username","nid",
                    "title", "create_time", "comment",
                    "desc",
                    "up_count")

            elif condition == "articles":
                article_obj = article_obj.filter(nid=parm).values("user__username","nid","title","create_time","content",
                                                                  "user__avatar","category__title","comment", "desc",
                                                                  "up_count","down_count","tags__title").first()

                comment_list = Comment.objects.filter(article_id=parm)
                return render(request,"personal_page.html",locals())

    return render(request,"home_site.html", locals())


def digg(request):
    if request.is_ajax:
        msg ={"num_msg":{"up_num":None,"down_num": None}, "error":None}
        article_id = json.loads(request.POST.get("article_id"))
        is_up = json.loads(request.POST.get("is_up"))
        user_id = request.user.pk
        staue_obj = ArticleUpDown.objects.filter(user_id=user_id,article_id=article_id,).first()
        if staue_obj:
            msg["error"] = "您已经点赞过了" if is_up else "您已经反对过了"
        else:
            ArticleUpDown.objects.create(user_id=user_id, is_up=is_up,article_id=article_id)
            querset = Article.objects.filter(pk=article_id)
            if is_up:
                querset.update(up_count=F("up_count")+1)
            else:
                querset.update(down_count=F("down_count")+1)
            msg["num_msg"]["up_num"] = querset.values("up_count").first()
            msg["num_msg"]["down_num"] = querset.values("down_count").first()

    return HttpResponse(JsonResponse(msg))


def comment(request):
    if request.is_ajax:
        msg ={"msg":None}
        article_id =request.POST.get("article_id")
        content = request.POST.get('content')
        pid = request.POST.get("pid")
        article_name = Article.objects.filter(nid=article_id).first()
        user_id =request.user.pk
        commmet_obj = Comment.objects.create(user_id=user_id, article_id=article_id,content=content,parent_comment_id=pid)
        Article.objects.filter(pk=article_id).update(comment_count=F("comment_count")+1)
        msg["create_time"] = commmet_obj.create_time.strftime("%Y-%m-%d %X")
        msg["username"] = request.user.username
        msg["content"] = content
        msg["partent_id"] = commmet_obj.parent_comment_id
        msg["comment_uer"] = str(commmet_obj.user)
        msg["nid"] = commmet_obj.nid
        if commmet_obj.parent_comment_id:
            msg["partent_username"] = commmet_obj.parent_comment.user.username
            msg["partent_content"] = commmet_obj.parent_comment.content

    return HttpResponse(JsonResponse(msg))


@login_required
def cn_backecd(request):
    username = request.user.username
    article_list = Article.objects.filter(user=request.user)
    return render(request, "backend.html", locals())


@login_required
def add_article(request):
    username =request.user.username
    return render(request,'add_article.html',locals())

@login_required
def create_article(request):
    msg ={"data":"123"}
    if request.is_ajax():
        title = request.POST.get("title")
        content = request.POST.get("content")
        soup = BeautifulSoup(content, "html.parser")
        tag = request.POST.get("tag")
        category = request.POST.get("category")

        blog_num = UserInfo.objects.filter(username=request.user).values("blog__nid").first()["blog__nid"]
        category_obj = Category.objects.filter(title=category,blog_id=blog_num).first()
        tag_obj = Tag.objects.filter(title=tag,blog_id=blog_num).first()
        for tag_num in soup.find_all():
            if tag_num.name == "script":
                tag_num.decompose()
        desc = soup.text[0:150] + "..."
        category_nid = category_obj.pk if category_obj else Category.objects.create(title=category,blog_id=blog_num).nid
        tag_id = tag_obj.pk if tag_obj else Tag.objects.create(title=tag, blog_id=blog_num).nid
        article_obj =Article.objects.create(title=title,content=str(soup), user=request.user, desc=desc,
                                            category_id=category_nid)
        Article2Tag.objects.create(article_id=article_obj.nid,tag_id=tag_id)
    return HttpResponse(JsonResponse(msg))

def logout(request):
    auth.logout(request)
    return render(request,'main.html')

@login_required
def del_article(request,article_id):
    username = request.user.username
    Article.objects.filter(nid=article_id).delete()
    article_list = Article.objects.filter(user=request.user)
    return render(request,"backend.html", locals())


@login_required
def editor_article(request):
    pass


def upload(request):

    img_obj = request.FILES.get("imgFile")
    path=os.path.join(settings.MEDIA_ROOT,'add_article', img_obj.name)
    with open(path,"wb") as f:
        for line in img_obj:
            f.write(line)
    response = {
        'error':0,
        'url':'/media/add_article/%s/'%img_obj.name,
    }
    return HttpResponse(JsonResponse(response))


def gooo(request,name):
    return render(request,"gogp.html")

def qq(request):
    return render(request,"gogp.html")

