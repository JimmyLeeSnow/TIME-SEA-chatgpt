<template>
  <div class="u_container">
    <div class="button-row">
      <el-button color="#626aef" style="width: 100px" @click="dialogFormVisible = true">新增模型</el-button>
    </div>
    <el-table :data="dataTables" height="70%" :header-cell-style="{
      background: ' rgb(27,30,32)',
      borderColor: '#202020',
      }" style="background-color: rgb(27, 30, 32)" :row-style="{
        height: '100%',
        background: ' rgb(27,30,32)',
        border: 'none',
      }">
      <el-table-column prop="sd_id" label="标识" width="60" />
      <el-table-column prop="model_name" label="配置名称" width="360" />
      <el-table-column prop="text_name" label="展示名称" />
      <el-table-column prop="is_selected" label="是否默认" width="90" />
      <el-table-column prop="created_time" label="创建时间" />
      <el-table-column fixed="right" label="操作" width="100">
        <template #header>
          <el-input style="width: 180px" v-model="prompt" size="small" placeholder="模糊搜索" @change="search" />
        </template>
        <template #default="scope">
          <el-button link type="primary" size="small" @click="deleteProduct(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div style="display: flex; justify-content: right; padding-top: 10px">
      <el-pagination layout="prev, pager, next" :total="total" :page-size="15" background
        @current-change="handleCurrentChange" />
    </div>
  </div>
  <el-dialog v-model="dialogFormVisible" width="400px" x style="background-color: rgb(27, 30, 32); padding-top: 20px">
    <el-form>
      <el-form-item label="配置名称" label-width="100px">
        <el-input autocomplete="off" style="width: 180px" v-model="form.modelName" />
      </el-form-item>
    </el-form>
    <el-form>
      <el-form-item label="展示名称" label-width="100px">
        <el-input autocomplete="off" style="width: 180px" v-model="form.textName" />
      </el-form-item>
    </el-form>
    <el-form>
      <el-form-item label="是否默认" label-width="100px">
        <el-radio-group v-model="form.isSelected">
          <el-radio class="custom-radio" label="1">是</el-radio>
          <el-radio class="custom-radio" label="0">否</el-radio>
        </el-radio-group>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button type="default" color="#626aef" @click="handleAddProduct">
          创建
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script>
import { onMounted, ref } from "vue";
import store from "@/store";
import {
  StableDiffusionModelSelect,
  StableDiffusionModelCurd
} from "../../../../api/YSideApi";
import { ElLoading, ElMessageBox, ElNotification } from "element-plus";

export default {
  name: "productView",
  computed: {
    store() {
      return store;
    },
  },
  setup() {
    const dialogFormVisible = ref(false);
    let loginVisible = ref(false);
    const dataTables = ref([]);
    const current = ref(1);
    const total = ref(0);
    const amount = ref(0);
    const prompt = ref("");
    let load = ref(true);
    let empty = ref(false);
    let error = ref(false);
    const form = ref({
      textName: "",
      isSelected: undefined,
      modelName: undefined,
    });
    onMounted(() => {
      if (store.getters.userinfo && store.getters.userinfo.type === "ADMIN") {
        handleCurrentChange(current.value);
      }
    });

    async function handleAddProduct() {
      const { modelName, textName, isSelected } = form.value;
      if (!textName) {
        ElNotification({
          title: "错误",
          message: "展示名称不能为空",
          type: "error",
        });
        return;
      }
      if (!isSelected) {
        ElNotification({
          title: "错误",
          message: "默认选择不能为空",
          type: "error",
        });
        return;
      }
      if (!modelName) {
        ElNotification({
          title: "错误",
          message: "配置名称不能为空",
          type: "error",
        });
        return;
      }
      ElLoading.service({
        fullscreen: true,
        text: "正在重载数据...",
        spinner: "el-icon-loading",
        background: "rgba(0, 0, 0, 0.7)",
      });
      try {
        // 组装一下传输的数据
        let tempDict = {'data': form.value, 'curd_type': 'add', 'user': localStorage.getItem('login_email')}
        await StableDiffusionModelCurd(tempDict);
        // 关闭加载图标
        ElLoading.service().close();
        prompt.value = "";
        current.value = 1;
        await handleCurrentChange(1);
        // 弹出退出登录成功提示框
        ElNotification({
          message: "新增成功",
          type: "success",
        });
        dialogFormVisible.value = false;
      } catch (e) {
        ElNotification({
          title: "错误",
          message: e,
          type: "error",
        });
      }
    }

    function search() {
      current.value = 1;
      dataTables.value = [];
      handleCurrentChange(1);
    }

    async function deleteProduct(data) {
      try {
        await ElMessageBox({
          title: "提示",
          message: "确定要删除?",
          confirmButtonText: "确定",
          cancelButtonText: "再想想",
          showCancelButton: true,
          type: "warning",
        });
        ElLoading.service({
          fullscreen: true,
          text: "正在删除...",
          spinner: "el-icon-loading",
          background: "rgba(0, 0, 0, 0.7)",
        });
        // 组装一下传输的数据
        let tempDict = {'data': data.sd_id, 'curd_type': 'del', 'user': localStorage.getItem('login_email')}
        await StableDiffusionModelCurd(tempDict);
        // 关闭加载图标
        ElLoading.service().close();
        prompt.value = "";
        current.value = 1;
        await handleCurrentChange(1);
        ElNotification({
          message: "删除成功",
          type: "success",
        });
      } catch (e) {
        console.log("取消删除");
      }
    }

    async function handleCurrentChange(pageNum) {
      try {
        let res = await StableDiffusionModelSelect(pageNum, prompt.value);
        if (res.length > 0) {
          dataTables.value = res;
        } else {
          empty.value = true;
        }
        current.value = res.current;
        total.value = res.total;
        load.value = false;
        error.value = false;
      } catch (e) {
        load.value = false;
        error.value = true;
      }
    }

    return {
      deleteProduct,
      search,
      load,
      error,
      empty,
      amount,
      total,
      loginVisible,
      handleCurrentChange,
      dataTables,
      prompt,
      dialogFormVisible,
      handleAddProduct,
      form,
    };
  },
};
</script>

<style scoped>
@keyframes explainAnimation {
  from {
    transform: scale(0);
  }

  to {
    transform: scale(1);
  }
}

::v-deep(.el-table--enable-row-hover .el-table__body tr:hover td.el-table__cell) {
  background: none !important;
}

::v-deep(.el-pagination .is-background .el-pager li:not(.is-disabled).is-active) {
  background-color: rgb(125, 128, 255);
}

::v-deep(.el-table-fixed-column--right) {
  background: rgb(27, 30, 32) !important;
}

::v-deep(.el-pagination.is-background .el-pager li:not(.is-disabled).is-active) {
  background-color: rgb(125, 128, 255) !important;
}

::v-deep(.el-table--enable-row-hover .el-table__body tr:hover td.el-table__cell) {
  background: none;
}

.button-row {
  margin-bottom: 30px;
  margin-top: 30px;
}

.head_model {
  display: flex;
  background-color: #7d80ff;
  height: 130px;
  margin-bottom: 20px;
  align-items: center;
  border-radius: 3px;
  box-shadow: 0 2px 6px rgb(27, 30, 32);
}

.head_model_style {
  padding-left: 40px;
  color: white;
}

.number_people {
  font-size: 35px;
  font-weight: 600;
}

.text_people {
  font-size: 15px;
  margin-top: 5px;
  padding-left: 5px;
}

::v-deep .el-radio__inner {
  background: #303030;
}

::v-deep .el-radio__wrapper {
  background: #303030;
}

::v-deep .el-input__inner {
  background: rgb(39, 41, 42);

  font-weight: 400;
  color: #b7b7b7;
}

::v-deep .el-input__wrapper {
  background: rgb(39, 41, 42);
  box-shadow: none;
}
</style>
