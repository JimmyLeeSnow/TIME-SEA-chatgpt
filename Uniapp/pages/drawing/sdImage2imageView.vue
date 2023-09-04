<template>
  <view class="container">
    <loading-component ref="loadingRef" :msg="msg" :degree="0.8" />
    <generate-loading-component ref="generateLoadingRef" :location="location" />
    <scroll-view class="main-scroll" scroll-y>
      <!--  上传文件框框-->
      <view class="title">
        <view>
          上传原图(必填)
        </view>
        <view class="uploader_container">
          <view v-if="!form.images">
            <van-uploader @after-read="imageCacheCallback" use-before-read :deletable="false" @before-read="beforeRead">
              <van-icon name="plus" size="60rpx" color="#868585" />
            </van-uploader>
            <view class="uploader_subassembly">
              <view class="uploader_prompt">
                点击上传(参考图)
              </view>
              <view>
                图片格式支持 JPG、JPEG、PNG 不超过2MB
              </view>
              <view>
                请勿上传违反微信社区相关条例内容
              </view>
            </view>
          </view>
          <view v-else>
            <image :src="form.images" class="preview_image" @click="previewImage(form.images)" />
            <view class="preview_model">
              <van-uploader @after-read="imageCacheCallback" :deletable="false">
                <button class="preview_choose">重新选择
                </button>
              </van-uploader>
              <button class="preview_deleted" @click="deleted">删除</button>
            </view>
          </view>
        </view>
      </view>
      <!--  描述词-->
      <view class="title">
        <view class="title-row">
          <view class="lable-prompt">正向提示词</view>
          <button class="random-prompt" @click="randomForward">随机</button>
          <button class="clear-prompt" @click="clearForward">清空</button>
        </view>
        <textarea :show-confirm-bar="false" :auto-height="true" maxlength="2000" confirm-type="done" v-model="form.prompt"
          placeholder-class="placeholder-class" @input="formVal = form.prompt.replace(promptData.key, promptData.val)"
          placeholder="请输入绘画描述词汇" />
      </view>
      <!--  描述词-->
      <view class="title">
        <view class="title-row">
          <view class="lable-prompt">反向提示词(可选)</view>
          <button class="random-prompt" @click="randomReverse">随机</button>
          <button class="clear-prompt" @click="clearReverse">清空</button>
        </view>
        <textarea :show-confirm-bar="false" :auto-height="true" maxlength="2000" confirm-type="done"
          v-model="form.negative_prompt" placeholder-class="placeholder-class" placeholder="请输入绘画描述词汇" />
      </view>
      <!--  参数配置-->
      <view class="title">
        <view>图片大小</view>
        <scroll-view class="scroll-x" :scroll-with-animation="true" :scroll-bar="false" enable-flex scroll-x>
          <view :class="item.isSelected ? 'model_choose_selected' : 'model_choose'" v-for="(item, index) in size"
            :key="index" @click="handleSize(index)">
            {{ item.text }}
          </view>
        </scroll-view>
      </view>
      <view class="title">
        <view>采样率</view>
        <scroll-view class="scroll-x" :scroll-with-animation="true" :scroll-bar="false" enable-flex scroll-x>
          <view :class="item.isSelected ? 'model_choose_selected' : 'model_choose'" v-for="(item, index) in sampling"
            :key="index" @click="handleSampling(index)">
            {{ item.text }}
          </view>
        </scroll-view>
      </view>
      <view class="title">
        <view>迭代步数</view>
        <scroll-view class="scroll-x" :scroll-with-animation="true" :scroll-bar="false" enable-flex scroll-x>
          <view :class="item.isSelected ? 'model_choose_selected' : 'model_choose'" v-for="(item, index) in iteration"
            :key="index" @click="handleIteration(index)">
            {{ item.text }}
          </view>
        </scroll-view>
      </view>
      <view class="title">
        <view>模型选择</view>
        <scroll-view class="scroll-mx-x" :scroll-with-animation="true" :scroll-bar="false" enable-flex scroll-x>
          <view class="item-rows">
            <view class="item-row" v-for="(_, rowIndex) in Array(Math.ceil(model.length / 3))" :key="rowIndex">
              <view v-for="(_, colIndex) in Array(3)" :key="colIndex">
                <view v-if="model[rowIndex * 3 + colIndex]"
                  :class="model[rowIndex * 3 + colIndex].is_selected ? 'model_choose_selected' : 'model_choose'"
                  @click="handleModel(rowIndex * 3 + colIndex)">
                  {{ model[rowIndex * 3 + colIndex].text_name }}
                </view>
              </view>
            </view>
          </view>
        </scroll-view>
      </view>
    </scroll-view>
    <view class="levitation">
      <button @click="submit" class="sub_btn">立即生成</button>
    </view>
  </view>
</template>

<script>
import GenerateLoadingComponent from "@/pages/drawing/components/generateLoadingComponent.vue";
import LoadingComponent from "@/wxcomponents/components/loadingComponent.vue";
import { ProhibitedUserDisable, ProhibitedTextDetection, StableDiffusionModelSelect } from "@/api/python";
import { isDrawingSucceed, sdConnectivity } from "@/api/drawing";
import env from "@/utils/env";
import prompt from "@/utils/prompt";
import { getToken } from "@/utils/utils";

export default {
  components: { LoadingComponent, GenerateLoadingComponent },
  data() {
    return {
      form: {
        images: '',
        prompt: '',
        width: 512,
        height: 512,
        seed: 0,
        restore_faces: 0,
        rate: '',
        steps: 0,
        modelName: '',
        location: 0,
        negative_prompt: ''
      },
      // 英文提示词
      promptEnglish: '',
      msg: '正在检查绘图服务运行状态',
      //图片大小
      size: [{
        width: 512,
        height: 896,
        isSelected: true,
        text: "竖图(512*869)"
      },
      {
        width: 896,
        height: 512,
        isSelected: false,
        text: "横图(896*512)"
      },
      {
        width: 512,
        height: 512,
        isSelected: false,
        text: "标准"
      },
      {
        width: 1024,
        height: 1024,
        isSelected: true,
        text: "高清"
      }
      ],
      //模型
      model: [],
      //采样率
      sampling: [{
        rate: "Euler a",
        isSelected: false,
        text: "Euler a"
      },
      {
        rate: "Restart",
        isSelected: false,
        text: "Restart"
      },
      {
        rate: "DPM++ SDE Karras",
        isSelected: false,
        text: "SDE Karras"
      },
      {
        rate: "DPM++ 2M SDE Karras",
        isSelected: false,
        text: "2M SDE Karras"
      },
      {
        rate: "DPM++ 2M SDE Exponential",
        isSelected: false,
        text: "2M SDE Exponential"
      },
      {
        rate: "DPM++ 2M SDE Heun Karras",
        isSelected: false,
        text: "2M SDE Heun Karras"
      },
      {
        rate: "DPM++ 2M SDE Heun Exponential",
        isSelected: false,
        text: "2M SDE Heun Exponential"
      },
      {
        rate: "DPM++ 3M SDE Karras",
        isSelected: false,
        text: "3M SDE Karras"
      },
      {
        rate: "DPM++ 3M SDE Exponential",
        isSelected: false,
        text: "3M SDE Exponential"
      }
      ],
      //迭代步数
      iteration: [{
        steps: 20,
        isSelected: false,
        text: "20"
      },
      {
        steps: 30,
        isSelected: false,
        text: "30"
      },
      {
        steps: 40,
        isSelected: false,
        text: "40"
      },
      {
        steps: 50,
        isSelected: false,
        text: "50"
      },
      {
        steps: 60,
        isSelected: false,
        text: "60"
      }
      ]
    };
  },
  created: async function () {
    try {
      const res = await this.sdModelSelect();
      if (res.status == true) {
        this.model = res.data;
        this.model.forEach(m => {
          if (m.is_selected) {
            this.form.modelName = m.model_name;
          }
        });
      }
    } catch (e) {
      console.error(e);
    }
  },
  methods: {
    /**
     * 处理采样率
     * @param index
     */
    handleSampling: function (index) {
      this.sampling.forEach(s => s.isSelected = false)
      this.sampling[index].isSelected = true
      this.form.rate = this.sampling[index].rate
    },
    /**
     * 处理迭代步数
     * @param index
     */
    handleIteration: function (index) {
      this.iteration.forEach(s => s.isSelected = false)
      this.iteration[index].isSelected = true
      this.form.steps = this.iteration[index].steps
    },
    /**
     * 处理模型
     * @param index
     */
    handleModel: function (index) {
      this.model.forEach(s => s.is_selected = false)
      this.model[index].is_selected = true
      this.form.modelName = this.model[index].model_name
    },
    beforeRead: function (e) {
      const { file, callback } = e.detail;
      try {
        if (file.size > 2 * 1024 * 1024) { // 判断图片大小是否超过2MB
          uni.showToast({
            title: '图片超过了2MB,请重新选择',
            icon: 'none',
            duration: 4000
          })
        } else {
          callback(true); // 设置callback为true
        }
      } catch (e) {
        this.form.images = undefined
      }
    },
    /**
     * 返回上一页
     */
    previousPage: function () {
      uni.navigateBack()
    },
    /**
     * 遥测SD状态
     * @returns
     */
    examineServer: async function () {
      let loadingRef = this.$refs.loadingRef;
      try {
        loadingRef.openShow()
        let res = await sdConnectivity(1);
        if (!res) {
          this.msg = '请联系小程序管理员开启绘图服务'
          setTimeout(() => {
            uni.navigateBack();
          }, 3000)
          return
        }
        loadingRef.closeShow()
      } catch (e) {
        this.msg = e
        setTimeout(() => {
          uni.navigateBack();
        }, 3000)

      }

    },
    /**
     *  检查绘图是否成功
     */
    isDrawingSucceed: async function (id) {
      const _this = this
      let generateLoadingRef = this.$refs.generateLoadingRef;
      try {
        let promise = await isDrawingSucceed(id);
        if (promise) {
          //跳转
          generateLoadingRef.closeShow();
          _this.stopTimer()
          uni.navigateTo({
            url: '/pages/drawing/drawingResultView?drawingId=' + id
          })

        }
      } catch (e) {
        uni.showToast({
          title: e,
          icon: 'none',
          duration: 2000
        })
        this.stopTimer()
        setTimeout(() => {
          uni.navigateBack();
        }, 3000)
      }
    },
    /**
     * 关闭定时器
     */
    stopTimer() {
      clearInterval(this.timer);
    },
    /**
     * 清除图片
     */
    deleted: function () {
      this.form.images = ''
    },
    /**
     * 违禁词检测
     */
    textDetection: async function (messages) {
      try {
        const res = await ProhibitedTextDetection({ messages: messages });
        if (res) {
          if (res.data.code === 2004) {
            uni.showToast({
              title: res.data.msg,
              icon: 'none',
              duration: 2000
            });
            return { status: false, message: res.data.msg };
          }
        }
        return { status: true };
      } catch (e) {
        uni.showToast({
          title: '违禁词校验失败，请联系管理员查看原因',
          icon: 'none',
          duration: 2000
        });
        return { status: false, message: '违禁词校验失败，请联系管理员查看原因' };
      }
    },
    /**
     * sd绘图模型查询
     */
    sdModelSelect: async function () {
      try {
        const res = await StableDiffusionModelSelect();
        if (res) {
          return { status: true, data: res };
        }
      } catch (e) {
        uni.showToast({
          title: 'sd绘图模型查询失败，请联系管理员查看原因',
          icon: 'none',
          duration: 2000
        });
        return { status: false, message: 'sd绘图模型查询失败，请联系管理员查看原因' };
      }
    },
    /**
     * 正向随机提示词
     */
    randomForward: function () {
      const _this = this
      // 首先，从 prompt 中随机选择一条数据
      const randomItem = prompt.promptForward[Math.floor(Math.random() * prompt.promptForward.length)];
      // 将 key 和 val 内容分别赋值给相应变量
      _this.form.prompt = randomItem.key;
      _this.promptEnglish = randomItem.val;
    },
    /**
     * 反向随机提示词
     */
    randomReverse: function () {
      const _this = this
      // 首先，从 prompt 中随机选择一条数据
      const randomItem = prompt.promptReverse[Math.floor(Math.random() * prompt.promptReverse.length)];
      // 将 key 和 val 内容分别赋值给相应变量
      _this.form.negative_prompt = randomItem.key;
      _this.promptEnglish = randomItem.val;
    },
    /**
     * 清空正向提示词
     */
    clearForward: function () {
      const _this = this
      _this.form.prompt = '';
    },
    /**
     * 清空反向提示词
     */
    clearReverse: function () {
      const _this = this
      _this.form.negative_prompt = '';
    },
    /**
     * 提交
     */
    submit: async function () {
      const { images, prompt } = this.form;
      if (!images) {
        uni.showToast({
          title: '请上传参考图',
          icon: 'none',
          duration: 4000
        })
        return
      }
      // 判断this.promptEnglish是否有值 有值的话替换
      if (this.promptEnglish) {
        this.form.prompt = this.promptEnglish;
      }
      if (!prompt) {
        uni.showToast({
          title: '请填写描述',
          icon: 'none',
          duration: 4000
        })
        return
      }
      const _this = this
      const tmplIds = env.tmplIds
      const baseUrl = env.baseUrl;
      // 构造一个字典 同步web端
      let messages = {
        'content': _this.form.prompt,
        'emailAccount': '',
        'userInfo': JSON.stringify(uni.getStorageSync('user'))
      };
      // 违禁状态检测
      let statusResult = await ProhibitedUserDisable(messages);
      if (statusResult.data.code != 2000) {
        uni.showToast({
          title: statusResult.data.msg,
          icon: 'none',
          duration: 2000
        });
        return;
      };
      // 违禁词检测
      let textResult = await _this.textDetection(messages);
      if (!textResult.status) {
        uni.showToast({
          title: textResult.message,
          icon: 'none',
          duration: 2000
        });
        return;
      };
      uni.requestSubscribeMessage({
        tmplIds: tmplIds,
        success: async function (res) {
          let s = baseUrl + '/drawing/sd/image2image';
          if (res[tmplIds[0]] === 'accept') {
            let generateLoadingRef = _this.$refs.generateLoadingRef;
            uni.showLoading({
              title: '正在加入队列~',
              mask: true
            });
            wx.uploadFile({
              url: s,
              filePath: _this.form.images,
              name: 'images',
              header: {
                'token': getToken()
              },
              formData: {
                'width': _this.form.width,
                'prompt': _this.form.prompt,
                'height': _this.form.height,
                'seed': _this.form.seed,
                'restore_faces': _this.form.restore_faces,
                'rate': _this.form.rate,
                'steps': _this.form.steps,
                "modelName": _this.form.modelName,
                "negative_prompt": _this.form.negative_prompt
              },
              async success(res) {
                let parse = JSON.parse(res.data);
                if (parse.code === 200) {
                  let data = parse.data;
                  this.location = data.location
                  uni.showToast({
                    title: '操作成功',
                    icon: 'none',
                    duration: 2000
                  })
                  generateLoadingRef.openShow()
                  _this.timer = setInterval(() => {
                    _this.isDrawingSucceed(data.drawingId)
                  }, 5000);
                } else {
                  _this.stopTimer()
                  uni.showToast({
                    title: parse.msg,
                    icon: 'none',
                    duration: 2000
                  })
                  uni.hideLoading()
                }

              },
              fail(res) {
                console.log(res)
                console.log('错误')
                uni.showToast({
                  title: '服务貌似被关闭了',
                  icon: 'none',
                  duration: 1000
                })
                uni.hideLoading()
                setTimeout(() => {
                  uni.navigateBack();
                }, 2000)
              }
            })

          }
        }
      })
    }

    ,
    /**
     * 处理大小
     * @param index
     */
    handleSize: function (index) {
      this.size.forEach(s => s.isSelected = false)
      this.size[index].isSelected = true
      this.form.height = this.size[index].height
      this.form.width = this.size[index].width
    }
    ,

    /**
     * 解析用户选择的图片
     * @param e
     */
    imageCacheCallback: function (e) {
      const { file } = e.detail;
      this.form.images = file.url
    }
    ,
    /**
     * 预览图片
     * @param url
     */
    previewImage(url) {
      uni.previewImage({
        urls: [url]
      });
    }
  },
  beforeDestroy() {
    clearInterval(this.timer);
  },
  onLoad() {

    this.examineServer()
  },
  //刷新次数
  onUnload() {
    uni.$emit('master_userInfo')
  },

}
</script>

<style lang="scss">
.container {
  animation: fadeIn 0.5s ease-in-out forwards;
  padding: 20rpx;
  color: white;
}

.main-scroll {
  height: 85vh
}

.title {
  padding-top: 30rpx;
  font-size: 28rpx
}

.title-row {
  display: flex;
  align-items: center;
}

.lable-prompt {
  width: 300rpx;
}

.random-prompt {
  background-color: rgb(138, 117, 255);
  color: #ffffff;
  font-size: 25rpx;
  border: none;
  border-radius: 10px;
  padding-left: 30rpx;
  padding-right: 30rpx;
  height: 60rpx;
  margin-right: -120rpx;
  justify-content: center;
  align-items: center;
}

.clear-prompt {
  background-color: rgb(138, 117, 255);
  color: #ffffff;
  font-size: 25rpx;
  border: none;
  border-radius: 10px;
  padding-left: 30rpx;
  padding-right: 30rpx;
  height: 60rpx;
  margin-right: 20rpx;
  justify-content: center;
  align-items: center;
}

.model_choose,
.model_choose_selected {
  font-size: 25rpx;
  border-radius: 10rpx;
  padding-left: 30rpx;
  padding-right: 30rpx;
  height: 60rpx;
  margin-right: 20rpx;
  display: flex;
  justify-content: center;
  align-items: center;
}

.model_choose {
  background-color: rgb(138, 117, 255);
}

.model_choose_selected {
  background-color: rgb(92, 72, 204);
}

.scroll-mx-x {
  display: flex;
  overflow-x: auto;
  white-space: nowrap;
  margin-top: 20rpx;
}

.item-rows {
  display: inline-flex;
  flex-direction: column;
}

.item-row {
  display: flex;
  justify-content: flex-start;
  margin-bottom: 20rpx;
}

.preview_model {
  display: flex;
  justify-content: center;
  align-items: center;
  padding-top: 20rpx
}

.placeholder-class {
  font-size: 25rpx;
}

.scroll-x {
  height: 60rpx;
  display: flex;
  overflow-x: auto;
  white-space: nowrap;
  margin-top: 20rpx;
}

textarea {
  font-size: 25rpx;
  margin-top: 20rpx;
  color: #dadada;
  background-color: #1e1e1e;
  padding: 10rpx;
  width: 695rpx;
  border-radius: 15rpx;
  max-height: 500rpx;
  min-height: 130rpx;
}

.preview_choose {
  background-color: rgb(138, 117, 255);
  color: #ffffff;
  font-size: 24rpx;
  margin: 0 10rpx
}

.preview_deleted {
  background-color: #f43030;
  color: #ffffff;
  font-size: 24rpx;
  margin: 0 10rpx
}

.uploader_subassembly {
  text-align: center;
  font-size: 23rpx;
  color: #868585;
}

.levitation {
  position: fixed;
  z-index: 2;
  left: 120rpx;
  bottom: 5vh;
}

.sub_btn {
  background-color: rgb(138, 117, 255);
  color: white;
  width: 500rpx;
  font-size: 30rpx
}

.uploader_prompt {
  font-size: 26rpx;
  color: #e3e3e3;
  padding-bottom: 30rpx;
  padding-top: 10rpx
}

.uploader_container {
  background-color: #1e1e1e;
  margin-top: 20rpx;
  border-radius: 20rpx;
  height: 400rpx;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center
}

.preview_image {
  width: 240rpx;
  height: 240rpx;
  border-radius: 20rpx
}
</style>
