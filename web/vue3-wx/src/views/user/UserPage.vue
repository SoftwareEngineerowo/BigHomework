<script setup>
import { ref } from 'vue'
import { updateUserInfoAPI } from '@/api/user.js'
import { uploadImgAPI } from '@/api/imghandle.js'
import { useUserStore } from '../../stores/userStore';

const userStore = useUserStore()
// 本地上传之后回显头像
const imgUrl = ref(userStore.userInfo.avatar)
const file = ref({})
const onShowImg = (f) => {
  imgUrl.value = URL.createObjectURL(f.raw)
  file.value = f
}
// 准备请求参数
const formModel = ref({
  sysId: userStore.userInfo.sysId,
  avatar: userStore.userInfo.avatar,
  roleId: userStore.userInfo.roleId,
  username: userStore.userInfo.username,
  password: userStore.userInfo.password
})
// 取消修改
const onCancel = () => {
  formModel.value = {
    sysId: userStore.userInfo.sysId,
    avatar: userStore.userInfo.avatar,
    roleId: userStore.userInfo.roleId,
    username: userStore.userInfo.username,
    password: userStore.userInfo.password
  }
}
// 确认修改
const onConfirm = async () => {
  // 上传图片
  const filename = file.value.raw.name
  const res = await uploadImgAPI(filename, file.value.raw)
  formModel.value.avatar = res.data
  // 发送请求
  const res1 = await updateUserInfoAPI(formModel.value)
  // 修改仓库中的和表单中的用户信息
  userStore.updateUserInfo(formModel.value)
  formModel.value = res1.data.data.newInfo
  ElMessage.success("修改成功")
}
</script>
<template>
  <div class="topTitle">
    个人信息
  </div>
  <div class="container">
    <el-card class="info">
      <template #header>
        基本信息
      </template>
      <div class="box">
        <div class="left">
          <el-avatar class="left" :src="userStore.userInfo.avatar" />
          <div>{{ userStore.userInfo.username }}</div>
        </div>
        <div class="right">
          <div class="item">账号: {{ userStore.userInfo.roleId }}</div>
          <div class="item">身份: <el-button plain type="primary">教师</el-button></div>
        </div>
      </div>
    </el-card>

    <el-card class="state">
      <template #header>
        账户身份
      </template>
      <el-button plain type="primary" color="">教师</el-button>
    </el-card>
    <el-card class="update">
      <template #header>
        更改信息
      </template>
      <el-form :model="formModel" label-width="auto">
        <el-form-item class="avatar" label="头像：">
          <el-avatar shape="square" :size="130" :fit="fit" :src="imgUrl" :on-exceed="onExceed" />
          <div class="upload">
            <el-upload v-model:file-list="fileList" :limit="1" :on-change="onShowImg">
              <el-button type="success" plain size="large">上传头像</el-button>
            </el-upload>
          </div>
        </el-form-item>
        <el-form-item label="用户名:">
          <el-input v-model="formModel.username" size="large"></el-input>
        </el-form-item>
        <el-form-item label="密码:">
          <el-input v-model="formModel.password" size="large"></el-input>
        </el-form-item>
        <el-form-item class="btn">
          <el-button @click="onCancel" size="large" class="btn1">取消</el-button>
          <el-button @click="onConfirm" size="large" color='#045afe'>修改</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>
<style lang="scss" scoped>
.topTitle {
  height: 7vh;
  line-height: 7vh;
  font-size: 1.6rem;
  font-weight: 100;
}

.container {
  display: flex;
  flex-direction: column;
  min-height: 83vh;
}

// 上部基本信息
.info {
  border-radius: 10px;
  height: 15vh;

  .box {
    display: flex;
    height: 7vh;
  }

  .left {
    height: 7vh;
    line-height: 7vh;
    display: flex;
    font-size: 18px;

    .el-avatar {
      height: 3.5rem;
      width: 3.5rem;
      margin-right: 1rem;
    }
  }

  .right {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    margin-left: 3rem;
    font-size: 18px;
  }
}

.state {
  margin-top: 3vh;
  border-radius: 10px;
  width: 100%;
  height: 12vh;
}

// 下部更新部分
.update {
  margin-top: 3vh;
  border-radius: 20px;
  flex: 1;
  border-radius: 10px;
  position: relative;
  overflow: auto;
  height: 40%;

  .el-form {
    position: absolute;
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    height: 70%;
    top: 0;
    bottom: 0;
    left: 2rem;
    margin: auto;

    .el-form-item {
      width: 100%;

      .el-input {
        width: 100%;
      }
    }

    .avatar {
      .upload {
        position: absolute;
        left: 8rem;
      }
    }

    .btn {
      .btn1 {
        margin-left: 12rem;
      }
    }
  }
}
</style>
