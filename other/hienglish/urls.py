from django.urls import path
from .views import verification_code
from .views import RegisterView, LoginView, UserData1View,UserData2View,UserData3View,UserData1Write,UserData2Write,UserData3Write,UserDelete,UserPayKey,UserPassword
from .views import UploadIDDocuments

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path


urlpatterns = [
    path('upload-id-documents/', UploadIDDocuments.as_view(), name='upload-id-documents'),
    path('verification', verification_code, name='verification_code'),
    path('register/', RegisterView.as_view(), name='register'),#注册
    path('login/', LoginView.as_view(), name='login'),#登录
    path('userdata1/', UserData1View.as_view(), name='userdata1'),#读取
    path('userdata2/', UserData2View.as_view(), name='userdata2'),#读取
    path('userdata3/', UserData3View.as_view(), name='userdata3'),#读取
    path('write1/', UserData1Write.as_view(), name='write1'),#写入
    path('write2/', UserData2Write.as_view(), name='write2'),#写入
    path('write3/', UserData3Write.as_view(), name='write3'),#写入
    path('delete/', UserDelete.as_view(), name='delete'),#注销
    path('checkpaykey/', UserPayKey.as_view(), name='checkpaykey'),#校验支付密码
    path('cp/', UserPassword.as_view(), name='cp'),#校验/修改登录密码
]