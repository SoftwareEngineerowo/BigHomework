import request from '@/utils/request2.js';


// 添加阅卷任务
export const addMarkAPI = (data)=>{
    return request.post('/mark/add/',data)
}
// 根据考试id查询考试学生
export const getAllStuByExamIdAPI = (examId)=>{
    return request.get(`/showCertify/byExamId/?examId=${examId}`)
}
// 根据准考证id和试题id查询答题模型
export const getAwQuesByCertIdandQuesIdAPI = (certId,quesId)=>{
    return request.get(`/showAnswer/byCertIdandQuesId/?certId=${certId}&quesId=${quesId}`)
}

// 添加打分结果
export const addMarkResult = (data)=>{
    return request.post('/mark/result/',data)
}
// 根据打分id删除单题打分结果
export const deleteMarkResultByIDAPI = (id)=>{
    return request.delete(`/mark/deleteMarkResultById/?id=${id}`)
}
// 根据answerId查询单题打分结果
export const getMarkResultByAnswerId = (answerId)=>{
    return request.get('/markResult/selectMarkResultByAnswerId/?answerId='+answerId)
}
// 添加单卷分数
export const addSheetScoreAPI = (data)=>{
    return request.post('/score/addSheetScore/',data)
}
// 根据examId查询所有学生成绩
export const getSheetScoreByExamIdAPI = (examId)=>{
    return request.get("/score/selectAllByExamId/?examId="+examId)
}

// 教师查询阅卷题目
export const getMark = (query)=>{
    return request.get('/mark/getMark',query)
}

