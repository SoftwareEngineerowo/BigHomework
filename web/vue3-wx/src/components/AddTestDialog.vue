<script setup>
import { ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { addExamAPI, getAllPaperAPI, addExamBeforeAPI, addExamAfterAPI } from '@/api/test.js'
const dialogVisible = ref(false)

const examId = ref('')
//open
const open = async (row) => {
  dialogVisible.value = true
  // 开局获得一个壳子
  const res = await addExamBeforeAPI()
  examId.value = res.data.data.examId
}
defineExpose({ open })


// 日历时间部分
const time1 = ref(new Date())
const time2 = ref('')

// 选择试卷部分
const centerDialogVisible = ref(false)
// 穿梭框 初始化data数据
const transList = ref([])
const paperList = ref([])
const data = ref([])
const getAllPaper = async () => {
  const res = await getAllPaperAPI()
  paperList.value = res.data.data
  data.value = paperList.value.map((paper) => {
    return {
      key: paper.paperId,
      label: paper.paperName,
    }
  })
}
getAllPaper()
// 确定选择试卷
// 已选择的试卷数组
const showList = ref([])
const onPaperConfirm = () => {
  showList.value = paperList.value.map((paper) => {
    if (transList.value.indexOf(paper.paperId) !== -1) {
      return paper
    }
  })
  centerDialogVisible.value = false
  ElMessage.success("选择试卷成功")
}

// 提交部分
const formRef = ref()
//表单数据
const formModel = ref({})
//校验
const rules = {

}
const emit = defineEmits(['success'])
const onSubmit = async () => {
  // 判断试卷的选择
  if(transList.value.length==0){
    ElMessage.error("请选择试卷")
    return
  }
  if(transList.value.length>1){
    ElMessage.error("只能选择一张试卷")
    return
  }
  // 判断时间的选择
  if(time1.value==''||time2.value==''){
    ElMessage.error("请选择时间")
    return
  }
  // 构建时间参数
  const m1 = time2.value[0].getMinutes() < 10 ? '0' + time2.value[0].getMinutes() : time2.value[0].getMinutes()
  const m2 = time2.value[1].getMinutes() < 10 ? '0' + time2.value[1].getMinutes() : time2.value[1].getMinutes()

  const t1 = time1.value.getFullYear() + '/' + (time1.value.getMonth() + 1) + '/' + time1.value.getDate() + ' ' + time2.value[0].getHours() + ':' + m1
  const t2 = time1.value.getFullYear() + '/' + (time1.value.getMonth() + 1) + '/' + time1.value.getDate() + ' ' + time2.value[1].getHours() + ':' + m2

  const data1 = {
    examId: examId.value,
    examName: formModel.value.examName,
    paperIds: "[" + transList.value + "]",
    examTimes: "{'1':'" + t1 + "','2':'" + t2 + "'}"
  }
  console.log("这是请求添加考试内容的参数")
   await addExamAPI(data1)
  dialogVisible.value = false
  ElMessage.success("添加考试成功")
  // 向父组件发送信息提醒父组件重新渲染考试部分
  emit('success')
}
// 取消
const onCancel = async () => {
  console.log("取消取消取消")
  dialogVisible.value = false
   await addExamAfterAPI(examId.value)
}
</script>
<template>
  <el-dialog v-model="dialogVisible" :title="formModel.id ? '编辑' : '新建'" width="30%">
    <el-form ref="formRef" :rules="rules" :model="formModel">

      <el-form-item class="name" prop="examName" label="考试名称 ">
        <el-input v-model="formModel.examName" placeholder="请输入考试名称" autocomplete="off" />
      </el-form-item>

      <!-- 选择考试时间 -->
      <el-form-item label="月份日期">
        <el-calendar v-model="time1">
          <template #date-cell="{ data }">
            <p :class="data.isSelected ? 'is-selected' : ''">
              {{ data.day.split('-').slice(1).join('-') }}
              {{ data.isSelected ? '✔️' : '' }}
            </p>
          </template>
        </el-calendar>
      </el-form-item>

      <el-form-item class="time" label="具体时间">
        <el-time-picker @change="onChangeTime2" v-model="time2" is-range range-separator="To"
          start-placeholder="Start time" end-placeholder="End time" />
      </el-form-item>

      <!-- 选择考试试卷 -->
      <el-form-item class="paper" label="选择试卷">
        <ul>
          <li v-for="show of showList" :key="show?.paperId">{{ show?.paperName }}</li>
        </ul>
        <el-button @click="centerDialogVisible = true" type="success">选 择</el-button>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="onCancel">取消</el-button>
        <el-button @click="onSubmit" color="#045afe">确认</el-button>
      </span>
    </template>
  </el-dialog>
  <!-- 穿梭层弹出框 -->
  <el-dialog v-model="centerDialogVisible" title="选择考试试卷" width="500" center>
    <el-transfer @change="onChange" v-model="transList" :data="data" :titles="['未选择', '已选择']" />
    <el-button @click="onPaperConfirm" class="btn"  color="#045afe">确定选择</el-button>
    <el-button @click="centerDialogVisible = false" class="btn">取消</el-button>
  </el-dialog>
</template>
<style lang="scss">
.el-dialog {
  width: 60%;
  // height: 35rem;
}

// 考试名称
.name {
  width: 50%;
}

// 日历
.el-calendar {
  width: 30rem;

  .el-calendar-day {
    height: 2rem;
  }
}

// 具体时间
.time {
  width: 50%;
}

// 选择试卷按钮
.paper {
  ul {
    margin: 0 2rem;
  }

  .el-button {
    width: 6rem;
    height: 3rem;
  }
}

// 穿梭框
.el-transfer {
  .el-transfer-panel {
    width: 15rem;
  }
}

.el-dialog {
  // 开启BFC
  overflow: hidden;
}

.btn {
  margin-top: 1rem;
  float: right;
  margin-bottom: 1rem;
  margin-right: 1rem;
}
</style>
