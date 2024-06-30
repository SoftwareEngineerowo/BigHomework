<template>
    <div ref="listContainer" class="virtual-list-container" @scroll="handleScroll">
        <div v-if="startOffset" class="virtual-list-offset1" :style="{ height: startOffset + 'px' }"></div>
        <div class="li" @click="onClickQues(ques)" v-for="ques in visibleItems" :key="ques.quesId"
            :style="{ height: itemHeight + 'px' }">
            <a href="javascript:;">
                <el-button color="#045afe" plain type="success">{{ quesTypeList[ques.quesKindId - 1].quesKindName
                }}</el-button>
                <div class="content">
                    <div class="contentInner">
                        {{ ques.quesContent }}
                    </div>
                    <el-button @click.stop="onDeleteQues(ques)" class="delete" plain type="danger">删除</el-button>
                </div>
            </a>
        </div>
        <div v-if="endOffset" class="virtual-list-offset2" :style="{ height: endOffset + 'px' }"></div>
    </div>
    <!-- 显示试题详细信息弹窗 -->
    <el-dialog v-model="quesShowDialog" width="400">
        <el-descriptions class="margin-top" title="试题详情" :column="2" :size="size" border>
            <el-descriptions-item>
                <template #label>
                    <div class="cell-item">
                        <el-icon>
                            <EditPen />
                        </el-icon>
                        <div>试题内容</div>
                    </div>
                </template>
                {{ quesInfo.quesContent }}
            </el-descriptions-item>

            <el-descriptions-item>
                <template #label>
                    <div class="cell-item">
                        <el-icon>
                            <EditPen />
                        </el-icon>
                        <div>试题答案</div>
                    </div>
                </template>
                {{ quesInfo.quesAnswer }}
            </el-descriptions-item>

        </el-descriptions>

        <template #footer>
            <span class="dialog-footer">
                <el-button @click="quesShowDialog = false" type="primary">确认</el-button>
            </span>
        </template>
    </el-dialog>
</template>  
    
<script setup>
import { ref, onMounted, computed } from 'vue'
import {
  deleteQuesByIdAPI
} from '@/api/test.js'


// 删除试题
const emit = defineEmits(['success'])
const onDeleteQues = async (ques) => {
    await ElMessageBox.confirm('您确定删除该试题吗', 'Warning', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
    })
    const res = await deleteQuesByIdAPI(ques.quesId)
    ElMessage.success("删除成功")
    // 通知父组件
    emit('success')
}
const quesInfo = ref({})
const quesShowDialog = ref(false)
const onClickQues = (ques) => {
    quesShowDialog.value = true
    quesInfo.value = ques
}



// 实现虚拟列表
const props = defineProps({
    items: {
        type: Array,
        required: true,
    },
    itemHeight: {
        type: Number,
        required: true,
    },
})
const quesTypeList = ref([{ quesKindId: 1, quesKindName: '单选题' }, { quesKindId: 2, quesKindName: '多选题' }, { quesKindId: 3, quesKindName: '简答题' }, { quesKindId: 4, quesKindName: '判断题' }])
const listContainer = ref(null)
const startIndex = ref(0)
const endIndex = ref(0)

// 获取当前可视范围内的列表项数组
const visibleItems = computed(() => {
    const start = startIndex.value
    const end = endIndex.value
    return props.items.slice(start, end + 1)
})
// 获取上滚动空白区域的高度
const startOffset = computed(() => {
    return startIndex.value * props.itemHeight
})
// 获取下滚动空白区域的高度
const endOffset = computed(() => {
    // 已经渲染的列表数
    const visibleCount = endIndex.value + 1
    // 总列表数
    const totalCount = props.items.length
    const ret = Math.max(0, (totalCount - visibleCount) * props.itemHeight)
    return ret
})

onMounted(() => {
    updateVisibleItems()
})

const handleScroll = () => {
    updateVisibleItems()
}

// 更新可见列表项
const updateVisibleItems = () => {
    if (!listContainer.value) return
    // 获取已经滚动了的高度
    const scrollTop = listContainer.value.scrollTop
    // 获取容器可视区域高度
    const clientHeight = listContainer.value.clientHeight
    startIndex.value = Math.floor(scrollTop / props.itemHeight)
    endIndex.value = Math.min(
        startIndex.value + Math.ceil(clientHeight / props.itemHeight) - 1,
        // 确保索引不越界
        props.items.length - 1
    )
}
</script>  
    
<style scoped lang="scss">  .virtual-list-container {
      height: 100%;
      overflow-y: scroll;
      width: 100%;
      position: relative;

      .li {
          line-height: 8vh;
          // 开启相对定位
          position: relative;

          &:hover {
              background-color: rgb(236, 244, 247);
          }

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

              // 文字部分
              .contentInner {
                  width: 30rem;
                  height: 100%;
                  overflow: hidden;
                  text-overflow: ellipsis;
                  white-space: nowrap;
              }

              // 删除按钮
              .delete {
                  position: absolute;
                  left: 90%;
                  width: 3.5rem;
                  height: 2rem;
              }
          }
      }
  }

  .virtual-list-offset1,
  .virtual-list-offset2 {

      width: 100%;
  }
</style>