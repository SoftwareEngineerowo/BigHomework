<script setup>
import { ref } from 'vue'
import AddTestDialog from '@/components/AddTestDialog.vue'
import VirtualList from '../../components/VirtualList.vue'
import {
  getAllQuesAPI, getAllPaperAPI, getAllTestAPI,
  getQuesByTypeAPI, addQuesTypeAPI, getPaperByIdAPI,
  deleteQuesByIdAPI, deletePaperByIdAPI, deleteExamByIdAPI,
  changePaperStatusAPI
} from '@/api/test.js'
import { ElMessage, ElMessageBox } from 'element-plus';
const activeName = 'first'
const addTestDialog = ref()
// 试题部分
// 获取全部试题
const quesList = ref([])
const quesTypeList = ref([{ quesKindId: 1, quesKindName: '单选题' }, { quesKindId: 2, quesKindName: '多选题' }, { quesKindId: 3, quesKindName: '简答题' }, { quesKindId: 4, quesKindName: '判断题' }])
const getAllQues = async () => {
  const res = await getAllQuesAPI()
  quesList.value = res.data.data
}
getAllQues()
// 添加试题类型
const formModel = ref({
  quesKindName: ''
})
const questypedialog = ref(false)
const onQuesTypeComfirm = async () => {
  const res = await addQuesTypeAPI(formModel.value)
  questypedialog.value = false
}
// 根据试题类型搜索试题功能
const quesSelectValue = ref()
// 装所搜索的试题
const onQuesSearch = async () => {
  const res = await getQuesByTypeAPI(Number(quesSelectValue.value))
  quesList.value = res.data.data
}
// 清空按钮
const onQuesClear = () => {
  quesSelectValue.value = ''
  getAllQues()
}
// 删除成功通知
const onSuccess2 = () => {
  getAllQues()
}





// 试卷部分
// 获取所有试卷
const paperList = ref([])
const getAllPaper = async () => {
  const res = await getAllPaperAPI()
  paperList.value = res.data.data
}
getAllPaper()
// 删除试卷
const onDeletePaper = async (paper) => {
  await ElMessageBox.confirm('您确定删除该试卷吗', 'Warning', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
  const res = await deletePaperByIdAPI(paper.paperId)
  ElMessage.success("删除成功")
  getAllPaper()
}


// 获取全部考试
const examList = ref([])
const state = ['未上传答卷', '未分配阅卷任务', '未批改', '已批改']
const getAllExam = async () => {
  const res = await getAllTestAPI()
  examList.value = res.data.data
}
getAllExam()
// 新建考试
const onAddTest = () => {
  addTestDialog.value.open({})
}
const onSuccess = () => {
  getAllExam()
}
// 点击显示对应考试具体信息
const testShowDialog = ref(false)
// 渲染在弹窗上的信息
const ExamInfo = ref({
  examName: '第一次期末考试',
  newPaperList: [],
  time1: '',
  time2: ''
})
// 点击考试列表展现考试详情
const onClickExam = async (exam) => {
  testShowDialog.value = true
  ExamInfo.value.newPaperList = []
  // 考试名称
  ExamInfo.value.examName = exam.examName
  const id = exam.paperIds.slice(1, -1)
  const res = await getPaperByIdAPI(id)
  ExamInfo.value.newPaperList.push(res.data.data)
  // 考试时间处理
  const timeArray = exam.examTimes.split("'")
  const time1 = timeArray[3]
  const time2 = timeArray[7]
  ExamInfo.value.time1 = time1
  ExamInfo.value.time2 = time2
}
// 删除考试
const onDeleteExam = async (exam) => {
  await ElMessageBox.confirm('您确定删除该考试吗', 'Warning', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
  const res = await deleteExamByIdAPI(exam.examId)
  ElMessage.success("删除成功")
  getAllExam()
}
// 获取视口高度
const viewportHeight = window.innerHeight
const elementHeightInPx = viewportHeight * 0.08
</script>
<template>
  <div class="topTitle">
    考试管理
  </div>
  <div class="contaniner">
    <el-tabs type="card" v-model="activeName" class="demo-tabs" @tab-click="handleClick">
      <el-tab-pane label="试题" name="first">
        <div class="top">
          <el-form>
            <el-form-item label="题型:">
              <el-select v-model="quesSelectValue" placeholder="Select" size="large">
                <el-option v-for="quesType of quesTypeList" :key="quesType.quesKindId" :label="quesType.quesKindName"
                  :value="quesType.quesKindId" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button @click="onQuesSearch" size="large" type="primary" color="#045afe">
                搜索
              </el-button>
            </el-form-item>
            <el-form-item>
              <el-button @click="onQuesClear" size="large">清空</el-button>
            </el-form-item>
          </el-form>

        </div>
        <el-empty class="bottom" v-if="quesList.length === 0" :image-size="200" />
        <ul class="bottom" v-if="quesList.length != 0">
          <!-- 虚拟列表组件 -->
          <VirtualList @success="onSuccess2" :item-height="elementHeightInPx" :items="quesList"> </VirtualList>
        </ul>
      </el-tab-pane>

      <el-tab-pane label="试卷" name="second">
        <div class="top">
          <el-button @click="$router.push('/carve')" class="add" size="large" color="#045afe" plain>添加试卷</el-button>
        </div>
        <el-empty class="bottom" v-if="paperList.length === 0" :image-size="200" />
        <ul class="bottom" v-if="paperList.length != 0">
          <li v-for="paper of paperList">
            <a href="javascript:;">
              <el-button color="#045afe" plain type="success">试卷</el-button>
              <div class="content">
                <div>{{ paper.paperName }}</div>
                <el-button @click.stop="onDeletePaper(paper)" class="delete" plain type="danger">删除</el-button>
              </div>
            </a>
          </li>
        </ul>
      </el-tab-pane>

      <el-tab-pane label="考试" name="three">
        <div class="top">
          <el-button @click="onAddTest" class="add" type="primary" size="large" color="#045afe" plain>添加考试</el-button>
        </div>
        <el-empty class="bottom" v-if="examList.length === 0" :image-size="200" />
        <ul class="bottom" v-if="examList.length != 0">
          <el-scrollbar>
            <li @click="onClickExam(exam)" v-for="exam of examList" :key="exam.examId">
              <a href="javascript:;">
                <el-button color="#045afe" plain type="success">考试</el-button>
                <div class="content">
                  <el-button @click.stop class="info" plain type="primary">{{ state[exam.hasAnswers] }}</el-button>
                  <el-button @click.stop="onDeleteExam(exam)" class="delete" plain type="danger">删除</el-button>
                  {{ exam.examName }}
                  <div class="time">
                  </div>
                </div>
              </a>
            </li>
          </el-scrollbar>
        </ul>
      </el-tab-pane>
    </el-tabs>
    <!-- 添加试题类型弹出层 -->
    <el-dialog class="questypedialog" v-model="questypedialog" width="400">
      <el-form :model="formModel" :rules="rulse">
        <el-form-item prop="quesKindName" label="题型名称：">
          <el-input v-model="formModel.quesKindName" placeholder="请输入您想添加的题型"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="questypedialog = false">取消</el-button>
          <el-button @click="onQuesTypeComfirm"  color="#045afe">
            确定
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
  <!-- 添加考试组件 -->
  <AddTestDialog @success="onSuccess" ref="addTestDialog"></AddTestDialog>
  <!-- 显示考试弹窗部分 -->
  <el-dialog v-model="testShowDialog" width="400">
    <el-descriptions class="margin-top" title="考试详情" :column="1" :size="size" border>
      <el-descriptions-item>
        <template #label>
          <div class="cell-item">
            <el-icon>
              <EditPen />
            </el-icon>
            <div>考试名称</div>
          </div>
        </template>
        {{ ExamInfo.examName }}
      </el-descriptions-item>
      <el-descriptions-item>
        <template #label>
          <div class="cell-item">
            <el-icon>
              <Clock />
            </el-icon>
            <div>考试时间</div>
          </div>
        </template>
        {{ ExamInfo.time1 }}——{{ ExamInfo.time2 }}
      </el-descriptions-item>

      <el-descriptions-item>
        <template #label>
          <div class="cell-item">
            <el-icon>
              <Document />
            </el-icon>
            <div>考试试卷</div>
          </div>
        </template>
        <ul>
          <li v-for="paper of ExamInfo.newPaperList" :key="paper.paperId">
            <a href="javascript:;">{{ paper.paperName }}</a>
          </li>
        </ul>
      </el-descriptions-item>
    </el-descriptions>



    <template #footer>
      <span class="dialog-footer">
        <el-button @click="testShowDialog = false" color="#045afe">确认</el-button>
      </span>
    </template>
  </el-dialog>
</template>
<style lang="scss" scoped>
.topTitle {
  height: 7vh;
  line-height: 7vh;
  font-size: 1.6rem;
  font-weight: 100;
}

.contaniner {
  padding-top: 2vh;
  padding-left: 2vw;
  background-color: #fff;
  min-height: 83vh;

  // 修改字体大小
  ::v-deep .el-tabs__item {
    font-size: 16px;
  }
}

.top {
  height: 2.5rem;
  line-height: 2.5rem;
  position: relative;

  //   搜索表单
  .el-form {
    margin-top: 0.5rem;
    display: flex;

    .el-form-item {
      margin-right: 1rem;
    }

    .el-select {
      width: 6rem;
    }
  }

  span {
    position: absolute;
    font-size: 0.7rem;
    left: 1.7rem;

  }

  .add {
    float: right;
    margin-right: 2vw;
  }
}

.bottom {
  height: 64vh;
  overflow-y: auto;

  li {
    height: 8vh;
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
      font-size: 0.7rem;
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

      .contentInner {
        width: 30rem;
        height: 100%;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }


      // 开始录入按钮
      .info {
        position: absolute;
        left: 78%;
        width: 5.5rem;
        height: 2rem;
      }

      .start {
        position: absolute;
        left: 90%;
        width: 3.2rem;
        height: 1.8rem;
      }

      .delete {
        position: absolute;
        left: 90%;
        width: 3.5rem;
        height: 2rem;
      }
    }
  }

  li:hover {
    background-color: #d2e0f6;
  }
}

// 添加试题类型弹窗
.questypedialog {
  width: 5rem;

  .el-form {
    .el-form-item {
      margin-top: 2rem;
      width: 80%;
    }
  }
}

a {
  text-decoration: none;
  color: black;
}
</style>
