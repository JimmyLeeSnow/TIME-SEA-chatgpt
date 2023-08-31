// 引用网络请求中间件
import request from './../utils/pyRequest';

/**
 *    违禁状态检测
 */
export function ProhibitedUserDisable(data) {
    let paramString = '';

    Object.keys(data).forEach((key, index) => {
        paramString += (index === 0 ? '' : '&') + encodeURIComponent(key) + '=' + encodeURIComponent(data[key]);
    });

    return request({
        url: '/python/system/userdisable/?' + paramString,
        method: 'GET'
    });
}

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
