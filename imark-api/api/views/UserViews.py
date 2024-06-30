from api import models
from rest_framework.views import APIView
from rest_framework.response import Response
from ext import Code
import uuid

from api.serializers.userSerializers import UserSerializer

code=Code.SUCCESS_CODE
msg=''

#注册
class RegisteredView(APIView):
    def post(self,request):
        ser = UserSerializer(data=request.data)
        if ser.is_valid():
            # 序列化验证通过，数据类型正确
            after_data = ser.validated_data  # 将通过验证的json数据转化为字典
            roleId=after_data.get('roleId')
            role_obj = models.Role.objects.filter(roleId=roleId).first()
            if not role_obj:
                new_obj = models.Role()
                sysId=str(uuid.uuid1())
                new_obj.sysId=sysId
                new_obj.roleId=roleId
                new_obj.username=after_data.get('username')
                new_obj.password=after_data.get('password')
                new_obj.save()
                a_ser=UserSerializer(instance=new_obj)
                code = Code.SUCCESS_CODE
                msg = "注册成功"
                data = a_ser.data
            else:
                code = Code.ERROR_CODE
                msg = "roleId已经存在，请修改"
                data = after_data
        else:
            #序列化验证失败，数据不正确
            msg= ser.errors
            code=Code.ERROR_CODE
            data={}
        context = {'code': code, 'msg': msg, 'data': data}
        return Response(context)


#登录
class LoginView(APIView):
    def post(self, request):
        roleId=request.data["roleId"]
        password=request.data["password"]
        r_obj=models.Role.objects.filter(roleId=roleId,password=password).first()
        if not r_obj:
            code=Code.ERROR_CODE
            msg="登录失败，账号或密码错误"
            data={
                "roleId":roleId,
                "password":password
            }
        else:
            code=Code.SUCCESS_CODE
            msg="登录成功"
            ser=UserSerializer(instance=r_obj)
            data=ser.data
        context = {'code': code, 'msg': msg, 'data': data}
        return Response(context)


#修改个人资料
class UserInfoUpdateView(APIView):
    def post(self, request):
        ser = UserSerializer(data=request.data)
        if ser.is_valid():
            # 序列化验证通过，数据类型正确
            after_data = ser.validated_data  # 将通过验证的json数据转化为字典
            sysId=after_data['sysId']
            sy_obj=models.Role.objects.filter(sysId=sysId).first()
            sy_obj1=models.Role.objects.filter(sysId=sysId).first()
            if not sy_obj:
                code=Code.ERROR_CODE
                msg="该用户不存在，请检查sysId"
                data=after_data
            else:
                new_roleId=after_data['roleId']
                models.Role.objects.filter(sysId=sysId).update(roleId="-1")
                ro_obj=models.Role.objects.filter(roleId=new_roleId).first()
                if not ro_obj:
                    sy_obj.roleId=new_roleId
                    sy_obj.username=after_data['username']
                    sy_obj.password=after_data['password']
                    sy_obj.avatar=after_data['avatar']
                    sy_obj.save()
                    serbefore=UserSerializer(instance=sy_obj1)
                    serafter=UserSerializer(instance=sy_obj)
                    code=Code.SUCCESS_CODE
                    msg='修改信息成功'
                    data={
                        "oldInfo" : serbefore.data,
                        "newInfo" : serafter.data
                    }

                else:
                    code=Code.ERROR_CODE
                    msg="修改失败，roleId已经存在，请修改roleId"
                    data=after_data
        else:
            #序列化验证失败，数据不正确
            msg= ser.errors
            code=Code.ERROR_CODE
            data={}
        context={'code':code,'msg':msg,'data':data}
        return Response(context)
