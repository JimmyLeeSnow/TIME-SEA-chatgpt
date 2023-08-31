<template>
  <view class="container">
    <loading-component ref="loadingRef" :msg="msg" :degree="0.8" />
    <generate-loading-component ref="generateLoadingRef" :location="form.location" />
    <scroll-view class="main-scroll" scroll-y>
      <!--  描述词-->
      <view class="title">
        <view>正向提示词</view>
        <textarea :show-confirm-bar="false" :auto-height="true" maxlength="2000" confirm-type="done" v-model="form.prompt"
          placeholder-class="placeholder-class" placeholder="请输入绘画描述词汇" />
      </view>
      <!--  描述词-->
      <view class="title">
        <view>反向提示词(可选)</view>
        <textarea :show-confirm-bar="false" :auto-height="true" maxlength="2000" confirm-type="done"
          v-model="form.negative_prompt" placeholder-class="placeholder-class" placeholder="请输入绘画描述词汇" />
      </view>
      <!--  参数配置-->
      <view class="title">
        <view>图片大小</view>
        <scroll-view class="scroll-x" :scroll-with-animation="true" :scroll-bar="false" enable-flex scroll-x>
          <view :class="item.isSelected ? 'model_choose_selected' : 'model_choose'" v-for="(item, index) in size" :key="index"
            @click="handleSize(index)">
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
                  :class="model[rowIndex * 3 + colIndex].isSelected ? 'model_choose_selected' : 'model_choose'"
                  @click="handleModel(rowIndex * 3 + colIndex)">
                  {{ model[rowIndex * 3 + colIndex].text }}
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


import env from "@/utils/env";
import { addSdDrawingTextTaskQueue, isDrawingSucceed, sdConnectivity } from "@/api/drawing";
import { ProhibitedUserDisable, ProhibitedTextDetection } from "@/api/python";
import LoadingComponent from "@/wxcomponents/components/loadingComponent.vue";
import GenerateLoadingComponent from "@/pages/drawing/components/generateLoadingComponent.vue";

export default {
  components: { LoadingComponent, GenerateLoadingComponent },
  data() {
    return {
      form: {
        prompt: '',
        width: 512,
        height: 512,
        seed: 0,
        restore_faces: 0,
        rate: '',
        steps: 0,
        modelName: '',
        location: 0,
        negative_prompt: '',

      },
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
        rate: "DPM++ SDE Karras",
        isSelected: false,
        text: "SDE Karras"
      },
      {
        rate: "DPM++ 2S a Karras",
        isSelected: false,
        text: "2S a Karras"
      },
      {
        rate: "DPM++ 2M alt Karras",
        isSelected: false,
        text: "2M alt Karrass"
      },
      {
        rate: "DPM++ 2M Karras",
        isSelected: false,
        text: "2M Karras"
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
      ],
      timer: undefined
    };
  },
  created() {
    this.model = env.sdModels
    this.model.forEach(m => {
      if (m.isSelected) {
        this.form.modelName = m.modelName
      }
    })
  },
  methods: {
    /**
     * 返回上一页
     */
    previousPage: function () {
      uni.navigateBack()
    },
    stopTimer() {
      clearInterval(this.timer);
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
     * 提交
     */
    submit: async function () {
      const { prompt } = this.form;
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
      let generateLoadingRef = _this.$refs.generateLoadingRef;
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
          if (res[tmplIds[0]] === 'accept') {
            uni.showLoading({
              title: '正在加入队列...',
              mask: true
            });
            try {
              let data = await addSdDrawingTextTaskQueue(_this.form);
              uni.showToast({
                title: '提交成功',
                icon: 'none',
                duration: 2000
              });
              _this.form.location = data.location
              generateLoadingRef.openShow()
              _this.timer = setInterval(() => {
                _this.isDrawingSucceed(data.drawingId)
              }, 5000);
            } catch (e) {
              uni.hideLoading()
              uni.showToast({
                title: e,
                icon: 'none',
                duration: 2000
              });
            }
          } else {
            uni.showModal({
              title: '订阅消息',
              content: '您当前拒绝接收作品消息通知，是否去开启?',
              confirmText: '开启授权',
              confirmColor: '#345391',
              cancelText: '仍然拒绝',
              cancelColor: '#999999',
              success: res => {
                if (res.confirm) {
                  uni.openSetting({
                    success(res) {
                      console.log(res)
                    },
                  })
                }
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
    },
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
      this.model.forEach(s => s.isSelected = false)
      this.model[index].isSelected = true
      this.form.modelName = this.model[index].modelName
    }
    ,
    /**
     * 检查SD运行状态 初步验证用户是否有足够次数
     * @returns {Promise<void>}
     */
    examineServer: async function () {
      let loadingRef = this.$refs.loadingRef;
      try {
        loadingRef.openShow()
        let res = await sdConnectivity(0);
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
    }
  },
  //刷新次数
  onUnload() {
    uni.$emit('master_userInfo')
    clearInterval(this.timer);
  },
  onLoad() {
    this.examineServer()
  }

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
