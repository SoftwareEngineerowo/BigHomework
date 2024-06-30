<script setup>
import { ref } from 'vue'
import { User, Lock } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router';
import { loginAPI, registerAPI } from '@/api/user.js'
import { useUserStore } from '../../stores/userStore';
const userStore = useUserStore()
const router = useRouter()

const isLogin = ref(true)
const formModel = ref({
  roleId: '',
  password: ''
})
const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 1, max: 6, message: '用户名长度在 1 到 6 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 15, message: '密码长度在 6 到 15 个字符', trigger: 'blur' },
    { pattern: /^[^\s]*$/, message: '密码不能包含空格', trigger: 'blur' }
  ],
  roleId: [
    { required: true, message: '请输入账号', trigger: 'blur' },
    { len: 11, message: '角色ID必须为11位数字', trigger: 'blur' },
    { pattern: /^\d{11}$/, message: '账号只能为11位数字', trigger: 'blur' }
  ],
  repassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    { validator: confirmPassword, trigger: 'blur' }
  ]
}
// 自定义验证规则：确认密码与密码一致  
function confirmPassword(rule, value, callback) {
  if (value === '') {
    callback(new Error('请再次输入密码'));
  } else if (value !== formModel2.value.password) {
    callback(new Error('两次输入的密码不一致'));
  } else {
    callback();
  }
}
const formRef = ref()
// 登录按钮
const onLogin = async () => {
  await formRef.value.validate()
  const res = await loginAPI(formModel.value)

  ElMessage.success("登录成功")
  userStore.updateUserInfo(res.data.data)
  router.push('/home')
}


const formModel2 = ref({
  roleId: '',
  username: '',
  password: '',
  repassword: ''
})

const formRef2 = ref()
// 注册按钮
const showDialog = ref(false)
const result2 = ref({})
const onRegister = async () => {
  await formRef2.value.validate()
  // 获取roleId
  function randomNum(n) {
    var res = "";
    for (var i = 0; i < n; i++) {
      res += Math.floor(Math.random() * 10);
    }
    return res;
  }
  formModel2.value.roleId = randomNum(11)
  const res = await registerAPI(formModel2.value)

  ElMessage.success("注册成功")
  result2.value = res.data.data
  showDialog.value = true
  formModel2.value = {}
}
</script>
<template>
  <el-container>
    <el-header>iMark <span>智能阅卷平台</span></el-header>

    <el-main>
      <el-row>
        <el-col class="loginBox" :span="10" :offset="12">
          <!-- 登录 -->
          <el-form ref="formRef" :rules="rules" :model="formModel" v-if="isLogin" size="large" autocomplete="off">
            <el-form-item>
              <div class="title">登 录</div>
            </el-form-item>
            <el-form-item prop="roleId">
              <el-input v-model="formModel.roleId" :prefix-icon="User" placeholder="请输入账号"></el-input>
            </el-form-item>
            <el-form-item prop="password">
              <el-input v-model="formModel.password" :prefix-icon="Lock" type="password" placeholder="请输入密码"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button @click="onLogin" class="button"  color="#045afe">登 录</el-button>
            </el-form-item>
            <el-form-item class="to">
              <a href="javascript:;" @click="isLogin = false">
                <el-icon>
                  <ArrowLeftBold />
                </el-icon>
                <span>注册</span>
              </a>
            </el-form-item>
          </el-form>

          <!-- 注册 -->
          <el-form ref="formRef2" :rules="rules" :model="formModel2" v-else size="large" autocomplete="off">
            <el-form-item>
              <div class="title">注 册</div>
            </el-form-item>
            <el-form-item prop="username">
              <el-input v-model="formModel2.username" :prefix-icon="User" placeholder="请输入用户名"></el-input>
            </el-form-item>
            <el-form-item prop="password">
              <el-input v-model="formModel2.password" :prefix-icon="Lock" type="password" placeholder="请输入密码"></el-input>
            </el-form-item>
            <el-form-item prop="repassword">
              <el-input v-model="formModel2.repassword" :prefix-icon="Lock" type="password"
                placeholder="请再次输入密码"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button @click="onRegister" class="button"  color="#045afe">注 册</el-button>
            </el-form-item>
            <el-form-item class="to">
              <a href="javascript:;" @click="isLogin = true">
                <el-icon>
                  <ArrowLeftBold />
                </el-icon>
                <span>登录</span>
              </a>
            </el-form-item>
          </el-form>
        </el-col>
        <div class="bg"></div>
      </el-row>
    </el-main>
  </el-container>
  <!-- 显示账号弹窗 -->
  <el-dialog v-model="showDialog">
    <el-descriptions class="margin-top" :column="3" :size="size" border>
      <el-descriptions-item>
        <template #label>
          <div>用户名</div>
        </template>
        {{ result2.username }}
      </el-descriptions-item>

      <el-descriptions-item>
        <template #label>
          <div>账号</div>
        </template>
        {{ result2.roleId }}
      </el-descriptions-item>

      <el-descriptions-item>
        <template #label>
          <div>密码</div>
        </template>
        {{ result2.password }}
      </el-descriptions-item>
    </el-descriptions>
  </el-dialog>
</template>

<style lang="scss" scoped>
.el-container{
  min-width: 1533px;
}
a {
  text-decoration: none;
  color: black;
}

a:hover {
  color: dodgerblue
}

.el-header {
  height: 6vh;
  line-height: 6vh;
  font-size: 3rem;
  margin-left: 4vw;
  span {
    font-size: 1.5rem;
  }
}

.el-main {
  height: 94vh;
  background-color: rgb(245, 245, 245);
  background-image: url('@/assets/bg.jpg');
  background-repeat: no-repeat;
  background-size: 100% 100%;

  .loginBox {
    position: relative;
    z-index: 2;
    height: 50vh;
    margin-top: 5vh;
    border-radius: 10px;
    background-color: rgba(255,255,255,0.13);
    backdrop-filter: blur(10px); 
    box-shadow: 0 0 30px 10px rgba(0, 0, 0, .1);

    .el-form {
      position: absolute;
      width: 60%;
      height: 80%;
      // 垂直居中
      margin: auto;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      display: flex;
      flex-direction: column;
      justify-content: space-around;

      .to {
        a {
          display: block;
          height: 2rem;
          line-height: 2rem;
          font-size: 0.7rem;

          span {
            margin-left: 0.5rem;
          }
        }
      }

      .title {
        margin: 0 auto;
        font-size: 1.5rem;
        color: dodgerblue;
      }

      .el-input {
        margin-top: 0.5rem;
        width: 100%;
      }

      .el-button {
        margin-top: 0.5rem;
        width: 100%;
      }

      .el-link span {
        font-size: 0.7rem;
      }
    }
  }
}
</style>
