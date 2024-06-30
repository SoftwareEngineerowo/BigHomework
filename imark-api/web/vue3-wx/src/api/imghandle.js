import request from '@/utils/request.js';

// 上传图片
export const uploadImgAPI = (fileName,data) =>{
    return request({
        url: `/files/upload/${fileName}`,
        method: 'PUT',
        data: data,
        config:{
            headers:{
               'Content-Type': 'image/png'
            }
        }
    })
}

// 发送坐标获取分割后的图片
export const carveImgAPI = (formData)=>{
    return request({
            url: '/api/seg/save/',
            method: 'POST',
            data: formData,
        })
}

// 上传坐标（多个）
export const uploadPointsAPI = (data)=>{
    return request({
        url: '/api/seg/structure/',
        method: 'PUT',
        data: data,
    })
}

// 更新切片题号
export const updatePaperId = (data)=>{
    return request({
        url: '/api/seg/update/',
        method: 'PATCH',
        data: data,
    })
}

// 统一分割答卷
export const carveAllAwPaperAPI = (data)=>{
    return request({
            url: '/api/seg/do/',
            method: 'POST',
            data: data,
        })
}
