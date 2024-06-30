import request from '@/utils/request.js';

// AI助手对话
export const talkAiAPI = (formData)=>{
    return request.put('/api/ai/assistant/',formData)
}

// 获取聊天记录
export const getHistoryAPI = (formData)=>{
    return request.get('/api/ai/history/',formData);
}

// 获取AI评价
export const getAICommentAPI = (formData)=>{
    return request.post('/api/ai/comment/',formData)
}

// 获取AI打分
export const getAIMarkAPI = (formData)=>{
    return request.post('/api/ai/mark/',formData)
}