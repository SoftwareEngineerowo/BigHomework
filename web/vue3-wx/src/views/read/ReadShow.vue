<script setup>
import { ref } from 'vue'
import { getAllStuByExamIdAPI, getAwQuesByCertIdandQuesIdAPI, addMarkResult, addSheetScoreAPI, getMarkResultByAnswerId, deleteMarkResultByIDAPI } from '@/api/read.js'
import { getTextAPI } from '@/api/texthandle.js'

import { getAICommentAPI, getAIMarkAPI } from '@/api/ai.js'
import { getQuesByIdAPI, getExamById, changePaperStatusAPI } from '@/api/test.js'
import { ElLoading, ElMessage } from 'element-plus'
import { useUserStore } from '../../stores/userStore';
const userStore = useUserStore()
import { useRoute, useRouter } from 'vue-router'
const route = useRoute()
const router = useRouter()
// 获取传递过来的参数
const examId = route.query.examId
const paperId = route.query.paperId
// quesId的数组
const quesList = route.query.quesList

const quesId = ref('')
const answerId = ref('')
const cert = ref('')

// 控制是否显示学生姓名
const isShowName = ref(true)
// 根据examId获取考试学生数组和考试名称用于渲染
const stuList = ref([])
const examName = ref('')
const getAllStuByExamId = async (id) => {
    const res = await getAllStuByExamIdAPI(String(id))
    stuList.value = res.data.data
    const res2 = await getExamById(id)
    examName.value = res2.data.data.examName
}
getAllStuByExamId(examId)


// 渲染中间部分内容
const centData = ref({
    quesId: '',
    quesKindId: '',
    quesContent: '',
    quesAnswer: '',
    quesDefaultScore: '',
    ansImg: '',
    answer: ''
})
const studentData = ref({})
const quesIndex = ref()
const AIComment = ref([''])
const TeacherComment = ref('')
const AIScore = ref('')
const TeacherScore = ref('')
const ID = ref('')
const sindex = ref('')
// 控制a的类名动态添加的变量
const activeIndex1 = ref(-1)
const activeIndex2 = ref(-1)
// 控制折叠自动打开的变量
const activeNames = ref(-1)

// 点击学生获取该学生对应题目的答题模型
const onClickStu = async (ques, stu, index, SIndex) => {
    activeIndex1.value = index;
    activeIndex2.value = SIndex;
    cert.value = stu.certId
    sindex.value = SIndex
    const loadingInstance1 = ElLoading.service({ fullscreen: true })
    // 根据试题id和准考证id查询答卷模型
    const res = await getAwQuesByCertIdandQuesIdAPI(stu.certId, ques)
    answerId.value = res.data.data.answerId
    quesId.value = res.data.data.quesId
    // 根据试题id查询试题模型,给centerData赋值
    const res1 = await getQuesByIdAPI(ques)
    centData.value = res1.data.data
    centData.value.ansImg = res.data.data.ansImg
    console.log(centData.value)
    // 将学生更新和题号更新
    studentData.value = studentData.value = stu
    quesIndex.value = index + 1
    fn()
    loadingInstance1.close()

}
// 点击学生后的后续步骤
const fn = async () => {
    // 将答案图片请求文字识别
    const formData = new FormData()
    formData.append('img', centData.value.ansImg)
    formData.append('typ', 'INFO')
    const res2 = await getTextAPI(formData)
    centData.value.answer = res2.data.res
    // 根据answerId查询单题打分结果
    const res3 = await getMarkResultByAnswerId(answerId.value)
    // 将AI评价等赋值方便渲染到页面中
    if (res3.data.data.length > 0) {
        ID.value = res3.data.data[0].id
        AIComment.value[0] = res3.data.data[0].AIComment
        AIScore.value = res3.data.data[0].AIScore
        TeacherScore.value = res3.data.data[0].TeacherScore
        TeacherComment.value = res3.data.data[0].TeacherComment
    } else {
        AIComment.value = ['']
        AIScore.value = ''
        TeacherScore.value = ''
        TeacherComment.value = ''
    }
}
// 获取AI打分
const getAIScore = async () => {
    const formData = new FormData()
    formData.append('question', centData.value.quesContent)
    formData.append('full', centData.value.quesDefaultScore)
    formData.append('answer', centData.value.answer)
    formData.append('correct', centData.value.quesAnswer)
    const loadingInstance1 = ElLoading.service({ fullscreen: true })
    const res = await getAIMarkAPI(formData)
    AIScore.value = res.data.score
    AIComment.value[0] = res.data.reson
    console.log(AIScore.value)
    loadingInstance1.close()
}
// 重新获取AI评价
const getAIComment = async () => {
    const formData = new FormData()
    formData.append('question', centData.value.quesContent)
    formData.append('answer', centData.value.answer)
    formData.append('correct', centData.value.quesAnswer)
    formData.append('count', 1)
    const loadingInstance1 = ElLoading.service({ fullscreen: true })
    const res = await getAICommentAPI(formData)
    AIComment.value[0] = res.data[0]
    loadingInstance1.close()
}
// 电话按键功能
const keypadNumbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
const addToInput = (num) => {
    TeacherScore.value += num

}
const onDeleteNum = () => {
    TeacherScore.value = ''
}
// 批改完成，提交单题目阅卷结果
const onFinish = async () => {
    // 处理时间
    const now = new Date();
    const year = now.getFullYear();
    const month = now.getMonth() + 1
    const day = now.getDate()
    const hours = ('0' + now.getHours()).slice(-2);
    const minutes = ('0' + now.getMinutes()).slice(-2);
    const time = year + '/' + month + '/' + day + ' ' + hours + ':' + minutes
    // 请求参数
    const data = {
        examId: examId,
        paperId: paperId,
        quesId: quesId.value,
        answerId: answerId.value,
        marKTime: time,
        teaId: userStore.userInfo.roleId,
        AIScore: AIScore.value || 0,
        TeacherScore: TeacherScore.value || 0,
        AIComment: AIComment.value[0] ||'',
        TeacherComment: TeacherComment.value || '',
    }
    const res = await addMarkResult(data)
    // 获取本题打分id
    if (res.data.code === 200) {
        ID.value = res.data.data.id
    }
    ElMessage.success("批改完成")
}
// 下一份按钮逻辑
const onNext = () => {
    // 如果该学生为本题最后一位
    if (sindex.value === stuList.value.length - 1) {
        // 下一份：题目是下一道，学生重置为第一位
        onClickStu(quesList[quesIndex.value], stuList.value[0], quesIndex.value, 0)
    } else {
        // 正常情况  题目不变，学生为下一位
        onClickStu(quesList[quesIndex.value - 1], stuList.value[sindex.value + 1], quesIndex.value - 1, sindex.value + 1)
    }
}
// 删除打分结果
const onDeleteMarkResult = async () => {
    const res = await deleteMarkResultByIDAPI(ID.value)
    ElMessage.success("删除成功")
    AIComment.value = ['']
    AIScore.value = ''
    TeacherScore.value = ''
    TeacherComment.value = ''
}

// 提交总阅卷结果（假设一个老师改全卷）
const onComfirmResult = async () => {
    const loadingInstance1 = ElLoading.service({ fullscreen: true })
    for (let stu of stuList.value) {
        let finalScore = 0
        let detailScores = []

        for (let quesId of quesList) {
            const res = await getAwQuesByCertIdandQuesIdAPI(stu.certId, quesId)
            const answerId = res.data.data.answerId
            // 根据answerId获取单题打分结果
            const res2 = await getMarkResultByAnswerId(answerId)
            const score = res2.data.data[0].TeacherScore ? res2.data.data[0].TeacherScore : 0
            finalScore += score || 0
            detailScores.push(score)
        }

        const data = {
            examId: examId,
            paperId: paperId,
            certId: stu.certId,
            detailScores: '[' + detailScores.join(',') + ']',
            finalScore: finalScore,
        }

        // 添加单卷分数
        const res3 = await addSheetScoreAPI(data)
        console.log(res3.data)
    }
    loadingInstance1.close()
    ElMessage.success("提交成功")
    // 更改试卷状态
    await changePaperStatusAPI(examId, 3)
    router.push('/read')
}

</script>
<template>
    <div class="box">
        <div class="header">
            <div class="left">
                <el-page-header @click="$router.go(-1)" :icon="ArrowLeft">
                    <template #content>
                        <span>阅卷</span>
                        <span>{{ examName }}</span>
                    </template>
                </el-page-header>
            </div>
            <div class="right">
                <el-button @click="onComfirmResult" size="large" color="#045afe">提交阅卷结果</el-button>
            </div>
        </div>
        <div class="main">
            <!-- 学生名单渲染 -->
            <div class="left">
                <el-scrollbar>
                    <el-collapse v-model="activeNames" @change="handleChange">
                        <div class="tip">是否显示学生姓名</div>
                        <div class="switch"> <el-switch v-model="isShowName" size="large" active-text="Open"
                                inactive-text="Close" /></div>

                        <el-collapse-item v-for="(ques, QIndex) of quesList" :name="QIndex" :key="QIndex">
                            <template #title>
                                <span class="title">
                                    第{{ QIndex + 1 }}题
                                </span>
                            </template>
                            <ul>
                                <li @click="onClickStu(ques, stu, QIndex, SIndex)" v-for="(stu, SIndex) of stuList"
                                    :key="stu.id">
                                    <a :class="{ active: activeIndex1 == QIndex && activeIndex2 == SIndex }"
                                        href="javascript:;" v-if="!isShowName">{{ SIndex+1 }}号学生</a>
                                    <a :class="{ active: activeIndex1 == QIndex && activeIndex2 == SIndex }"
                                        href="javascript:;" v-if="isShowName">{{ stu.stuName }}</a>
                                </li>
                            </ul>
                        </el-collapse-item>
                    </el-collapse>
                </el-scrollbar>

            </div>
            <div class="center">
                <div class="top">
                    <el-button v-if="!quesIndex" type="primary" plain size="large"> 请从左侧选择待批改试题以及学生</el-button>
                    <div class="btn" v-if="quesIndex">
                        <el-button type="primary" plain size="large">第{{ quesIndex }}题</el-button>
                        <el-button type="danger" plain size="large">单选题</el-button>
                        <el-button type="success" plain size="large" v-if="isShowName">{{ studentData.stuName }}</el-button>
                        <el-button type="success" plain size="large" v-if="!isShowName">{{ studentData.stuId }}</el-button>
                    </div>
                    <div class="content" v-if="quesIndex">
                        <el-button size="large" color="rgb(29, 75, 131)" plain> 参考答案:{{ centData.quesAnswer
                        }}</el-button>

                    </div>
                </div>
                <div class="ret">
                    <img :src="centData.ansImg" alt="">
                </div>
                <div class="bottom">
                    <div class="score">
                        <div class="score-top">
                            <div class="num">
                                <span>AI打分:</span>
                                <el-input v-model="AIScore"></el-input>
                                <span>老师打分:</span>
                                <el-input v-model.number="TeacherScore" placeholder="请输入分数"></el-input>
                            </div>
                            <div class="btn">
                                <el-button @click="getAIScore" class="wenti" color="#045afe">AI评阅</el-button>
                            </div>
                        </div>
                        <div class="score-bottom">
                            <div class="num">
                                <div class="keypad">
                                    <el-button v-for="num in keypadNumbers" :key="num" @click="addToInput(num)">
                                        {{ num }}
                                    </el-button>
                                </div>
                            </div>
                            <div class="btn">
                                <a-button class="a" @click="onDeleteNum">清空</a-button>
                                <a-button class="a" @click="TeacherScore = 0">0分</a-button>
                                <a-button class="a" @click="TeacherScore = centData.quesDefaultScore">满分</a-button>
                            </div>
                        </div>
                    </div>
                    <div class="comment">
                        <div class="comment1">
                            <div class="title">AI评价:</div>
                            <el-input :value="AIComment[0]" :autosize="{ minRows: 6, maxRows: 10 }" type="textarea" />
                        </div>
                        <div class="comment2">
                            <div class="title">老师评价:</div>
                            <el-input v-model="TeacherComment" :autosize="{ minRows: 6, maxRows: 10 }" type="textarea"
                            placeholder="手动输入评价" />
                        </div>
                    </div>
                    <div class="button">
                        <a-button @click="getAIComment">重置评价</a-button>
                        <el-button @click="onFinish" size="large">批改完成</el-button>
                        <el-button :disabled="ID == ''" @click="onDeleteMarkResult" size="large" plain
                            type="danger">删除打分结果</el-button>
                            <el-button :disabled="quesIndex == quesList.length && sindex == stuList.length - 1" size="large"
                            type="info" @click="onNext" color="#045afe">下一份</el-button>
                    </div>
                    <!-- <el-form>
                        <el-form-item>
                            <div v-if="AIScore != ''">
                                AI建议: {{ AIScore }}分
                            </div>
                            <el-button @click="getAIScore" class="wenti" type="success">AI评阅</el-button>
                            <el-button type="primary" @click="TeacherScore = 0">0分</el-button>
                            <el-button type="danger" @click="TeacherScore = centData.quesDefaultScore">满分</el-button>
                        </el-form-item>
                        <el-form-item lable="老师打分:">
                            <el-input v-model.number="TeacherScore" placeholder="请输入分数"></el-input>
                            <el-button type="danger" @click="onDeleteNum">删除</el-button>
                        </el-form-item>
                        <el-form-item>
                            <div class="keypad">
                                <el-button v-for="num in keypadNumbers" :key="num" @click="addToInput(num)">
                                    {{ num }}
                                </el-button>
                            </div>
                        </el-form-item>
                    </el-form>
                    <el-tabs tab-position="left">
                        <el-tab-pane label="AI评价" v-for="comment of AIComment" :key="comment">
                            <el-input :value="comment" :autosize="{ minRows: 6, maxRows: 7 }" type="textarea" />
                            <el-button @click="getAIComment" type="success" v-if="comment != ''">重新获取评价</el-button>
                        </el-tab-pane>
                    </el-tabs>
                    <div class="comment">
                        <el-input v-model="TeacherComment" :autosize="{ minRows: 4, maxRows: 10 }" type="textarea"
                            placeholder="手动输入评价" />
                    </div>
                    <div class="end">
                        <el-button @click="onFinish" size="large" type="success">批改完成</el-button>
                        <el-button :disabled="quesIndex == quesList.length && sindex == stuList.length - 1" size="large"
                            type="info" @click="onNext">下一份</el-button>
                        <el-button :disabled="ID == ''" @click="onDeleteMarkResult" size="large"
                            type="danger">删除打分结果</el-button>
                    </div> -->
                </div>
            </div>
        </div>
    </div>
</template>
<style scoped lang="scss">
.header {
    text-align: center;
    font-size: 1rem;
    display: flex;
    width: 100%;
    height: 3rem;
    justify-content: space-between;
    color: #045afe;
    background-color: #fff;

    .left {
        margin-top: 1rem;
        margin-left: 3rem;
        line-height: 3rem;
        width: 20rem;
        .el-page-header {
            span {
                font-size: 0.8rem;
                margin-right: 1rem;
                color: #045afe;
            }
        }
    }

    .right {
        line-height: 3rem;
        margin-right: 5rem;
    }
}

.main {
    background-color: #f1f1f1;
    display: flex;

    // 左侧名字部分
    .left {
        width: 13%;
        box-sizing: border-box;
        background-color: #fff;
        height: 94vh;
        overflow-y: scroll;

        // 手风琴
        .el-collapse {
            margin-top: 1rem;

            .tip {
                font-size: 0.8rem;
                margin-top: 0.5rem;
                text-align: center;
            }

            .switch {
                text-align: center;
            }


            .title {
                margin-left: 1rem;
                font-size: 20px;
                display: block;
            }
        }

        li {
            list-style: none;
            line-height: 4rem;
            height: 4rem;
            font-size: 1rem;
            border-bottom: 1px solid rgba(0, 0, 0, 0.1);
            box-sizing: border-box;

            a {
                text-decoration: none;
                color: black;
                display: block;
                text-align: center;
            }

            a:hover {
                background-color: rgb(18, 68, 139);
                color: white;
            }

            a.active {
                background-color: rgb(18, 68, 139);
                color: white;
            }
        }
    }

    // 中间内容区域
    .center {
        background-color: #fff;
        margin: 0rem 1rem;
        margin-top: 1rem;
        border-radius: 10px;
        position: relative;
        width: 84vw;

        // 题目
        .top {
            height: 18vh;
            box-sizing: border-box;
            padding-top: 2rem;
            display: flex;
            border-bottom: 1px solid rgba(0, 0, 0, 0.1);
            box-sizing: border-box;
            padding-left: 2rem;
            justify-content: space-between;

            .content {
                word-break: break-all;
                width: 50%;
                font-size: 0.8rem;
                margin-right: 3rem;
                height: 4rem;
                overflow-y: auto;
            }

        }

        // 扫描结果
        .ret {
            height: 44vh;
            overflow-y: auto;
        }

        // 打分评价区域
        .bottom {
            padding: 1vh;
            box-sizing: border-box;
            bottom: 0;
            height: 30vh;
            width: 100%;
            border-top: 1px solid rgba(0, 0, 0, 0.2);
            box-sizing: border-box;
            display: flex;

            // 打分区域
            .score {
                width: 30%;
                height: 100%;
                display: flex;
                flex-direction: column;
                justify-content: space-around;
                align-items: center;
                box-sizing: border-box;
                // background-color: pink;

                .score-top {
                    width: 100%;
                    height: 35%;
                    display: flex;
                    .num {
                        width: 70%;
                        height: 100%;
                        display: flex;
                        flex-direction: column;
                        justify-content: space-between;
                        .el-input {
                            width: 90%;
                            height: 1.7rem;
                        }
                        span {
                            font-size: 14px;
                            color: rgb(117, 116, 116);
                        }
                    }

                    .btn {
                        position: relative;
                        width: 30%;
                        height: 100%;

                        .el-button {
                            height: 50%;
                            position: absolute;
                            top: 0;
                            bottom: 0;
                            left: 0;
                            right: 0;
                            margin: auto;
                            font-size: 18px;
                        }
                    }
                }

                // 数字框区域
                .score-bottom {
                    width: 100%;
                    height: 65%;
                    display: flex;
                    .num {
                        width: 70%;
                        height: 100%;
                        position: relative;
                        // 数字按键
                        .keypad {
                            display: flex;
                            flex-wrap: wrap;
                            justify-content: space-around;
                            align-items: stretch;
                            position: absolute;
                            margin: auto;
                            height: 90%;
                            width: 90%;
                            top: 0;
                            bottom: 0;
                            left: 0;
                        }

                        .keypad .el-button {
                            flex: 1 1 calc(33.333% - 20px);
                            margin: 10px;
                            box-sizing: border-box;
                            height: 2rem;
                            font-size: 20px;
                            background-color: #045afe;
                            color: white;
                        }
                    }

                    .btn {
                        margin: 0;
                        width: 30%;
                        height: 100%;
                        display: flex;
                        flex-direction: column;
                        justify-content: space-evenly;
                        .a{
                           margin: 0;
                           height: 20%;
                           width: 90%;
                           font-size: 18px;
                        }
                    }
                }
            }

            .comment {
                width: 70%;
                height: 100%;
                display: flex;
                justify-content: space-around;
                align-items: center;
                box-sizing: border-box;
                .comment1, .comment2{
                    padding-top: 2rem;
                     width: 40%;
                     height: 100%;
                     display: flex;
                     flex-direction: column;
                     box-sizing: border-box;
                     .title{
                        margin-bottom: 0.8rem;
                        font-size: 16px;
                     }
                }
            }

            .button {
                width: 20%;
                height: 100%;
                display: flex;
                flex-direction: column;
                justify-content: space-around;
                align-items: center;
                box-sizing: border-box;

                color: white;
                .ant-btn{
                    margin: 0;
                    width: 70%;
                    height: 18%;
                    font-size: 18px;
                }
                .el-button{
                    margin: 0;
                    width: 70%;
                    height: 18%;
                    font-size: 18px;
                }
            }

        }
    }

    // 右侧题号部分
    .right {
        padding: 1rem;
        box-sizing: border-box;
        font-size: 0.8rem;
        width: 20%;
        background-color: white;
        margin-top: 1rem;
        margin-right: 1rem;
        border-radius: 10px;
        overflow-y: scroll;
        height: 91vh;

        .box {
            display: flex;
            flex-wrap: wrap;
            margin-top: 0.5rem;
            margin-bottom: 2rem;
        }

        a {
            display: block;
            margin-top: 1rem;
            margin-right: 0.7rem;
        }

        .num {
            display: inline-block;
            background-color: dodgerblue;
            width: 2rem;
            height: 2rem;
            line-height: 2rem;
            text-align: center;

            color: white;
            border-radius: 5px;
        }
    }
}</style>