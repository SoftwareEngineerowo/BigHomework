<script setup>
import { ref, watch } from 'vue'
import { talkAiAPI } from '@/api/ai.js'
import { useUserStore } from '../../stores/userStore';
const userStore = useUserStore()
import { useActiveStore } from '../../stores/active.js'
import { Position } from '@element-plus/icons-vue';
const activeStore = useActiveStore()
// 存储发送信息
const inputValue = ref('')
// 用来存储用户及ai的信息
const infoList = ref([])
// 点击发送按钮后的逻辑
const btnLoading = ref(false)
const dialogLoading = ref(false)


const fullText = ref('')
const displayText = ref('')
const onSend = async () => {
  // 判断是否为空
  if (inputValue.length == 0) {
    ElMessage.warning("发送数据不能为空")
    return
  }
  // 不为空则插入用户发送数据
  infoList.value.push({ isUser: true, info: inputValue.value })
  // 开启loading效果
  btnLoading.value = true
  infoList.value.push({ isUser: false, info: '' })
  dialogLoading.value = true

  // 封装请求数据
  const sysId = "57C8F5F7-36A9-769C-26D3-6ED7C76D3602"
  const fresh = 0
  const formData = new FormData()
  formData.append('sysId', sysId)
  formData.append('content', inputValue.value)
  formData.append('fresh', fresh)

  // 清空对话框
  inputValue.value = ''
  // 请求数据并获取结果
  const res = await talkAiAPI(formData)
  // infoList.value[infoList.value.length - 1].info = res.data
  fullText.value = res.data
  const chunkSize = 1
  let currentIndex = 0

  const intervalId = setInterval(() => {
    if (currentIndex < fullText.value.length) {
      const chunk = fullText.value.substring(currentIndex, currentIndex + chunkSize);
      // displayText.value.push(chunk)
      infoList.value[infoList.value.length - 1].info += chunk
      currentIndex += chunkSize;
    }
    else {
      clearInterval(intervalId);
    }
  }, 100); // 每秒显示chunkSize个字符  

  // 关闭loading效果
  btnLoading.value = false
  dialogLoading.value = false
}

// 监视infoList的变化
watch(infoList, () => {
  setTimeout(() => {
    const scrollref = document.querySelector('.bottombottom .content')
    console.log(scrollref.scrollHeight)
    scrollref.scrollTop = scrollref.scrollHeight
  }, 0)
}, {
  deep: true
})

</script>
<template>
  <div class="container">
    <div class="bottombottom">
      <div class="content">

        <div class="dialogbox" v-if="!infoList[0]?.info">
          <div class="left">
            <el-avatar :size="35">
              <img src="../../assets/ai.png" alt="">
            </el-avatar>
          </div>
          <div class="right">
            <div class="name">人工智能</div>
            <div class="res ai">需要做一些什么？</div>
          </div>
        </div>
        <div class="dialogbox" v-for="info of infoList" :key="info.info">
          <div class="left">
            <el-avatar v-if="info.isUser == true" :size="35" :src="userStore.userInfo.avatar" />

            <el-avatar v-if="info.isUser == false" :size="35">
              <img src="../../assets/ai.png" alt="">
            </el-avatar>

          </div>
          <div class="right">
            <div class="name">{{ info.isUser == true ? '你' : '人工智能' }}</div>
            <div class="res ai" v-if="info.isUser == false" v-loading="dialogLoading && info.info == ''">{{ info.info }}
            </div>
            <div class="res user" v-if="info.isUser == true">{{ info.info }}</div>
          </div>
        </div>
      </div>

      <div class="input">
        <el-input class="area" @keyup.enter="onSend" v-model="inputValue" size="large" type="textarea"
          :autosize="{ minRows: 4, maxRows: 6 }">
        </el-input>
        <el-button :icon="Position" color="#045afe" @click="onSend" size="large" :loading="btnLoading"></el-button>
      </div>

    </div>
  </div>
</template>
<style lang="scss" scoped>
.container {
  overflow: hidden;
  height: 90vh;
  backdrop-filter: blur(100px);
}

// 下部AI助手
div.bottombottom {
  background: linear-gradient(135deg,
      hsl(0, 0%, 100%),
      hsl(235, 44%, 95%),
      hsl(223, 100%, 94%),
      hsl(226, 78%, 87%));
  width: 100%;
  margin: 0 auto;
  margin-top: 2rem;
  height: 85.5vh;
  border-radius: 20px;
  padding-bottom: 0;

  // 对话内容区
  .content {
    box-sizing: border-box;
    height: 86%;
    padding-top: 2rem;
    overflow-y: auto;

    // 一个对话
    .dialogbox {
      width: 60%;
      display: flex;
      margin-bottom: 2rem;
      margin-left: 10rem;

      // 右边内容区域
      .right {
        margin-top: 0.2rem;
        margin-left: 0.3rem;

        .name {
          font-weight: bold;
          font-size: 0.8rem;
          min-width: 4rem;
        }

        .res {
          min-height: 1rem;
          min-width: 1rem;
          font-size: 0.85rem;
          margin-top: 0.3rem;
          line-height: 1.4rem;
          color: white;
          border-radius: 10px;
          padding: 10px;
        }

        .ai {
          background-color: rgb(255, 255, 255);
          color: rgb(0, 0, 0);
        }

        .user {
          color: black;
        }

      }
    }
  }

  // 输入区
  .input {
    width: 70%;
    height: 11%;
    text-align: center;
    margin: 0 auto;
    position: relative;

    .area {
      width: 100%;
      height: 20vh;
      margin: 0 auto;
    }

    .el-button {
      position: absolute;
      bottom: 20px;
      right: 10px;
      border-radius: 20px;
    }
  }
}</style>
