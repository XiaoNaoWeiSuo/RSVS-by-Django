
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
from hienglish.common.sms import sms
from hienglish.common.veriemail import send_email
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django.views import View
import json
from .models import Account
import jwt
from datetime import datetime, timedelta
import uuid

@csrf_exempt
def verification_code(request):
    if request.method == 'GET':
        # 生成一个四位数验证码
        code = ''.join(random.choices('0123456789', k=4))
        value=request.GET.get('value')
        #Check the loacl
        if request.GET.get('type')=='e':
            status= send_email(value, code)
            #return JsonResponse({"code": code,"status":status})
        else:
            status = sms(value,code,request.GET.get('local'))
        return JsonResponse({"code": code,"status":status})

# 生成 token
def generate_token(user_name):
    # 设置 token 过期时间
    expiration_time = datetime.utcnow() + timedelta(days=20)  # 20天过期
    # 构造 payload
    payload = {
        'user_name': user_name,
        'exp': expiration_time,
    }
    # 生成 token
    token = jwt.encode(payload, '1234ZXCVBN', algorithm='HS256')
    return token  # 转为字符串返回

# 验证 token
def verify_token(request):
    # 从请求头中获取 token
    token = request.get('Authorization')
    #print(token)
    if token:
        try:
            # 解码 token
            payload = jwt.decode(token, '1234ZXCVBN', algorithms=['HS256'])
            username = payload.get('user_name')
            #print(username)
            # 查询用户
            user = Account.objects.get(name=username)
            return user
        except jwt.ExpiredSignatureError:
            # token 过期
            return None
        except jwt.InvalidTokenError:
            # token 无效
            return None
        except Account.DoesNotExist:
            # 用户不存在
            return None
    else:
        # 请求头中没有 token
        return None

# 用户注册接口
@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View): 
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')
        data1={}
        id=self.generate_unique_id()
        data2={"name":"","id": id}#newest:0无新消息或已读，1:有新消息未提醒未读
        data3={"object":[]}
        if username and password:
            if Account.objects.filter(name=username).exists():
                return JsonResponse({'status': 'error', 'message': 'Username already exists.'})
            else:
                account = Account(name=username, password=password, data1=json.dumps(data1), data2=json.dumps(data2), data3=json.dumps(data3))
                account.save()

                # Create a token for the new user
                token = generate_token(username)

                return JsonResponse({'status': 'success', 'token': token})
        else:
            return JsonResponse({'status': 'error', 'message': 'Username and password are required.'})
    def generate_unique_id(self):
        # 生成一个唯一的6位数字ID
        return str(uuid.uuid4().int)[:6]

# 用户登录接口
@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def post(self, request, *args, **kwargs):

        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return JsonResponse({'status': 400, 'message': 'Username and password are required.'})
        try:
            user = Account.objects.get(name=username)
        except Exception as e:
            return JsonResponse({'status': 409, 'message': 'User not found.'})

        if password == user.password:
            login(request, user)
            # Generate a custom token
            token = generate_token(username)
            return JsonResponse({'status': 200, 'token': token})
        else:
            return JsonResponse({'status': 401, 'message': 'Invalid username or password.'})

#数据读取三大金刚
@method_decorator(csrf_exempt, name='dispatch')
class UserData1View(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format.'})
        user = verify_token(data)
        if user:
            return JsonResponse({'status': 'success', 'data1': json.loads(user.data1)})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid or expired token.'})
@method_decorator(csrf_exempt, name='dispatch')
class UserData2View(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format.'})

        user = verify_token(data)
        if user:
            return JsonResponse({'status': 'success', 'data2': json.loads(user.data2)})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid or expired token.'})
@method_decorator(csrf_exempt, name='dispatch')
class UserData3View(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format.'})

        user = verify_token(data)
        if user:
            return JsonResponse({'status': 'success', 'data3': json.loads(user.data3)})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid or expired token.'})

#用户数据修改接口
@method_decorator(csrf_exempt, name='dispatch')
class UserData1Write(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format.'})
        user = verify_token(data)
        if user:
            user.data1 = json.dumps(data.get("data1"))
            user.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid or expired token.'})
@method_decorator(csrf_exempt, name='dispatch')
class UserData2Write(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format.'})

        user = verify_token(data)
        if user:
            user.data2 = json.dumps(data.get("data2"))
            user.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid or expired token.'})
@method_decorator(csrf_exempt, name='dispatch')
class UserData3Write(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format.'})
        user = verify_token(data)
        if user:
            user.data3 = json.dumps(data.get("data3"))
            user.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid or expired token.'})

#用户密码修改接口
@method_decorator(csrf_exempt, name='dispatch')
class UserPassword(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        user = verify_token(data)
        if user:
            if data.get("type")=="login":
                if user.password==data.get("old"):
                    user.password=data.get("new")
                    user.save()
                    return JsonResponse({
                        'status': 'success',
                    })
                else:
                    return JsonResponse({
                        'status': 'mistoken',
                    })
            elif data.get("type")=="pay":
                if json.loads(user.data2)["paykey"]==data.get("old"):
                    mid=json.loads(user.data2)
                    mid["paykey"]=data.get("new")
                    user.data2=json.dumps(mid)
                    user.save()
                    return JsonResponse({
                        'status': 'success',
                    })
                else:
                    return JsonResponse({
                        'status': 'mistoken',
                    })
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid or expired token.'})

#用户校验支付密码接口
@method_decorator(csrf_exempt, name='dispatch')
class UserPayKey(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        user = verify_token(data)
        if user:
            # 修改用户数据
            if json.loads(user.data2)["paykey"]==data.get("paykey"):
                finaldata=data.get("data")
                # 修改用户数据
                user.data1 = json.dumps(finaldata.get("data1"))
                user.data2 = json.dumps(finaldata.get("data2"))
                user.data3 = json.dumps(finaldata.get("data3"))
                # 保存修改后的用户数据到数据库
                user.save()
                return JsonResponse({
                    'status': 'success',
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message':'Password error'
                })
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid or expired token.'})

#用户注销接口
@method_decorator(csrf_exempt, name='dispatch')
class UserDelete(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        user = verify_token(data)
        if user:
            # 修改用户数据
            user.delete()
            return JsonResponse({
                'status': 'success',
            })
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid or expired token.'})


#用户上传证件照
@method_decorator(csrf_exempt, name='dispatch')
class UploadIDDocuments(View):
    def post(self, request, *args, **kwargs):
        if 'id_front' not in request.FILES or 'id_back' not in request.FILES:
            return JsonResponse({'status': 'error', 'message': 'Both id_front and id_back files are required.'})
        try:
            user=verify_token(request.POST)
            user.id_front = request.FILES['id_front']
            user.id_back = request.FILES['id_back']
            user.save()
            return JsonResponse({'status': 'success'})
        except:
            return JsonResponse({'status': 'error', 'message': 'Invalid or expired token.'})