<script setup>
import { SwitchButton, CaretBottom, User, House } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '../../stores/userStore.js'
import { ref,reactive, onMounted, getCurrentInstance } from 'vue';
const userStore = useUserStore()
const router = useRouter()
import { useActiveStore } from '../../stores/active.js'
const activeStore = useActiveStore()
// 退出登录
const onEsc = async () => {
  await ElMessageBox.confirm('您确定退出吗', 'Warning', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
  router.push('/login')
  ElMessage.success("退出成功")
  userStore.updateUserInfo({})
}
const open = ref(false);
const ref1 = ref(null);
const ref2 = ref(null);
const ref3 = ref(null);
const ref4 = ref(null);
const ref5 = ref(null);
const ref6 = ref(null)
const current = ref(0);
const steps = [
  {
    title: 'AI助手',
    description: '可以在这里向AI咨询问题',
    target: () => ref1.value && ref1.value.$el,
    placement: 'right',
  },
  {
    title: '考试管理',
    description: '可以在这里管理了上传的试题、试卷以及考试',
    target: () => ref2.value && ref2.value.$el,
    placement: 'right',
  },
  {
    title: '答卷上传',
    description: '可以在这里对创建后的考试进行答卷与准考证号的上传,分配阅卷任务',
    target: () => ref3.value && ref3.value.$el,
    placement: 'right',
  },
  {
    title: '阅卷',
    description: '可以在这里对已经分配好阅卷任务的考试进行批阅和查看批阅成绩单',
    target: () => ref4.value && ref4.value.$el,
    placement: 'right',
  },
  {
    title: '单卷分析',
    description: '可以在这里对批改完的考试可视化查看结果',
    target: () => ref5.value && ref5.value.$el,
    placement: 'right',
  },
  {
    title: '个人信息',
    description: '可以在这里查看该账户的个人信息',
    target: () => ref6.value && ref6.value.$el,
    placement: 'right',
  }
]
const handleOpen = val => {
  open.value = val;
};
</script>
<template>
  <el-container>
    <div class="show"></div>
    <div class="win"></div>
    <el-header>
      <div class="logo">iMark <span>智能阅卷平台</span></div>
      <div class="nav">
        <el-button class="shen" color="#045afe" size="large">身份:教师</el-button>
        <el-button @click="open=true" class="tour" size="large">导航栏介绍</el-button>

        <a-tour v-model:current="current" :open="open" :steps="steps" @close="handleOpen(false)" />

        <!-- 下拉菜单 -->
        <el-dropdown placement="bottom-end">
          <span class="el-dropdown__box">
            <el-avatar :src="userStore.userInfo.avatar" />
            <el-icon>
              <CaretBottom />
            </el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="user" :icon="User" @click="() => {
                activeStore.updateActiveWeb(4)
                router.push('/user')
              }">个人中心</el-dropdown-item>
              <el-dropdown-item @click="onEsc" command="esc" :icon="SwitchButton">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </el-header>
    <el-main>
      <el-aside>
        <div class="bottom">
          <el-menu background-color="rgb(255,255,255)" router>
            <el-menu-item ref="ref1" index="/home" @click="() => {
              activeStore.updateActiveWeb(0)
            }" :class="{ 'active': activeStore.activePath == 0 }">
              <el-icon>
                <House />
              </el-icon>
              <span>首页</span>
            </el-menu-item>

            <el-menu-item ref="ref2" index="/add" @click="() => {
              activeStore.updateActiveWeb(1)
            }" :class="{ 'active': activeStore.activePath == 1 }">
              <el-icon>
                <Files />
              </el-icon>
              <span>考试管理</span>
            </el-menu-item>

            <el-menu-item ref="ref3" index="/aw" @click="() => {
              activeStore.updateActiveWeb(5)
            }" :class="{ 'active': activeStore.activePath == 5 }">
              <el-icon>
                <Camera />
              </el-icon>
              <span>答卷上传</span>
            </el-menu-item>

            <el-menu-item ref="ref4" index="/read" @click="() => {
              activeStore.updateActiveWeb(2)
            }" :class="{ 'active': activeStore.activePath == 2 }">
              <el-icon>
                <Tickets />
              </el-icon>
              <span>阅卷</span>
            </el-menu-item>

            <el-menu-item ref="ref5" index="/fenxi" @click="() => {
              activeStore.updateActiveWeb(3)
            }" :class="{ 'active': activeStore.activePath == 3 }">
              <el-icon>
                <DataLine />
              </el-icon>
              <span>单卷分析</span>
            </el-menu-item>

            <el-menu-item ref="ref6" index="/user" @click="() => {
              activeStore.updateActiveWeb(4)
            }" :class="{ 'active': activeStore.activePath == 4 }">
              <el-icon>
                <User />
              </el-icon>
              <span>个人信息</span>
            </el-menu-item>

          </el-menu>
        </div>
      </el-aside>
      <div class="main">
        <div class="bottom">
          <router-view></router-view>
        </div>
      </div>
    </el-main>
  </el-container>
 
</template>
<style scoped lang="scss">
.el-header {
  color: white;
  display: flex;
  height: 8vh;
  line-height: 8vh;
  justify-content: space-between;
  border-bottom: 1px solid rgba(0, 0, 0, .2);

  .logo {
    color: black;
    font-size: 2rem;
    margin-left: 3rem;

    span {
      font-size: 1rem;
    }
  }

  .nav {
    display: flex;
    width: 20%;
    position: relative;

    .shen {
      position: absolute;
      right: 15rem;
      top: 0rem;
      bottom: 0;
      margin: auto;
    }

    .tour {
      position: absolute;
      right: 9rem;
      top: 0rem;
      bottom: 0;
      margin: auto;

      &:hover {
        color: #045afe;
        border-color: #045afe;
        background-color: #fff;
      }
    }

    //下拉菜单
    .el-dropdown {
      position: absolute;
      right: 3rem;
      top: 0;
      bottom: 0;
      margin: auto;
    }

    .el-dropdown__box {
      display: flex;
      align-items: center;

      .el-icon {
        color: #999;
        margin-left: 10px;
      }

      &:active,
      &:focus {
        outline: none;
      }
    }

    div {
      a {
        text-decoration: none;
        font-size: 0.8rem;
        color: black;
      }

      a:hover {
        color: dodgerblue;
      }

      .router-link-exact-active {
        color: dodgerblue;
      }
    }
  }
}

.el-main {
  display: flex;
  background-color: rgb(241, 241, 241);
  // 侧边栏
  .el-aside {
    background-color: #fff;
    position: absolute;
    width: 15vw;
    height: 92vh;
    display: flex;
    flex-direction: column;
    border-right: 1px solid rgba(0, 0, 0, .1);
    box-shadow: 1px 1px 10px rgba(0, 0, 0, .1);
    left: 0;
    top: 8vh;

    // 导航部分
    .bottom {
      .el-menu {
        margin-top: 2rem;
        border-right: none;
        display: flex;
        flex-direction: column;
        align-items: center;

        .el-menu-item {
          border-radius: 5px;
          width: 85%;
          height: 2.5rem;
          margin-bottom: 1rem;
          color: black;
        }

        .el-menu-item:hover {
          background-color: #d2e0f6;
        }

        .active {
          background-color: #005ff5;
          color: white;

          &:hover {
            background-color: #005ff5;
            color: white;
          }
        }

        .el-icon {
          font-size: 1.5rem;
        }

        span {
          font-size: 1rem;
          margin-left: 0.5rem;
        }
      }
    }
  }

  // 内容区
  .main {
    margin-top: -2vh;
    margin-left: 16vw;
    width: 86vw;
  }
}
</style>
