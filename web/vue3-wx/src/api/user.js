import request from '@/utils/request2.js';

// 注册
export const registerAPI = (data)=>{
    return request({
        url: '/registered/',
        method: 'post',
        data: data
    })
}

// 登录
export const loginAPI = (data)=>{
    return request({
        url: '/login/',
        method: 'post',
        data: data
    })
}

// 修改个人资料
export const updateUserInfoAPI = (data)=>{
    return request({
        url: '/userInfo/update/',
        method: 'POST',
        data: data
    })
}