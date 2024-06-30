import request from '@/utils/request.js';

// 发送图片识别文字
export const  getTextAPI = (formData)=>{
    return request({
            url: '/api/ocr/simple/',
            method: 'PUT',
            data: formData,
        }) 
}

// 发送图片获取答案
export const getAnswerAPI = (img)=>{
    return request({
        url: '/api/ocr/ques/',
        method: 'PUT',
        data:{
            img
        }
    })
}

