<script setup>
import { ref, nextTick } from 'vue'
import { getAllTestAPI,getFenxiByID } from '../../api/test';
import * as echarts from "echarts";
const activeName = ref('first')

// 单卷分析板块
const oneDialog = ref(false)
const echarsDom1 = ref()
const echarsDom2 = ref()
const echarsDom3 = ref()
const echarsDom4 = ref()
const echarsDom3El = ref('')
const echarsDom4El = ref('')
const userEc3 = ref('')
const userEc4 = ref('')
// 单卷分析饼图数据
const data1 = ref([
  { value: 580, name: '0~59' },
  { value: 1048, name: '60~79' },
  { value: 600, name: '80~89' },
  { value: 300, name: '90~100' },
])
const data2 = ref(['0~59', '60~79', '80~89', '90~100'])
// 单卷分析柱状图y轴数值
const data3 = ref([1, 1, 1, 1, 1, 1])


// 获取所有批改完后的考试
const oneList = ref([])
const getAllOne = async () => {
  const res = await getAllTestAPI()
  oneList.value = res.data.data.filter(item=>item.hasAnswers==3)
}
getAllOne()

const examTitle = ref('')
const max = ref('')
const min = ref('')
const avg = ref('')
const countList = ref([])
// 查看单卷分析
const onLookFenxi = async(exam) => {
  const examId = exam.examId
  const paperId = exam.paperIds.slice(1,-1)
  const res = await getFenxiByID(paperId,examId)

  max.value = res.data.data.max_score
  min.value = res.data.data.min_score
  avg.value = res.data.data.avg_score.toFixed(2)
  countList.value = res.data.data.count


  data1.value[0].value = countList.value.poor_count
  data1.value[1].value = countList.value.normal_count
  data1.value[2].value = countList.value.good_count
  data1.value[3].value = countList.value.perfect_count

  data3.value = [countList.value.poor_count,countList.value.normal_count,countList.value.good_count,countList.value.perfect_count]

  examTitle.value = exam.examName
  oneDialog.value = true


  // 饼图
  var option1 = ref({
    title: {
      text: '成绩分布扇形图',
      subtext: examTitle.value,
      left: 'center'
    },
    tooltip: {
      trigger: 'item'
    },
    legend: {
      top: '85%',
      left: 'center'
    },
    series: [
      {
        name: 'Access From',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        padAngle: 5,
        itemStyle: {
          borderRadius: 20
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 40,
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: data1.value
      }
    ]
  });
  //  柱状图
  var option2 = ref({
    title: {
      text: '成绩分布柱状图',
      subtext:examTitle.value,
      left: 'center'
    },
    tooltip: {
      // 坐标轴指示器
      azisPointer: {
        type: "shadow",
      },
    },
    xAxis: {
      type: 'category',
      data: data2.value
    },
    yAxis: { type: 'value' },
    series: [
      {
        name: '分数',
        type: 'bar',
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#83bff6' },
            { offset: 0.5, color: '#188df0' },
            { offset: 1, color: '#188df0' }
          ])
        },
        data: data3.value,
      }
    ],
  })


  // 等待DOM渲染后再进行操作
  nextTick(() => {
    let echarsDom1El = echarsDom1.value;
    let echarsDom2El = echarsDom2.value;
    let userEc1 = echarts.init(echarsDom1El, "light");
    let userEc2 = echarts.init(echarsDom2El, "light");
    // 使用刚指定的配置项和数据显示图表。
    userEc1.setOption(option1.value);
    userEc2.setOption(option2.value);
  })
}






// 多卷分析板块
const twoDialog = ref(false)
const examList = ref([])
// 将选中的考试装入数组，取消选中的考试拿出数组
const onChange = (check, one) => {
  console.log(check, one)
  if (check) {
    examList.value.push(one)
  } else {
    examList.value.splice(examList.value.indexOf(one), 1)
  }
}
const onLookTwoFenxi = () => {
  twoDialog.value = true
  // 多个柱形图
  var option1 = {
    title: {
      text: '多卷成绩分布统计图',
      left: 'center'
    },
    legend: {
      top: '90%',
      left: 'center'
    },
    tooltip: {},
    dataset: {
      source: [
        ['product', '3.17考试测试1', '3.17考试测试2', '3.17考试测试3', '3.17考试测试4'],
        ['0~59', 43.3, 85.8, 93.7, 30],
        ['60~79', 83.1, 73.4, 55.1, 35],
        ['80~89', 86.4, 65.2, 82.5, 24],
        ['90~100', 72.4, 53.9, 39.1, 40]
      ]
    },
    xAxis: { type: 'category' },
    yAxis: {},
    series: [{ type: 'bar' }, { type: 'bar' }, { type: 'bar' }, { type: 'bar' }]
  }

  // 折线图
  var option2 = {
    title: {
      text: '多卷最低分、平均分、最高分折线图'
    },
    xAxis: {
      type: 'category',
      data: ['最低分', '平均分', '最高分']
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        data: [20, 67, 91],
        type: 'line'
      },
      {
        data: [32, 77, 98],
        type: 'line'
      },
      {
        data: [23, 80, 91],
        type: 'line'
      },
      {
        data: [10, 70, 88],
        type: 'line'
      }
    ]
  }
  // 等待DOM渲染后再进行操作
  nextTick(() => {
    echarsDom3El.value = echarsDom3.value;
    echarsDom4El.value = echarsDom4.value;
    userEc3.value = echarts.init(echarsDom3El.value, "light");
    userEc4.value = echarts.init(echarsDom4El.value, "light");
    // 使用刚指定的配置项和数据显示图表
    userEc3.value.setOption(option1);
    userEc4.value.setOption(option2);
  })
}
</script>
<template>
  <div class="topTitle">
    分析
  </div>
  <div class="container">
    <el-tabs v-model="activeName" class="demo-tabs" @tab-click="handleClick">
      <!-- <el-tab-pane label="单卷分析" name="first"> -->
        <el-empty class="bottom" v-if="oneList.length === 0" :image-size="200" />
        <ul class="bottom">
          <li v-for="one in oneList">
            <a href="javascript:;" @click="onLookFenxi(one)">
              <!-- <svg class="icon testIcon" aria-hidden="true">
                <use xlink:href="#icon-a-044_shujutongji"></use>
              </svg> -->
              <el-button color="#045afe" plain type="success">分析</el-button>
              <div class="content">
                {{ one.examName }}
                <el-button @click="onLookFenxi(one)" class="start" type="primary" color="#045afe">查看分析</el-button>
              </div>
            </a>
          </li>
        </ul>
      <!-- </el-tab-pane> -->
      <!-- <el-tab-pane label="多卷分析" name="two">
        <div class="top">
          <el-checkbox v-model="checkAll" @change="handleCheckAllChange"></el-checkbox>
          <span>已选 2</span>
          <el-button @click="onLookTwoFenxi" type="danger" class="topbtn" plain>开始分析</el-button>
        </div>

        <el-empty class="bottom" v-if="oneList.length === 0" :image-size="200" />
        <ul class="bottom">
          <li v-for="one in oneList">
            <a href="javascript:;">
              <el-checkbox @change="(value) => {
                onChange(value, one)
              }"></el-checkbox>
              <svg class="icon testIcon" aria-hidden="true">
                <use xlink:href="#icon-a-044_shujutongji"></use>
              </svg>
              <div class="content">
                {{ one.examName }}
              </div>
            </a>
          </li>

        </ul>
      </el-tab-pane> -->
    </el-tabs>
  </div>

  <!-- 弹窗1 -->
  <el-dialog class="one" v-model="oneDialog" width="55rem">
    <div class="title">{{ examTitle }}</div>
    <div class="box">
      <div class="left" ref="echarsDom1"></div>
      <div class="right" ref="echarsDom2"></div>
    </div>
    <div class="box2">
      <el-descriptions size="large" class="right" :column="1" border>

        <el-descriptions-item>
          <template #label>
            <div>最高分</div>
          </template>
          {{ max }}
        </el-descriptions-item>

        <el-descriptions-item>
          <template #label>
            <div>最低分</div>
          </template>
          {{ min }}
        </el-descriptions-item>

        <el-descriptions-item>
          <template #label>
            <div>平均分</div>
          </template>
          {{ avg }}
        </el-descriptions-item>


      </el-descriptions>
    </div>
  </el-dialog>
  <!-- 弹窗2 -->
  <el-dialog class="two" v-model="twoDialog" width="55rem">
    <div class="title">多卷分析</div>
    <div class="box">
      <div class="left" ref="echarsDom3"></div>
      <div class="right" ref="echarsDom4"></div>
    </div>
  </el-dialog>
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

  .el-button.topbtn {
    position: absolute;
    left: 6rem;
    top: 0;
    bottom: 0;
    margin: auto;
  }

  //   搜索表单
  .el-form {
    margin-top: 0.5rem;
    display: flex;

    .el-form-item {
      margin-right: 1rem;
    }

    .el-select {
      width: 8rem;
    }

    .el-input {
      width: 8rem;
    }
  }
}

.bottom {
  li {
    height: 4rem;
    line-height: 4rem;
    position: relative;

    a {
      display: block;
      color: black;
    }

    // 图形
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

      .start {
        position: absolute;
        left: 85%;
        width: 5rem;
        height: 2rem;
        font-size: 0.7rem;
      }

    }
  }

  li:hover {
    background-color: #d2e0f6;
  }
}

.one,
.two {

  .title {
    text-align: center;
    font-size: 1.5rem;
    margin-bottom: 2rem;
  }

  .box {
    overflow: hidden;
    justify-content: space-evenly;

    .left {
      margin-left: 2rem;
      float: left;
      box-sizing: border-box;
      width: 20rem;
      height: 20rem;
      border-radius: 10px;
      border: 1px solid rgba(0, 0, 0, 0.5);
    }

    .right {
      margin-right: 2rem;
      float: right;
      box-sizing: border-box;
      width: 20rem;
      height: 20rem;
      border-radius: 10px;
      border: 1px solid rgba(0, 0, 0, 0.5);
    }
  }

  .box2 {
    margin: 0 auto;
    width: 30rem;
    margin-top: 1rem;
    background-color: pink;
  }
}

.two {
  .title {
    text-align: center;
    font-size: 1.5rem;
    margin-bottom: 2rem;
  }

  .box {
    overflow: hidden;
    justify-content: space-evenly;

    .left {
      margin-left: 2rem;
      float: left;
      box-sizing: border-box;
      width: 23rem;
      height: 23rem;
      border-radius: 10px;
      border: 1px solid rgba(0, 0, 0, 0.5);
    }

    .right {
      margin-right: 2rem;
      float: right;
      box-sizing: border-box;
      width: 23rem;
      height: 23rem;
      border-radius: 10px;
      border: 1px solid rgba(0, 0, 0, 0.5);
    }
  }
}
</style>