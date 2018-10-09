from django.shortcuts import render,HttpResponse,redirect
from django.contrib import auth
from django.http import JsonResponse
from blogs.codeimg import get_valid_code_img
from blogs.myforms import UserForms
from django.db.models import F,Q
from blogs.models import *
import os,json,bs4
from django.contrib.auth.decorators import login_required
from myblog import settings
from django.core.mail import send_mail
import threading
from django.db import transaction



# Create your views here.


# 首页
def index(request):
    article_list = Article.objects.all()

    return render(request,'index.html',{'article_list':article_list})

# 登录函数
def login(request): # 测试账户为：jack ，密码：1234
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        count = request.session.get('count')
        respone_data = {'user':None,'msg':None}
        if count < 8:
            username = request.POST.get('user')
            password = request.POST.get('pwd')
            valid_code = request.POST.get('codeimg')
            if valid_code and valid_code.upper() == request.session["valid_code_str"].upper():
                user = auth.authenticate(username=username,password=password)
                if user:
                    auth.login(request,user)
                    respone_data['user'] = request.user.username
                else:
                    respone_data['msg'] = '登录失败! 账户或密码错误'
            else:
                respone_data['msg'] = '登录失败! 验证码错误'
            count += 1
            request.session['count'] = count
            return JsonResponse(respone_data)
        # 如果重试次数等于8，提示操作频繁
        elif count == 8:
            print('超过次数了')
            print(request.session['count'])
            respone_data['msg'] = '操作过于频繁，请稍候再试'
            count += 1
            request.session['count'] = count
            return JsonResponse(respone_data)

        # 开启安全性更高的滑动解锁
        else:
            pass
            # 开启极验科技的滑动验证
            # 后续补充
            # 。。。

# 验证码函数
def get_validCode_img(request):
    img = get_valid_code_img(request)
    return HttpResponse(img)

# 注册函数
def register(request):
    if request.is_ajax():
        form = UserForms(request.POST)
        respone_data = {'user':None,'msg':None}
        if form.is_valid():
            respone_data['user'] = form.cleaned_data.get('username')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            telephone = form.cleaned_data.get('telephone')
            email = form.cleaned_data.get('email')
            avatar = request.FILES.get('avatar')
            ava_dic = {}
            if avatar:
                ava_dic['avatar'] = avatar
            UserInfo.objects.create_user(username=username,password=password,telephone=telephone,
                                         email=email,**ava_dic)
        else:
            respone_data['msg'] = form.errors
        return JsonResponse(respone_data)
    else:
        form = UserForms()
        return render(request,'register.html',{'form':form})

# 个人站点

def person_site(request,username,**kwargs):
    username = UserInfo.objects.filter(username=username).first()
    if not username:
        return render(request,'not_found.html')

    article_list = Article.objects.filter(user=username)

    # # 子查询
    # blog = username.blog
    # kind_query = Kind.objects.filter(blog=blog).values('title').annotate(c=Count('id'))
    # tag_query = Tag.objects.filter(blog=blog).values('title').annotate(c=Count('id'))
    #
    # date_list=Article.objects.filter(user=username).annotate(month=TruncMonth("create_time")).values("month").\
    #     annotate(c=Count("id")).values_list("month","c")

    # # join查询
    # kind = UserInfo.objects.filter(username=person).values('blog__kind__title').annotate(c=Count('blog__kind__id'))
    # tag = UserInfo.objects.filter(username=person).values('blog__tag__title').annotate(c=Count('blog_        # print('1',kind)
    # print('2',tag)

    # print('kind:',kind_query,'\ntag:',tag_query)
    # for i,j in result:
    #     print(i,j)
    if kwargs:
        condition = kwargs.get('condition')
        values = kwargs.get('param')
        print('condition',condition)
        print('values',values)
        if condition == 'kind':
            article_list = article_list.filter(kind__title=values)
        elif condition == 'tag':
            article_list = article_list.filter(tag__title=values)
        else:
            year,month = values.split('/')
            article_list = article_list.filter(create_time__year=year,create_time__month=month)

    return render(request,'person.html',locals())




# 文章详情函数
def article_detail(request,username,article_id):
    username = UserInfo.objects.filter(username=username).first()
    if username:
        article = Article.objects.filter(id=article_id).first()
        comment_list = Comment.objects.filter(article=article)
        return render(request,'article.html',locals())

# 评论

@login_required
def comment(request):
    pid = request.POST.get('pid')
    content = request.POST.get('content')
    article_id = request.POST.get('article_id')

    response = {"msg":None}


    if pid:
        parent,self_content = content.split('\n') #@lucy \n test
        parent_content = Comment.objects.filter(id=pid).first().content
        content = parent+':'+parent_content+'\n'+self_content

    # # 如果有父级评论键
    # if pid:
    #     # 进入递归函数
    #     def cont(pid,content):
    #         parent,self_content = content.split('\n') #@lucy \n test
    #         if '@' in parent: # 如果@符号还在
    #             parent = cont(pid,content)
    #
    #         # 从数据库查询数据并重新组合
    #         parent_content = Comment.objects.filter(id=pid).first().content
    #         content = parent+':'+parent_content+'\n\n'+self_content
    #         return content

    with transaction.atomic():
        c_obj = Comment.objects.create(user_id = request.user.pk,content = content,article_id=article_id,parent_comment_id = pid)
        Article.objects.filter(id=article_id).update(comment_count=F('comment_count')+1)

    response["create_time"] = c_obj.create_time.strftime("%Y-%m-%d %X")
    response["username"] = request.user.username
    response["content"] = content

    # 发送邮件

    article_obj = Article.objects.filter(id=article_id).first()

    t = threading.Thread(target=send_mail, args=("您的文章%s新增了一条评论内容" % article_obj.title,
                                                 content,
                                                 settings.EMAIL_HOST_USER,
                                                 ["XXXX@qq.com"])
                         )
    t.start()
    return JsonResponse(response)

# 删除评论

def comment_delete(request):
    comment_id = request.POST.get('comment_id')
    article_id = request.POST.get('article_id')

    response = {'msg':None}
    c_obj = Comment.objects.filter(id=comment_id,user=request.user).delete()
    a_obj = Article.objects.filter(id=article_id).update(comment_count=F('comment_count')-1)
    if c_obj and a_obj:
        response['msg'] = '已删除'
    return JsonResponse(response)



# 后台管理
@login_required
def backend(request,**kwargs):
    username = UserInfo.objects.filter(username=request.user).first()
    if not username:
        return render(request,'not_found.html')
    article_list = Article.objects.filter(user=username)

    if not kwargs:
        return render(request, 'backend/backend.html', {'article_list':article_list,'username':username})

    article_id = kwargs.get('article_id')
    param = kwargs.get('param')

    # 删除文章
    if param == 'delete':
        Article.objects.filter(user=username).filter(id=article_id).delete()
        article_list = Article.objects.filter(user=username)
        return render(request, 'backend/backend.html', {'article_list':article_list,'username':username})

    # 编辑，更新文章
    elif param == 'update':
        article = Article.objects.filter(user=username).filter(id=article_id).first()
        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
            soup = bs4.BeautifulSoup(content,'html.parser')
            # 防止xss攻击
            for dom in soup.find_all():
                print(dom.text)
                if dom.name == 'script':
                    dom.decompose()
                # 一句话木马
                if dom.text == "@eval($_POST['pass'])":
                    dom.decompose()
            desc = soup.text[:150]+'...'
            Article.objects.filter(user=username).filter(id=article_id).update(title=title,desc=desc,content=str(soup),user=request.user)
            return redirect('/backend')

        return render(request,'backend/update_article.html',{'article':article})
    else:
        pass

# 添加文章
@login_required
def add_article(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        soup = bs4.BeautifulSoup(content,'html.parser')
        # 防止xss攻击
        for dom in soup.find_all():
            print(dom.text)
            if dom.name == 'script':
                dom.decompose()
            # 一句话木马
            if dom.text == "@eval($_POST['pass'])":
                dom.decompose()

        desc = soup.text[:150]+'...'

        Article.objects.create(title=title,desc=desc,content=str(soup),user=request.user)
    return render(request,'backend/add_article.html')


# 上传文件
@login_required
def upload(request):
    # print(request.FILES)
    img = request.FILES.get('upload_img')
    path = os.path.join(settings.MEDIA_ROOT,'article_img',img.name)
    with open(path,'wb') as f:
        for bytes in img:
            f.write(bytes)

    responese = {
        'error':0,
        'url':'/media/article_img/%s'%img.name
    }
    return HttpResponse(json.dumps(responese))


# 点赞
@login_required
def diggit(request):
    is_up = json.loads(request.POST.get("is_up"))
    article_id = request.POST.get("article_id")
    user = request.user.pk

    article_obj = ArticleUpDown.objects.filter(article=article_id,user=user).first()
    response = {'checked':False}
    if not article_obj:
        print('添加记录')
        ss = ArticleUpDown.objects.create(article_id=article_id,user_id=user,is_up=is_up)
        print(ss)
        if is_up:
            Article.objects.filter(id=article_id).update(up_count=F('up_count')+1)
        else:
            Article.objects.filter(id=article_id).update(down_count=F('down_count')+1)
    else:
        response['checked'] = True
        response['hands'] = article_obj.is_up

    return JsonResponse(response)

# 退出
@login_required
def logout(request):
    auth.logout(request)
    return redirect('/index')