/*
 * @FilePath: pyRequest.js
 * @Author: yun.huang <1594909346@qq.com>
 * @Date: 2023-08-31 13:42:27
 * @LastEditors: yun.huang <1594909346@qq.com>
 * @LastEditTime: 2023-08-31 16:10:22
 * @Version: 1.0.1
 * Copyright: 2023 YunYou Innovation Technology Co., Ltd. All Rights Reserved.
 * @Descripttion: 愿你开心每一天~
 */
import env from '../utils/env';
import {getToken, removeToken, removeUser} from "@/utils/utils";

function service(options = {}) {
    options.url = `${env.pythonUrl}${options.url}`;
    options.timeout = 100000;
    if (getToken()) {
        options.header = {
            'content-type': 'application/json',
            'Authorization': `${getToken()}`
        };
    }
    return new Promise((resolve, reject) => {
        // 发送 HTTP 请求
        uni.request({
            ...options,
            success: function (res) {
                if (res.statusCode === 200) {
                    if (res.data.code === 2000) {
                        resolve(res.data.data);
                    } else {
                        //未登录 ? 登陆失效
                        if (res.data.code === 401) {
                            removeToken()
                            removeUser()
                            uni.reLaunch({
                                url: '/pages/master/master?swiperIndex=1'
                            })
                        } else {
                            reject(res.data.msg);
                        }
                    }
                } else {
                    reject('与服务器建立连接失败');
                }
            },
            fail: function () {
                reject('与服务器建立连接失败');
            }
        });
    });
}

export default service;
