<script setup >
import { onMounted, ref } from 'vue';
import { Delete, Plus, ZoomIn } from '@element-plus/icons-vue'
import { uploadImgAPI, uploadPointsAPI, carveImgAPI, updatePaperId } from '@/api/imghandle.js'
import { getTextAPI, getAnswerAPI } from '@/api/texthandle.js'
import { addQuesAPI, addPaperAPI } from '@/api/test.js'
import { ElMessage } from 'element-plus';
import { useRouter } from 'vue-router'
import { ElLoading } from 'element-plus'

// 获取浏览器窗口的宽度和高度
const WIDTH = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth
const HEIGHT = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight
console.log(WIDTH)
console.log(HEIGHT)

const router = useRouter()
// Canvas
const createCanvas = (len) => {
    // 创建画布
    const canvas = document.querySelector('canvas')
    const init = (len) => {
        // 设置画布宽高
        const w = WIDTH * 0.9
        const h = 2000 * (len + 1)
        canvas.width = w * devicePixelRatio
        canvas.height = h * devicePixelRatio
        canvas.style.width = w + 'px';
        canvas.style.height = h + 'px';
        console.log("把画布浅浅初始化一下,长度是" + len);
        // 设置画布背景色
        canvas.fillStyle = 'rgba(0,0,0,0)'
    }
    init(len)
    // 获取画笔
    const ctx = canvas.getContext('2d')
    // 创建一个数组来保存所有图形
    const shapes = []

    // 创造矩形类
    class Rectangle {
        constructor(startX, startY) {
            this.color = 'rgba(0,0,0,0)'
            this.startX = startX
            this.startY = startY
            this.endX = startX
            this.endY = startY
        }
        get minX() {
            return Math.min(this.startX, this.endX)
        }
        get maxX() {
            return Math.max(this.startX, this.endX)
        }
        get minY() {
            return Math.min(this.startY, this.endY)
        }
        get maxY() {
            return Math.max(this.startY, this.endY)
        }
        draw() {
            ctx.beginPath();
            ctx.moveTo(this.minX * devicePixelRatio, this.minY * devicePixelRatio);
            ctx.lineTo(this.maxX * devicePixelRatio, this.minY * devicePixelRatio);
            ctx.lineTo(this.maxX * devicePixelRatio, this.maxY * devicePixelRatio)
            ctx.lineTo(this.minX * devicePixelRatio, this.maxY * devicePixelRatio)
            ctx.lineTo(this.minX * devicePixelRatio, this.minY * devicePixelRatio)
            ctx.fillStyle = this.color
            ctx.fill()
            ctx.strokeStyle = '#f00'
            ctx.lineCap = 'square'
            ctx.lineWidth = 2 * devicePixelRatio
            // 描边
            ctx.stroke()
        }
        // 判断（x,y）坐标是否在这个矩形中
        isInside(x, y) {
            return x >= this.minX && x <= this.maxX && y <= this.maxY && y >= this.minY
        }
    }

    // 鼠标事件
    canvas.onmousedown = (e) => {
        requestAnimationFrame(draw)
        // 获取画布
        const rect = canvas.getBoundingClientRect()
        // 获取鼠标点相对于canvas的位置
        const clickX = e.clientX - rect.left
        const clickY = e.clientY - rect.top
        const shape = getShape(clickX, clickY)
        // 判断鼠标点是否在已存在图形中
        if (shape) {
            // 如果在则执行拖动逻辑
            // 获取图形原来位置
            const { startX, startY, endX, endY } = shape
            // 监听鼠标移动事件
            window.onmousemove = e => {
                requestAnimationFrame(draw)
                // 鼠标移动距离:新的鼠标位置(相对于画布)-鼠标点击位置
                const disX = e.clientX - rect.left - clickX
                const disY = e.clientY - rect.top - clickY
                // 更新图形坐标
                shape.startX = startX + disX
                shape.startY = startY + disY
                shape.endX = endX + disX
                shape.endY = endY + disY
            }
            // 监听鼠标抬起事件
            window.onmouseup = (e) => {
                window.onmousemove = null
                window.onmouseup = null
                requestAnimationFrame(draw)

                // 获取原来坐标点位置
                const index = shapes.indexOf(shape)
                let point = points.value[index]
                // 更新坐标
                point = { x1: shape.startX, y1: shape.startY, x2: shape.endX, y2: shape.endY, num: points.value.length + 1, img: '', quesId: 'known', paper: 'known', typ: "INFO" }
                points.value[index] = point
            }
        } else {
            // 创建矩形
            const shape = new Rectangle(clickX, clickY)
            shapes.push(shape)
            // 监听鼠标移动事件
            window.onmousemove = (e) => {
                requestAnimationFrame(draw)
                shape.endX = e.clientX - rect.left
                shape.endY = e.clientY - rect.top
            }
            // 监听鼠标抬起事件
            window.onmouseup = (e) => {
                window.onmousemove = null
                window.onmouseup = null
                requestAnimationFrame(draw)
                // 存入这个新图形的坐标
                points.value.push({ x1: clickX, y1: clickY, x2: shape.endX, y2: shape.endY, num: points.value.length + 1, img: '', quesId: 'known', paper: 'known', typ: "INFO" })

            }
        }

    }

    // 重绘
    const draw = () => {
        // 清空画布
        ctx.clearRect(0, 0, canvas.width, canvas.height)
        for (const shape of shapes) {
            shape.draw()
        }
    }
    draw()

    // 获取（x,y）坐标下的图形，如果没有则返回null
    const getShape = (x, y) => {
        for (let i = shapes.length - 1; i >= 0; i--) {
            const shape = shapes[i]
            // 如果这个图形被我们点中了，则返回这个图形
            if (shape.isInside(x, y)) {
                return shape
            }
        }
        return null
    }

}

// 上传图片文件列表
const fileList = ref([])
const flag = ref(1)
const dialogImageUrl = ref('')
const dialogVisible = ref(true)
const len = ref(0)
const canvas = ref()
// 创建一个数组来保存所有图形的四个坐标点
const points = ref([])
const imgUrlList = ref([])

// 删除图片
const handleRemove = (file) => {
    const imgUrl = URL.createObjectURL(file.raw)
    urlList.value.remove(imgUrl)
}

// 展示大图
const handlePictureCardPreview = (file) => {
    dialogImageUrl.value = file.url
    dialogVisible.value = true
}

// 用于图片回显的数组
const urlList = ref([])

// 选择图片完毕->上传图片
const URL = ref('http://8.137.85.0:8008/files/download/img10aa5b14-fb2b-11ee-9b91-00163e04f5e4.jpg')
const onSelectEnd = async () => {
    if (value1.value == true) {
        flag.value = 2
        len.value = 1
        createCanvas(len.value)

        urlList.value.push(URL.value)
        imgUrlList.value.push(URL.value)
    } else {
        console.log(fileList.value)
        flag.value = 2
        len.value = fileList.value.length
        createCanvas(len.value)
        const loadingInstance1 = ElLoading.service({ fullscreen: true })
        for (let item of fileList.value) {
            const filename = item.raw.name
            // 上传
            const res = await uploadImgAPI(filename, item.raw)
            console.log(res.data)
            imgUrlList.value.push(res.data)
        }
        loadingInstance1.close()
    }
}

// 创建一个装文字识别信息的数组
const textList = ref([])
// 创建一个装上传坐标接口的请求参数
const newPoint = ref([])
// 提交进行切割图片
const onConfirm = async () => {
    // 处理points数组并且添加图片url
    points.value.sort((a, b) => { return a.y1 - b.y1 }).reserve

    // 获取imgDom元素
    const imgDom = document.querySelectorAll("img")
    let sum = []
    for (let i = 0; i < imgDom.length; i++) {
        console.log(imgDom[i])
        console.log(imgDom[i].naturalWidth)
        if (i === 0) sum[i] = imgDom[i].clientHeight
        else sum[i] = sum[i - 1] + imgDom[i].clientHeight
    }

    let index = 0, cnt = 0
    for (let i = 0; i < points.value.length; i++) {
        if (points.value[i].y1 > sum[index]) {
            index++
            cnt = 0
        }
        // 赋予img和num
        points.value[i].img = imgUrlList.value[index]
        points.value[i].num = cnt
        cnt++
        // 将坐标处理为相对坐标
        const naturalWidth = imgDom[index].naturalWidth
        const clientWidth = imgDom[index].clientWidth
        const naturalHeight = imgDom[index].naturalHeight
        const clientHeight = imgDom[index].clientHeight
        points.value[i].x1 = Math.floor(points.value[i].x1 * naturalWidth / clientWidth)
        points.value[i].x2 = Math.ceil(points.value[i].x2 * naturalWidth / clientWidth)
        points.value[i].y1 = Math.floor((points.value[i].y1 - (index - 1 < 0 ? 0 : sum[index - 1])) * naturalHeight / clientHeight)
        points.value[i].y2 = Math.ceil((points.value[i].y2 - (index - 1 < 0 ? 0 : sum[index - 1])) * naturalHeight / clientHeight)
    }

    // 处理上传多个坐标的请求参数
    points.value.forEach((point) => {
        let obj = {}
        obj.img = "STRUCTURE"
        obj.x1 = point.x1
        obj.y1 = point.y1
        obj.x2 = point.x2
        obj.y2 = point.y2
        obj.num = point.num
        obj.quesId = point.quesId
        obj.paper = point.paper
        obj.typ = point.typ
        newPoint.value.push(obj)
    })

    const loadingInstance1 = ElLoading.service({ fullscreen: true })
    // 将图片进行切割
    for (let point of points.value) {
        const formData = new FormData()
        formData.append('img', point.img)
        formData.append('num', point.num)
        formData.append('x1', point.x1)
        formData.append('x2', point.x2)
        formData.append('y1', point.y1)
        formData.append('y2', point.y2)
        const res = await carveImgAPI(formData)
        console.log(res.data)
        textList.value.push({ img: res.data, res: '', flag: false })
    }
    ElMessage.success("切割图片成功")
    loadingInstance1.close()
    // 移除画布
    const canvas = document.querySelector('canvas')
    canvas.remove()
    flag.value = 3
}
// 请求文字识别
const getText = async (text) => {
    // 获取文字识别
    const data = new FormData()
    data.append('img', text.img)
    const loadingInstance1 = ElLoading.service({ fullscreen: true })
    const res1 = await getTextAPI(data)
    ElMessage.success("获取文字识别成功")
    loadingInstance1.close()
    const index = textList.value.indexOf(text)
    textList.value[index].res = res1.data.res
}
// 添加题目
const quesTypeList = ref([{ quesKindId: 1, quesKindName: '单选题' }, { quesKindId: 2, quesKindName: '多选题' }, { quesKindId: 3, quesKindName: '简答题' }, { quesKindId: 4, quesKindName: '判断题' }])
const quesSelectValue = ref('')
const num = ref('')
// 用于记录所有试题题型与id，便于添加试卷
const quesKindIdList = ref([])
const quesIdList = ref([])
const onAddQues = async (text) => {
    // 判断是否选择题型
    if (quesSelectValue.value == '') {
        ElMessage.warning('还未选择题型')
        return
    }
    if (num.value == '') {
        ElMessage.warning('还未输入题目分数')
        return
    }
    // 修改添加状态
    text.flag = true
    const loadingInstance1 = ElLoading.service({ fullscreen: true })
    // 请求答案
    const res2 = await getAnswerAPI(text.img)
    // 封装请求参数
    const data = {
        quesKindId: quesSelectValue.value,
        quesContent: text.res,
        quesAnswer: res2.data.ans,
        quesDefaultScore: num.value,
        quesLevel: 200.01,
    }
    console.log(data)
    const res = await addQuesAPI(data)
    ElMessage.success("添加试题成功")
    loadingInstance1.close()
    quesIdList.value.push(res.data.data.quesId)

    if (quesKindIdList.value.indexOf(quesSelectValue.value) == -1&& quesSelectValue.value!=undefined) 
        quesKindIdList.value.push(quesSelectValue.value)
    console.log(quesKindIdList.value)
}
// 添加试卷
const paperDialog = ref(false)
// formModel
const formModel = ref({
    paperName: '',
    paperFullScore: '',
    paperLevel: '80.01',
    quesKindIds: '',
    quesIds: ''
})

const onAddPaper = () => {
    paperDialog.value = true
}
const onPaperComfirm = async () => {
    //上传多个坐标
    await uploadPointsAPI({ structure: newPoint.value })

    // 添加试卷
    console.log(quesKindIdList.value)
    formModel.value.quesKindIds = '[' + quesKindIdList.value.join(',') + ']'
    formModel.value.quesIds = '[' + quesIdList.value.join(',') + ']'
    console.log(formModel.value.quesKindIds)
    const res = await addPaperAPI(formModel.value)
    ElMessage.success("添加试卷成功")
    paperDialog.value = false

    // 更新切片题号
    const data = {
        old: 'known',
        update: {
            paper: res.data.data.paperId,
            ques: res.data.data.quesIds
        }
    }
    await updatePaperId(data)
    router.go(-1)
}
// 演示
const value1 = ref(false)
</script>
<template>
    <div class="select" v-if="flag == 1">
        <div class="switch"> <el-switch v-model="value1" />是否开启演示模式</div>
        <!-- 请选择试卷图片 -->
        <div class="title">请选择试卷图片 <el-button color="#045afe" @click="onSelectEnd">选择完毕</el-button></div>
        <!-- 上传框 -->
        <div class="upload">
            <el-upload v-if="!value1" :on-change="handleChange" v-model:file-list="fileList" action='#'
                list-type="picture-card" :auto-upload="false">
                <el-icon>
                    <Plus />
                </el-icon>

                <template #file="{ file }">
                    <div>
                        <img class="el-upload-list__item-thumbnail" :src="file.url" />
                        <span class="el-upload-list__item-actions">
                            <span class="el-upload-list__item-preview" @click="handlePictureCardPreview(file)">
                                <el-icon><zoom-in /></el-icon>
                            </span>
                            <span v-if="!disabled" class="el-upload-list__item-delete" @click="handleRemove(file)">
                                <el-icon>
                                    <Delete />
                                </el-icon>
                            </span>
                        </span>
                    </div>
                </template>
            </el-upload>

            <div class="box" v-if="value1">
                <img :src=URL>
            </div>

        </div>
    </div>

    <div class="selected">
        <div class="img" v-if="flag == 2">
            <img v-for="url of imgUrlList" :src="url" :key="url">
        </div>
        <div class="tool" v-if="flag == 2 || flag == 3">
            <el-button v-if="flag == 2" @click="onConfirm" color="#045afe">请求图片切割</el-button>
            <el-button v-if="flag == 3" @click="onAddPaper" color="#045afe">添加试卷</el-button>
        </div>
        <canvas></canvas>
    </div>

    <div class="ret2" v-if="flag == 3">
        <el-popover placement="left" :width="300" trigger="click" v-for="text of textList" :key="text.img">
            <div class="content">
                {{ text.res }}
            </div>
            <div style="text-align: right; margin: 0">

                <div class="before" v-if="text.res == ''">
                    <el-button @click="getText(text)" size="large" type="primary">请求文字识别</el-button>
                </div>
                <br>
                <div class="after" v-if="text.res != ''">
                    <el-form label-width="auto">
                        <el-form-item label="题型:">
                            <el-select size="large" v-model="quesSelectValue" placeholder="Select">
                                <el-option v-for="quesType of quesTypeList" :key="quesType.quesKindId"
                                    :label="quesType.quesKindName" :value="quesType.quesKindId" />
                            </el-select>
                        </el-form-item>
                        <el-form-item label="题目分数:">
                            <el-input-number v-model="num" />
                        </el-form-item>
                    </el-form>

                    <el-button @click="onAddQues(text)" size="large" type="primary" :disabled="text.flag">{{ text.flag ==
                        true ? '已添加' : '添加题目' }}</el-button>
                </div>

            </div>
            <template #reference>
                <img class="carveimg" :src="text.img">
            </template>
        </el-popover>
    </div>
    <!-- 试卷弹窗-->
    <el-dialog class="paperdialog" v-model="paperDialog" width="400">
        <el-form :model="formModel" :rules="rulse">
            <el-form-item prop="paperName" label="试卷名称：">
                <el-input v-model="formModel.paperName" placeholder="请输入试卷名称"></el-input>
            </el-form-item>
            <el-form-item prop="paperFullScore" label="全卷总分：">
                <el-input v-model="formModel.paperFullScore" placeholder="请输入全卷总分"></el-input>
            </el-form-item>
        </el-form>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="paperDialog = false">取消</el-button>
                <el-button type="primary" @click="onPaperComfirm">
                    确定
                </el-button>
            </div>
        </template>
    </el-dialog>
</template>
  

<style scoped lang="scss">
.el-popover {
    height: 300px;
    background-color: pink;
    font-size: 15px;
}

// 最开始选择图片
.select {
    margin: 0 auto;
    text-align: center;
    padding-top: 20vh;

    // 标题
    .title {
        font-size: 1.5rem;
        margin-bottom: 2rem;
    }

    .box {
        img {
            width: 15rem
        }
    }
}

// 选择图片完毕
div.selected {
    background-color: dodgerblue;
    width: 100vw;

    // 画布
    canvas {
        position: absolute;
        z-index: 9;
        margin-left: 3rem;
    }

    .img {
        width: 80vw;
        position: absolute;
        margin: 0 3rem;

        img {
            display: block;
            width: 100%;
        }
    }

}



.ret2 {
    width: 100%;

    // 分割后的图片
    .carveimg {
        margin-top: 3rem;
        width: 50%;
        display: block;
    }

    .el-select {
        .el-option {
            width: 20%;
        }
    }
}

// 工具栏
.tool {
    height: 5rem;
    border-radius: 10px;
    position: fixed;
    right: 0rem;
    top: 3rem;
    right: 4rem;
    z-index: 99;
    line-height: 5rem;

    .el-button {
        padding-left: 10px;
        padding-right: 10px;
        height: 3rem;
    }
}

// 试卷弹窗
.paperdialog {
    width: 5rem;

    .el-form {
        .el-form-item {
            width: 100%;
        }
    }
}
</style>
