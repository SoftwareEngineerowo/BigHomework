<script setup>
import { ref } from 'vue'
import AssignDrawer from '@/components/AssignDrawer.vue';
import { addMarkAPI } from '../../api/read.js';
import { getExamById, getPaperByIdAPI, changePaperStatusAPI } from '../../api/test.js';
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore.js'
import { ElMessage } from 'element-plus';
const userStore = useUserStore()
const route = useRoute()
const router = useRouter()

const examId = route.query.examId
const paperId = ref('')

// 根据考试id获取题目数组
const quesList = ref([])
const getQuesList = async () => {
    // 获取试卷id
    const res1 = await getExamById(examId)
    paperId.value = res1.data.data.paperIds.slice(1, -1)
    // 获取题目数组
    const res2 = await getPaperByIdAPI(paperId.value)
    quesList.value = res2.data.data.quesIds.slice(1, -1).split(',')
}
getQuesList()


const copyDialog = ref(false)
// 阅卷分配结果
const taskAllos = ref([])
// 复制分配信息
const onCopyInfo = () => {
    copyDialog.value = true
}
// 复制弹窗
const onCopyComfirm = () => {
    copyDialog.value = false
    ElMessage.success("复制成功")
}
const drawer = ref()
// 设置阅卷分配
const onAssign = () => {
    drawer.value.open()
}

// 右上角提交阅卷分配结果
const onConfirm = async () => {
    // 更改考试状态
    await changePaperStatusAPI(examId, 2)
    ElMessage.success("分配成功")
    router.push('/test')
}


</script>

<template>
    <div class="outer">
        <div class="top">
            <div class="left">
                <el-page-header @click="$router.go(-1)" :icon="ArrowLeft">
                    <template #content>
                        <span class="text-large font-600 mr-3">阅卷分配</span>
                        <span class="text-large font-600 mr-3">2023春数据结构考试</span>
                    </template>
                </el-page-header>
            </div>
            <div class="right">
                <el-button>导入阅卷老师</el-button>
                <el-button @click="onConfirm" type="primary">提交</el-button>
            </div>
        </div>
        <div class="container">
            <div class="bottom">
                <div class="left">
                    <ul class="list">
                        <li v-for="(quesId, index) in quesList" :key="quesId">
                            <a href="javascript:;">
                                <div class="title">第{{ index + 1 }}题</div>
                                <el-divider />
                                <div class="content">
                                    <div class="contentTitle">
                                        <span>阅卷分配</span>
                                        <el-button @click="onCopyInfo">复制分配信息</el-button>
                                        <el-button type="primary" @click="onAssign">设置阅卷分配</el-button>
                                    </div>
                                    <el-divider />
                                    <div class="qita">评分方式:单批</div>
                                    <div class="qita">批改人:何宗欣</div>
                                    <div class="qita">其他批改设置:批改人可查看批改均分</div>
                                </div>
                            </a>
                        </li>
                    </ul>
                </div>
                <div class="right">
                    <div class="box">
                        <div v-for="(quesId, index) in quesList" :key="quesId" class="num">
                            <a href="javascript:;">
                                {{ index + 1 }}
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- 抽屉 -->
    <AssignDrawer ref="drawer"></AssignDrawer>
    <!-- 复制弹窗 -->
    <el-dialog class="copy" v-model="copyDialog" width="500" :before-close="handleClose">
        <div class="title">复制题块设置</div>
        <div class="warn">把<span>第一题</span>的批改设置复制给以下题块</div>

        <div class="all">
            <el-checkbox v-model="checkAll"></el-checkbox>
            <span>全部题块</span>
        </div>

        <div class="box">
            <div class="item" v-for="(quesId, index) of quesList" :key="quesId">
                <el-checkbox @click="onCheckOne"></el-checkbox>
                <span>题目{{ index + 1 }}</span>
            </div>

        </div>
        <div class="end">复制以下内容</div>
        <div class="content">基础批改设置、批改人</div>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="copyDialog = false">取消</el-button>
                <el-button type="primary" @click="onCopyComfirm">
                    确定
                </el-button>
            </div>
        </template>
    </el-dialog>
</template>

<style lang="scss" scoped>
.outer {
    width: 100%;
    background-color: rgb(238, 237, 237);
    padding-bottom: 1rem;
    min-height: 97vh;
}

// 顶部
.top {
    display: flex;
    width: 100%;
    height: 6vh;
    background-color: white;
    position: fixed;
    top: 0;
    left: 0;
    z-index: 99;
    justify-content: space-between;

    .left {
        margin-left: 3rem;
        width: 25rem;
        .el-page-header {
            span {
                line-height: 6vh;
                font-size: 0.8rem;
                margin-right: 3rem;
            }
        }
    }

    .right {
        line-height: 6vh;
        margin-right: 5rem;
    }
}

.container {
    // 高度由内容撑开
    width: 56rem;
    margin: 0 auto;
    text-align: center;
    padding-top: 5rem;

    // 左侧题目部分
    .left {
        width: 35rem;

        .list {
            li {
                box-sizing: border-box;
                height: 16rem;
                border-radius: 10px;
                margin-bottom: 1rem;
                padding: 1rem;
                background-color: white;

                a {
                    box-sizing: border-box;
                    color: black;
                    display: block;
                    width: 100%;
                    height: 100%;
                    text-decoration: none;
                    text-align: left;

                    // 题目
                    .title {
                        margin-bottom: 1.5rem;
                        text-align: center;
                    }

                    .content {

                        // 按钮
                        .contentTitle {
                            span {
                                font-weight: bold;
                            }

                            .el-button {
                                float: right;
                                margin-right: 0.5rem
                            }
                        }

                        // 其他
                        .qita {
                            margin-top: 1.5rem;
                            font-size: 0.8rem;
                        }
                    }

                }
            }

            // li:hover{
            //     border: 1px solid dodgerblue;
            // }
        }
    }

    // 右侧题目详细部分
    .right {
        background-color: white;
        padding: 1rem;
        padding-bottom: 2rem;
        font-size: 0.8rem;
        box-sizing: border-box;
        width: 15rem;
        position: fixed;
        top: 5rem;
        right: 7rem;
        border-radius: 20px;

        .box {
            display: flex;
            flex-wrap: wrap;
            margin-top: 0.5rem;
            box-sizing: border-box;
        }

        a {
            display: block;
            text-decoration: none;
            color: white;
            border-radius: 5px;
        }

        .num {
            margin-top: 1rem;
            margin-left: 1.4rem;
            display: block;
            background-color: dodgerblue;
            width: 2.5rem;
            height: 2.5rem;
            line-height: 2.5rem;
            border-radius: 5px;
        }
    }
}

// 复制弹窗
.copy {
    .title {
        margin-bottom: 1rem;
    }

    .warn {
        margin-bottom: 1rem;

        span {
            font-weight: bold;
        }
    }

    .all {
        height: 1.5rem;
        line-height: 1.5;

        span {
            margin-left: 0.3rem;
        }
    }

    .box {
        display: flex;
        flex-wrap: wrap;

        .item {
            margin-right: 1rem;
            vertical-align: middle;

            span {
                margin-left: 0.3rem;
            }
        }
    }

    .end {
        margin-top: 1rem;
    }

    .content {
        margin-top: 1rem;
    }

}
</style>