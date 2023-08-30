/*
 * @FilePath: YSideApi.js
 * @Author: yun.huang <1594909346@qq.com>
 * @Date: 2023-08-30 10:03:45
 * @LastEditors: yun.huang <1594909346@qq.com>
 * @LastEditTime: 2023-08-30 10:03:46
 * @Version: 1.0.1
 * Copyright: 2023 YunYou Innovation Technology Co., Ltd. All Rights Reserved.
 * @Descripttion: 愿你开心每一天~
 */
/*
 * @FilePath: YSideApi.js
 * @Author: yun.huang <1594909346@qq.com>
 * @Date: 2023-05-30 10:52:47
 * @LastEditors: yun.huang <1594909346@qq.com>
 * @LastEditTime: 2023-06-07 21:55:33
 * @Version: 1.0.1
 * Copyright: 2023 YunYou Innovation Technology Co., Ltd. All Rights Reserved.
 * @Descripttion: 愿你开心每一天~
 */
import request from '@/utils/YSideRequest'

/**
 *    违禁词检测
 */
export function ProhibitedTextDetection(data) {
    return request({
        url: '/python/system/textdetection/',
        method: 'POST',
        data
    })
}

/**
 *    违禁状态检测
 */
 export function UserDisable(data) {
    const params = new URLSearchParams();

    Object.keys(data).forEach(key => {
        params.append(key, data[key]);
    });

    return request({
        url: '/python/system/userdisable/?' + params.toString(),
        method: 'GET'
    });
}
