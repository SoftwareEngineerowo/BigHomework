<script setup>
import { getAllTestAPI, getExamById, getPaperByIdAPI } from '../../api/test';
import { getSheetScoreByExamIdAPI } from '@/api/read.js'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()
const activeName = ref('first')

// 阅卷部分
const examId = ref('')
const paperId = ref('')
const quesList = ref([])

// 阅卷界面展示
const readPaperList = ref([])
const getReadPaperList = async () => {
  const res = await getAllTestAPI()
  readPaperList.value = res.data.data.filter((item) => item.hasAnswers == 2)
}
getReadPaperList()

// 开始阅卷 将考试id,试卷id和试题数组切换为点击的
const onStartRead = async (readPaper) => {
  // 获取考试id
  examId.value = readPaper.examId

  // 获取试卷id
  const res1 = await getExamById(examId.value)
  paperId.value = res1.data.data.paperIds.slice(1, -1)

  // 获取题目数组
  const res2 = await getPaperByIdAPI(paperId.value)
  quesList.value = res2.data.data.quesIds.slice(1, -1).split(',')

  // 跳转到详细阅卷界面并传递examId、paperId、quesList
  router.push({
    path: '/readshow',
    query: {
      examId: examId.value,
      paperId: paperId.value,
      quesList: quesList.value
    }
  })
}


// 评阅结果部分
// 评阅结果界面展示
const readResultList = ref([])
const getReadResultList = async () => {
  const res = await getAllTestAPI()
  readResultList.value = res.data.data.filter((item) => item.hasAnswers == 3)
}
getReadResultList()
// 点击哪个考试就根据examId查询所有考试学生成绩
const tableData = ref([])
const onClickReadResult = async (readResult) => {
  tableData.value = []
  const res = await getSheetScoreByExamIdAPI(readResult.examId)
  const data = res.data.data
  data.forEach((item) => {
    const obj = {}
    obj.certId = item[1]
    obj.stuId = item[2]
    obj.stuName = item[3]
    obj.finalScore = item[5]
    tableData.value.push(obj)
  })
}
</script>
<template>
  <div class="topTitle">
    阅卷
  </div>
  <div class="container">
    <el-tabs v-model="activeName" class="demo-tabs" @tab-click="handleClick">
      <el-tab-pane label="阅卷" name="first">
        <el-empty class="bottom" v-if="readPaperList.length === 0" :image-size="200" />
        <ul class="bottom">
          <li v-for="readPaper of readPaperList" :key="readPaper.examId">
            <a href="javascript:;">
              <el-button color="#045afe" plain type="success">阅卷</el-button>
              <div class="content">
                {{ readPaper.examName }}
                <el-button @click="onStartRead(readPaper)" class="start" type="primary" plain>开始阅卷</el-button>
              </div>
            </a>
          </li>
        </ul>
      </el-tab-pane>
      <el-tab-pane label="评阅结果" name="two">
        <el-empty class="bottom" v-if="readResultList.length === 0" :image-size="200" />
        <el-collapse accordion>
          <el-collapse-item @click="onClickReadResult(readResult)" :name="readResult.examId"
            v-for="readResult in readResultList" :key="readResult.examId">
            <template #title>
              <el-button color="DodgerBlue" plain type="success">结果</el-button>
              <span class="title">
                {{ readResult.examName }}
              </span>
            </template>
            <div>
              <el-table :default-sort="{ prop: 'date', order: 'descending' }" :data="tableData" border
                style="width: 100%">
                <el-table-column prop="stuId" label="学号" />
                <el-table-column prop="certId" label="准考证号" />

                <el-table-column label="姓名">
                  <template #default="scope">
                    <el-button type="primary" plain>{{ scope.row.stuName }}</el-button>
                  </template>
                </el-table-column>

                <el-table-column prop="finalScore" label="全卷分数" sortable />
                <el-table-column type="index" label="排名" width="200" />
              </el-table>
            </div>
          </el-collapse-item>
        </el-collapse>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>
<style lang="scss" scoped>
.topTitle {
  height: 7vh;
  line-height: 7vh;
  font-size: 1.6rem;
  font-weight: 100;
}
// 手风琴
.el-collapse {
  .title {
    margin-left: 2rem;
    font-size: 0.9rem;
    display: block;

  }
}
.container{
  background-color: white;
  min-height: 83vh;
}
.el-tabs {
  padding: 2rem;
  ::v-deep .el-tabs__item {
    font-size: 1rem;
  }

}

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
        width: 4rem;
        height: 1.8rem;
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

// 弹窗
.el-dialog {
  .title {
    font: 1rem;
    margin-bottom: 1rem;
    text-align: center;
  }

  .box {
    width: 70%;
    margin: 0 auto;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
  }
}
</style>