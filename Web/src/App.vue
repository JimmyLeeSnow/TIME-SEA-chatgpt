<template>
  <NavigationBar />
  <LeftNavigationBar />
  <el-dialog class="announcement" v-model="dialogVisible" center align-center width="380px"
    style="background-color: rgb(27, 30, 32)">
    <span style="text-align: center">{{ context }}</span>
    <template #footer>
      <span class="dialog-footer">
        <el-button type="primary" @click="dialogVisible = false" color="#626aef">
          朕已阅
        </el-button>
      </span>
    </template>
  </el-dialog>
  <levitation-ball />
  <div id="footer">
    2023 - 2023 © 佑云<a href="https://chat.yycld.com" target="_blank" rel="noopener noreferrer"
      style="color: inherit; text-decoration: none; margin-right: 16px; margin-left: 10px;">WOO CLOUD PLUS</a>
    <span id="htmer_time">该网站已运行 <span id="days"></span>天<span id="hours"></span>时<span id="minutes"></span>分<span
        id="seconds"></span>秒</span><br />
  </div>
</template>

<script>
import { useStore } from "vuex";
import LeftNavigationBar from "@/components/LeftNavigationBar.vue";
import LevitationBall from "@/components/LevitationBall.vue";
import NavigationBar from "@/components/NavigationBar.vue";
import { getAnnouncement } from "../api/BSideApi";
import { onMounted, ref } from "vue";

export default {
  components: { LeftNavigationBar, NavigationBar, LevitationBall },
  setup() {
    let store = useStore();
    store.commit("initState");

    // 网站运行时间显示
    function secondToDate(second) {
      if (!second || second < 0) {
        return [0, 0, 0, 0];
      }

      var time = [];

      var days = Math.floor(second / (24 * 3600));
      time.push(days);

      second %= 24 * 3600;
      var hours = Math.floor(second / 3600);
      time.push(hours);

      second %= 3600;
      var minutes = Math.floor(second / 60);
      time.push(minutes);

      var seconds = second % 60;
      time.push(seconds);

      return time;
    }

    function updateClock() {
      var create_time = Math.round(new Date("2023-05-28T00:00:00Z").getTime() / 1000);
      var current_time = Math.round(new Date().getTime() / 1000);
      var currentTime = secondToDate(current_time - create_time);

      var daysElement = document.getElementById("days");
      var hoursElement = document.getElementById("hours");
      var minutesElement = document.getElementById("minutes");
      var secondsElement = document.getElementById("seconds");

      if (
        daysElement !== null &&
        hoursElement !== null &&
        minutesElement !== null &&
        secondsElement !== null
      ) {
        daysElement.textContent = currentTime[0];
        hoursElement.textContent = currentTime[1];
        minutesElement.textContent = currentTime[2];
        secondsElement.textContent = currentTime[3];
        daysElement.style.color = "#409eff";
        hoursElement.style.color = "#409eff";
        minutesElement.style.color = "#409eff";
        secondsElement.style.color = "#409eff";
      }
    }

    // 每秒刷新一次
    setInterval(updateClock, 1000);

    const dialogVisible = ref(false);
    const context = ref("");
    onMounted(() => {
      setTimeout(() => {
        getAnnouncementData();
      }, 100);
    });

    async function getAnnouncementData() {
      try {
        let announcement = await getAnnouncement();
        if (announcement) {
          let item = localStorage.getItem("announcement");
          if (item !== null) {
            let parse = JSON.parse(item);
            if (parse.logotypeId !== announcement.logotypeId) {
              localStorage.setItem(
                "announcement",
                JSON.stringify(announcement)
              );
              context.value = announcement.context;
              dialogVisible.value = true;
            }
          } else {
            localStorage.setItem("announcement", JSON.stringify(announcement));
            context.value = announcement.context;
            dialogVisible.value = true;
          }
        }
      } catch (e) {
        console.log(e);
      }
    }

    return {
      dialogVisible,
      context,
    };
  },
  mounted() {
    const script = document.createElement('script');
    script.id = 'LA-DATA-WIDGET';
    script.crossOrigin = 'anonymous';
    script.src = 'https://v6-widget.51.la/v6/K4zEC7JJ8vWtJdWg/quote.js?theme=#1690FF,#666666,#999999,#FFFFFF,#FFFFFF,#1690FF,12&f=12';
    document.getElementById('footer').appendChild(script);
  }
};
// 此内容未经授权不能删除
// eslint-disable-next-line no-console
console.info('%cWOO CLOUD PLUS %cVer1.3.1 %chttps://chat.yycld.com/',
  'color:#409EFF;font-size: 22px;font-weight:bolder',
  'color:#999;font-size: 12px',
  'color:#333',
);
</script>

<style>
.announcement {
  width: 25%;
  border-radius: 10px;
}

@media (max-width: 767px) {
  .announcement {
    width: 70%;
  }
}

#app {
  width: 100%;
  height: 100%;
  flex-direction: column;
  display: flex;
  font-family: "PingFang SC", "Helvetica Neue", Helvetica, "Hiragino Sans GB",
    "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
  box-sizing: border-box;
  padding: 20px;
  letter-spacing: 1px;
}

#footer {
  margin-top: 5px;
  color: gray;
  font-size: 14px;
  text-align: center;
}

@media only screen and (max-width: 767px) {
  #app {
    padding: 0;
  }
}

html,
body {
  margin: 0;
  padding: 0;
  /*background: #f6f6f6;*/
  background: #1d2022ff;
  color: #303030;
  width: 100%;
  height: 100%;
}

/* TODO 滚动条样式*/
::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}

::-webkit-scrollbar-thumb {
  border-radius: 10px;
  background: rgba(0, 0, 0, 0.2);
}

::-webkit-scrollbar-track {
  /* box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.1); */
  border-radius: 0;
  background: rgba(0, 0, 0, 0.1);
  display: block;
}

.login-dialog>header {
  display: none;
}

.login-dialog>.el-dialog__body {
  padding: 0 !important;
}

.el-switch__core {
  background: #393939 !important;
}

.el-input-group__append {
  box-shadow: none !important;
}

.el-input-group__append {
  background: none !important;
}

.el-pagination .btn-prev,
.el-pagination .btn-next {
  background-color: rgb(35, 40, 42) !important;
}

.el-pagination .el-pager li:not(.active) {
  background-color: rgb(35, 40, 42) !important;
  color: darkgray !important;
}
</style>
