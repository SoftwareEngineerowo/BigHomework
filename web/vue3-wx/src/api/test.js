import request from '@/utils/request2.js';

// 显示所有试题
export const getAllQuesAPI = ()=>{
    return request.get('/showQues/all/')
}
// 添加试题
export const addQuesAPI = (data)=>{
    return request.post('/ques/add/',data)
}
// 添加题型
export const addQuesTypeAPI = (data)=>{
    return request.post('/quesKind/add/',data)
}
// 根据题型查询试题
export const getQuesByTypeAPI = (quesKindId)=>{
    return request.get(`/showQues/byQuesKindId/?quesKindId=${quesKindId}`)
}
// 根据试题id查询试题
export const getQuesByIdAPI = (quesId)=>{
    return request.get(`/showQues/byQuesId/?quesId=${quesId}`)
}
// 删除试题
export const deleteQuesByIdAPI = (quesId)=>{
    return request.delete(`/delete/Ques/byQuesId/?quesId=${quesId}`)
}



// 显示所有试卷
export const getAllPaperAPI = ()=>{
    return request.get('/showPaper/all')
}
// 添加试卷
export const addPaperAPI = (data)=>{
    return request.post('/paper/add/',data)
}
// 试卷名称模糊查询
export const getPaperByNameAPI = (paperName)=>{
    return request.get('/showPaper/fuzzyByPaperName/',paperName)
}
// 根据试卷id查询试卷
export const getPaperByIdAPI = (paperId)=>{
    return request.get(`/showPaper/byPaperId/?paperId=${paperId}`)
}
// 删除试卷
export const deletePaperByIdAPI = (paperId)=>{
    return request.delete(`/delete/Paper/byPaperId/?paperId=${paperId}`)
}



// 显示所有考试
export const getAllTestAPI = ()=>{
    return request.get('/showExam/all/')
}
// 添加考试（壳子）
export const addExamBeforeAPI = ()=>{
    return request.get('/exam/beforeAdd/')
}
// 添加考试(内容)
export const addExamAPI = (data)=>{
    return request.post('/exam/add/',data)
}
// 添加考试（取消）
export const addExamAfterAPI = (examId)=>{
    return request.delete(`/exam/cancel/?examId=${examId}`)
}
// 根据考试id查询考试
export const getExamById = (examId)=>{
    return request.get(`/showExam/byExamId/?examId=${examId}`)
}
// 删除考试
export const deleteExamByIdAPI = (examId)=>{
    return request.delete(`/delete/Exam/byExamId/?examId=${examId}`)
}
// 更改考试的上传状态
export const changePaperStatusAPI = (examId,status)=>{
    return request.get(`/exam/changeHasAnswer/?examId=${examId}&status=${status}`)
}




// 添加答卷
export const addAwPaperAPI = (data)=>{
    return request.post('/answer/add/',data)
}
// 添加考生准考证
export const addCertifyAPI = (data)=>{
    return request.post('/certify/add/',data)
}
// 根据答题id查询答卷
export const getAnswerQuesByIdAPI = (answerId)=>{
    return request.get('/showAnswer/byAnswerId/',answerId)
}


// 分析
export const getFenxiByID = (paperId,examId)=>{
    return request.get(`/analyse/normal/?paperId=${paperId}&examId=${examId}`)
}



