from django.shortcuts import render
from products.models import Category
from .forms import RegisterForm, LoginForm, UserProfileForm
from .models import UserProfile
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,login,logout
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
import  os
import uuid
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from notifications.signals import notify




class IndexView(View):
    """
        访问网站首页
    """
    def get(self, request):
        categorys = Category.objects.all()
        return render(request, 'index.html', {"categorys":categorys})


class LoginView(View):
    def get(self,request):
        return render(request, 'login.html')

    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                MSG = "用户名或密码错误"
                return render(request,'login.html',{"MSG":MSG})

        else:
            return render(request,'login.html')


class RegistView(View):
    def get(self,request):
        form = RegisterForm()

        return render(request,'regist.html',{"form":form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = UserProfile()
            new_user.username = form.cleaned_data.get('username')
            new_user.email = form.cleaned_data.get('email')
            new_user.password = make_password(form.cleaned_data.get('password'))
            new_user.save()

            system = UserProfile.objects.filter(id=1).first()
            notify.send(sender=system,recipient=new_user,verb="欢迎成员Django仿天猫的一员")

            registSuccess = True
            return render(request, "regist.html",{"registSuccess":registSuccess})
        else:
            return render(request, "regist.html",{"form":form})


class LogoutView(View):
    """
    退出登录
    """
    def get(self, request):
        logout(request)
        return  HttpResponseRedirect(reverse("index"))


class ITaobaoView(View):
    def get(self, request):
        return render(request, 'itaobao.html')


class AccountSettingsView(View):
    """
    帐号设置
    """
    def get(self,request):
        return render(request, 'account_settings.html')


class PersonalData(View):
    """
    个人资料
    """

    def get(self,request):
        # if request.user.is_authenticated:
        #     return HttpResponseRedirect(reverse('index'))
        return render(request, 'personalData.html')

    # @login_required
    def post(self,request):

        userProfileForm = UserProfileForm(request.POST)
        if userProfileForm.is_valid():
            # user = UserProfile.objects.filter(id=request.user.id).first()
            #
            # user.nick_name = userProfileForm.cleaned_data.get('nick_name')
            # user.birthday = userProfileForm.cleaned_data.get('birthday')
            # user.gender = userProfileForm.cleaned_data.get('gender')
            # user.address = userProfileForm.cleaned_data.get('address')
            # user.mobile = userProfileForm.cleaned_data.get('mobile')
            # user.identityCardType = userProfileForm.cleaned_data.get('identityCardType')
            # user.identityCardNo = userProfileForm.cleaned_data.get('identityCardNo')
            #
            # user.save()

            request.user.nick_name = userProfileForm.cleaned_data.get('nick_name')
            request.user.birthday = userProfileForm.cleaned_data.get('birthday')
            request.user.gender = userProfileForm.cleaned_data.get('gender')
            request.user.address = userProfileForm.cleaned_data.get('address')
            request.user.mobile = userProfileForm.cleaned_data.get('mobile')
            request.user.identityCardType = userProfileForm.cleaned_data.get('identityCardType')
            request.user.identityCardNo = userProfileForm.cleaned_data.get('identityCardNo')

            request.user.save()


        return render(request, 'personalData.html',{"userProfileForm":userProfileForm})


@login_required
def user_avatar_upload(request):
    """上传头像"""

    data = {}

    # 获取临时路径
    if request.FILES.get('avatar_file',None):
        # 本地上传
        avatar_file = request.FILES['avatar_file']
        temp_folder = os.path.join('media','avatar')

        if not os.path.isdir(temp_folder):
            os.makedirs(temp_folder)

        temp_filename = uuid.uuid1().hex + os.path.splitext(avatar_file.name)[-1]
        temp_path = os.path.join(temp_folder, temp_filename)
        real_avatar_path = os.path.join('avatar', temp_filename)

        # 保存上传的文件
        with open(temp_path, 'wb') as f:
            for chunk in avatar_file.chunks():
                f.write(chunk)
    else:
        return HttpResponse("错误")


    # 裁剪图片
    top = int(float(request.POST['avatar_y']))
    buttom = top + int(float(request.POST['avatar_height']))
    left = int(float(request.POST['avatar_x']))
    right = left + int(float(request.POST['avatar_width']))

    from PIL import Image
    im = Image.open(temp_path)
    # 裁剪图片
    crop_im = im.convert("RGBA").crop((left, top, right, buttom)).resize((100, 100), Image.ANTIALIAS)

    # 设置背景颜色为白色
    out = Image.new('RGBA', crop_im.size, (255, 255, 255))
    out.paste(crop_im, (0, 0, 100, 100), crop_im)

    # 保存图片
    out.save(temp_path)
    # 保存记录
    request.user.avatar = real_avatar_path
    request.user.save()
    #os.remove(temp_path)


    data['success'] = True
    data['avatar_url'] = temp_path
    return JsonResponse(data)


class LogisticsView(LoginRequiredMixin,View):
    """
    物流消息
    """
    def get(self,request):
        return render(request, 'logistics.html')


class NotificationsView(LoginRequiredMixin,View):
    """
    读取个人消息
    """
    def get(self,request):
        """
        分页读取个人所有消息
        """

        notifications = request.user.notifications.active()
        paginator = Paginator(notifications, 10)    # 每页10条记录
        page = request.GET.get("page",1)
        try:
            notifications = paginator.page(page)
        except PageNotAnInteger:
            notifications = paginator.page(1)
        except EmptyPage:
            notifications = paginator.page(paginator.num_pages)


        return render(request,'notifications.html',{'notifications':notifications})


    def post(self,request):
        """
        将消息置为已读状态
        """

        action = request.POST.get('action',"")
        if not action:
            return JsonResponse({"status":"no","reason":"无操作"})
        elif action == 'delete_all':
            request.user.notifications.all().mark_all_as_deleted()
        elif action=='delete':
            nid = request.POST.get('nid',"")

            if  nid:
                request.user.notifications.get(id=nid).delete()
            else:
                return JsonResponse({"status":"no","reason":"无操作"})

        elif action == 'read':
            nid = request.POST.get('nid', "")

            if nid:
                request.user.notifications.get(id=nid).mark_as_read()
            else:
                return JsonResponse({"status": "no", "reason": "无操作"})

        return JsonResponse({"status":"ok"})


