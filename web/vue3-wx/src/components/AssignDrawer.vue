<script setup>
import { ref } from 'vue'
import { Edit } from '@element-plus/icons-vue'
const drawer = ref(false)
//向外界呈现open方法
const open = async (row) => {
    drawer.value = true
    console.log(row)
}
defineExpose({ open })
// 确定
const onConfirm = () => {
    drawer.value = false
}
const quesSelectValue = ref('何宗欣')
const radio1 = ref('1')
</script>
<template>
    <div>
        <el-drawer v-model="drawer" size="24rem" title="I am the title" :with-header="false">
            <div class="title">第一题</div>
            <el-divider />
            <div class="evatype">
                <div class="left">评分方式:</div>
                <div class="right">
                    <el-radio-group v-model="radio1">
                        <el-radio label="1" value="1">
                            单评
                        </el-radio>
                        <div></div>
                        <div>每个题只需要一个老师修改,这个老师批改分数即为最终分</div>


                        <el-radio label="2" value="2">双评</el-radio>
                        <div>每个题由两个老师一起批改。双评分差大于仲裁分差时，由仲裁人给出最终得分</div>
                    </el-radio-group>

                </div>
            </div>
            <el-divider />
            <div class="people">
                <div class="left">批改人:</div>
                <div class="right">
                    <el-select size="large" v-model="quesSelectValue" placeholder="Select">
                        <el-option label="何宗欣" />
                    </el-select>
                </div>
            </div>
            <el-divider />
            <div class="assigntype">
                <div class="left">分配方式:</div>
                <div class="right">
                    <el-radio-group v-model="radio1">
                        <el-radio label="1" value="1">
                            定量分配
                        </el-radio>
                        <div>由操作者来自定义各批改人任务量</div>

                        <el-radio label="2" value="2">平均分配</el-radio>
                        <div>按照已上传题目的数量平均分配给批改人</div>
                    </el-radio-group>
                </div>
            </div>
            <el-divider />
            <el-button @click="drawer = false" class="btn">取消</el-button>
            <el-button @click="onConfirm" type="primary">确定</el-button>
        </el-drawer>
    </div>
</template>
<style lang="scss" scoped>
.btn {
    margin-left: 14rem;
}

.people {
    display: flex;

    .left {
        width: 30%;
        font-size: 0.8rem;

    }

    .right {
        width: 70%;
        font-size: 0.8rem;
    }
}




.evatype,
.assigntype {
    display: flex;

    .left {
        width: 30%;
        font-size: 0.8rem;
        padding-top: 2rem;
    }

    .right {
        width: 70%;
        display: flex;
        flex-direction: column;

        .el-radio {
            margin-top: 0.7rem;
        }

        // 说明部分
        div {
            font-size: 0.7rem;
        }
    }
}
</style>