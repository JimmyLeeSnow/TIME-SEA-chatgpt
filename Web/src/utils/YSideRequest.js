/*
 * @FilePath: YSideRequest.js
 * @Author: yun.huang <1594909346@qq.com>
 * @Date: 2023-08-30 10:04:42
 * @LastEditors: yun.huang <1594909346@qq.com>
 * @LastEditTime: 2023-08-30 10:04:42
 * @Version: 1.0.1
 * Copyright: 2023 YunYou Innovation Technology Co., Ltd. All Rights Reserved.
 * @Descripttion: 愿你开心每一天~
 */
/*
 * @FilePath: YSideRequest.js
 * @Author: yun.huang <1594909346@qq.com>
 * @Date: 2023-05-30 10:50:54
 * @LastEditors: yun.huang <1594909346@qq.com>
 * @LastEditTime: 2023-06-08 16:49:47
 * @Version: 1.0.1
 * Copyright: 2023 YunYou Innovation Technology Co., Ltd. All Rights Reserved.
 * @Descripttion: 愿你开心每一天~
 */
import axios from 'axios'

// TODO 请求取消令牌列表
export let cancelArr = [];

// TODO 创建第二个axios实例
const python = axios.create({
    baseURL: process.env.VUE_APP_BASE_API_PYTHON,
    timeout: 6 * 60 * 1000
});

// TODO 请求拦截器
python.interceptors.request.use(config => {
    // TODO 请求头
    config.headers.Authorization = `Bearer ${localStorage.getItem('token')}`
    // TODO 添加取消令牌
    config.cancelToken = new axios.CancelToken(cancel => {
        cancelArr.push(cancel)
    })

    return config
}, error => {
    return Promise.reject(error)
});

// TODO 响应拦截器
python.interceptors.response.use(response => {
    const res = response.data;
    if (res.code !== 2000) {
        if (res.code ===401){
            localStorage.removeItem('token');
            localStorage.removeItem('user')
        }else{
            throw res.msg
        }
    } else {
        return res.data
    }
}, () => {
    throw 'AI服务调用失败，正在紧急处理，请稍后使用。'
})

export default python
