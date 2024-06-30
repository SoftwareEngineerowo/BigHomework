<script setup>
import { ref } from 'vue'
import { uploadImgAPI, carveAllAwPaperAPI } from '@/api/imghandle.js'
import { getAllTestAPI, addAwPaperAPI, addCertifyAPI, changePaperStatusAPI } from '../../api/test.js';
const activeName = ref('first')
import { ElLoading } from 'element-plus'
import { ElMessage } from 'element-plus'

// 未开始答卷上传
// 获取全部未上传答卷的考试
const awList = ref([])
const getAllAw = async () => {
  const res = await getAllTestAPI()
  awList.value = res.data.data.filter((item) => item.hasAnswers == 0)
}
getAllAw()
// 上传答卷
// 请求同意分割答卷的参数data
const data = ref({
  paperId: 1,
  imgs: [],
  cert: ''
})
// 点击哪个考试获取哪个考试的paperId和examId
const examId = ref('')
const onClickExam = (exam) => {
  data.value.paperId = exam.paperIds.slice(1, -1)
  examId.value = exam.examId
}
const uploadDialog = ref(false)
const fileList1 = ref([])
const fileList2 = ref([])

// 确认上传答卷
const onUploadOne = async () => {
  if (fileList1.value.length == 0) {
    ElMessage({
      message: '请上传答卷',
      type: 'warning'
    })
    return
  }
  // 判断文件类型
  for (let item of fileList1.value) {
    if (item.raw.type !== 'image/jpeg' && item.raw.type !== 'image/png') {
      ElMessage.error('Picture must be JPG/Peng format!')
      return false
    }
  }

  // 正式开始上传答卷
  const loadingInstance1 = ElLoading.service({ fullscreen: true })
  for (let item of fileList1.value) {
    const filename = item.raw.name
    const res = await uploadImgAPI(filename, item.raw)
    data.value.imgs.push(res.data)
  }

  fileList1.value = []
  loadingInstance1.close()
  ElMessage({
    message: '上传答卷成功！',
    type: 'success'
  })
}

// 确认上传准考证
const onUploadTwo = async () => {
  // 判断是否已经上传准考证
  if (fileList2.value.length == 0) {
    ElMessage({
      message: '请上传准考证',
      type: 'warning'
    })
    return
  }
  const loadingInstance1 = ElLoading.service({ fullscreen: true })
  for (let item of fileList2.value) {
    const filename = item.raw.name
    const res = await uploadImgAPI(filename, item.raw)
    data.value.cert = res.data
    console.log(data.value.cert)
  }
  fileList2.value = []
  loadingInstance1.close()
  ElMessage({
    message: '上传准考证成功',
    type: 'success'
  })
}
// 最终确认上传两者+paperId
const onUploadConfirm = async () => {
  const loadingInstance1 = ElLoading.service({ fullscreen: true })
  if (value1.value == true) {
    data.value.imgs = showImgList.value
    data.value.cert = excel.value
  }
  const res = await carveAllAwPaperAPI(data.value)
  const ans = res.data.ans
  const cert = res.data.cert

  // 向后端数据库添加答卷
  for (let item of ans) {
    const data2 = {
      examId: examId.value,
      paperId: data.value.paperId,
      certId: item.certId,
      quesId: item.quesId,
      ansImg: item.url,
      scanResult: 'TAT'
    }
    const res = await addAwPaperAPI(data2)
  }

  // 向后端数据库添加准考证
  const data3 = {
    examId: examId.value,
    certs: cert
  }
  const res2 = await addCertifyAPI(data3)
  ElMessage({
    message: '上传成功',
    type: 'success'
  })
  // 更改考试状态
  await changePaperStatusAPI(examId.value, 1)
  loadingInstance1.close()
  // 关闭弹窗
  uploadDialog.value = false
  getAllAw()
  getAllAw2()

}





// 已完成答卷上传部分
const awList2 = ref([])
const getAllAw2 = async () => {
  const res = await getAllTestAPI()
  awList2.value = res.data.data.filter((item) => item.hasAnswers == 1)
}
getAllAw2()
// 分配
const onFenpei = async (examId) => {
  // 更改考试状态
  await changePaperStatusAPI(examId, 2)
  ElMessage.success("分配成功")
  getAllAw2()
}
// 演示模式
const value1 = ref(false)
const showImgList = ref([
'http://8.137.85.0:8008/files/download/img28e88b06-fb2b-11ee-9b91-00163e04f5e4.jpg',
'http://8.137.85.0:8008/files/download/img35d347a2-fb2b-11ee-8aee-00163e04f5e4.jpg',
'http://8.137.85.0:8008/files/download/img3fbdba2c-fb2b-11ee-8aee-00163e04f5e4.jpg',
'http://8.137.85.0:8008/files/download/img4bb1e2cc-fb2b-11ee-8aee-00163e04f5e4.jpg',
'http://8.137.85.0:8008/files/download/img55008978-fb2b-11ee-8aee-00163e04f5e4.jpg'
])
const excel = ref('http://8.137.85.0:8008/files/download/img3a59e4ce-fb2c-11ee-9b91-00163e04f5e4.xlsx')
</script>
<template>
  <div class="topTitle">
    答卷上传
  </div>
  <div class="container">
    <el-tabs type="card" v-model="activeName" class="demo-tabs" @tab-click="handleClick">
      <el-tab-pane label="未开始" name="first">
        <el-empty class="bottom" v-if="awList.length === 0" :image-size="200" />
        <ul class="bottom">
          <el-scrollbar>
            <li v-for="aw of awList" :key="aw.examId" @click="onClickExam(aw)">
              <a href="javascript:;">
                <!-- <svg class="icon testIcon" aria-hidden="true">
                  <use xlink:href="#icon-a-044_shige"></use>
                </svg> -->
                <el-button color="#045afe" plain type="success">答卷</el-button>
                <div class="content">
                  {{ aw.examName }}
                  <el-button @click="uploadDialog = true" class="start" type="primary" plain>上传答卷</el-button>
                </div>
              </a>
            </li>
          </el-scrollbar>
        </ul>

        <div class="test"></div>
      </el-tab-pane>

      <el-tab-pane label="已完成" name="three">

        <el-empty class="bottom" v-if="awList2.length === 0" :image-size="200" />
        <ul class="bottom">
          <li v-for="aw in awList2" :key="aw.examId">
            <a href="javascript:;">
              <!-- <svg class="icon testIcon" aria-hidden="true">
                <use xlink:href="#icon-a-044_shige"></use>
              </svg> -->
              <el-button color="#045afe" plain type="success">答卷</el-button>
              <div class="content">
                {{ aw.examName }}
                <el-button @click="$router.push(
                  {
                    path: '/assign',
                    query: {
                      examId: aw.examId
                    }
                  }
                )" class="start" type="primary" plain>分配阅卷任务</el-button>
              </div>
            </a>
          </li>
        </ul>
      </el-tab-pane>
    </el-tabs>


    <!-- 上传答卷弹框 -->
    <el-dialog v-model="uploadDialog">
      <div class="switch"> <el-switch v-model="value1" />是否开启演示模式</div>

      <el-upload v-if="!value1" v-model:file-list="fileList1" class="upload-demo" drag action="#" multiple
        :auto-upload="false">
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          Drop file here or <em>click to upload</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            jpg/png files
          </div>
          <el-button type="success" plain size="large" @click="onUploadOne">确认上传答卷</el-button>
        </template>
      </el-upload>
      <el-upload v-if="!value1" v-model:file-list="fileList2" class="upload-demo" drag action="#" multiple
        :auto-upload="false">
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          Drop file here or <em>click to upload</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            xlsx file
          </div>
          <el-button type="success" plain size="large" @click="onUploadTwo">确认上传准考证</el-button>

        </template>
      </el-upload>
      <div class="img" v-if="value1">
        <div class="title">学生答卷:</div>
        <img v-for="img of showImgList" :src="img">
      </div>
      <div class="excel" v-if="value1">
        <div class="title">准考证号:</div>
        <a :href="excel"> 本次考试准考证号</a>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="uploadDialog = false">取消上传</el-button>
          <el-button @click="onUploadConfirm" color="#045afe">确认上传</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>
<style lang="scss" scoped>
.topTitle {
  height: 7vh;
  line-height: 7vh;
  font-size: 1.6rem;
  font-weight: 100;
}
.container{
  background-color: white;
  min-height: 83vh;
}

.el-tabs {
  padding: 1rem;
  // 修改字体大小
  ::v-deep .el-tabs__item {
    font-size: 16px;
  }

  .el-tab-pane {
    .top {
      height: 2.5rem;
      line-height: 2.5rem;
      position: relative;

      span {
        position: absolute;
        font-size: 0.7rem;
        left: 1.7rem;

      }

      .add {
        float: right;
        margin-right: 2vw;
        background-color: #045afe;
      }
    }

    .bottom {
      li {
        height: 4rem;
        line-height: 4rem;
        // 开启相对定位
        position: relative;

        a {
          display: block;
          color: black;
        }

        // 考试图形
        .el-button {
          position: absolute;
          width: 2.5rem;
          height: 2.5rem;
          left: 1.5rem;
          top: 0;
          bottom: 0;
          margin: auto;
          font-size: 0.9rem;
        }

        // 内容部分
        .content {
          width: 90%;
          position: absolute;
          left: 5rem;
          top: 0;
          bottom: 0;
          margin: auto;
          font-size: 0.8rem;
          border-bottom: 1px solid rgba(0, 0, 0, .1);
          box-sizing: border-box;

          // 开始录入按钮
          .start {
            position: absolute;
            left: 85%;
            width: 5rem;
            height: 2rem;
            font-size: 0.7rem;
          }

          // 删除和编辑按钮
          .edit {
            position: absolute;
            left: 38rem;
            width: 2rem;
            height: 2rem;
          }

          .delete {
            position: absolute;
            left: 41rem;
            width: 2rem;
            height: 2rem;
          }
        }
      }

      li:hover {
        background-color: #d2e0f6;
      }
    }

  }
}

// 上传弹框
.el-dialog {
  .el-button {
    margin-top: 0.5rem
  }

  .img {
    margin-top: 1rem;

    img {
      width: 14rem;
    }
  }

  .excel {
    margin-top: 1rem;

    a {
      display: block;
      margin-top: 1rem;
      text-decoration: none;
      color: rgb(168, 205, 242);
    }

    a:hover {
      color: dodgerblue;
    }
  }

}
</style>
