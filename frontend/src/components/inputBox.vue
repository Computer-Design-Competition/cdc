<template>
  <div class="input-box">
    <el-form :inline="true"  class="demo-form-inline">
      <el-form-item label="记录日期">
        <el-date-picker v-model="date" align="right" type="date" placeholder="选择日期"></el-date-picker>
      </el-form-item>
      <el-form-item label="所在地区">
        <el-cascader
          v-model="province"
          :options="chinaList"
          :props="{ expandTrigger: 'hover' }"
          @change="handleChange"
        ></el-cascader>
      </el-form-item>
      <el-form-item>
        <el-input placeholder="请输入确诊人数" v-model="detail.cofirmed"></el-input>
      </el-form-item>
      <el-form-item>
        <el-input placeholder="请输入治愈人数" v-model="detail.cured"></el-input>
      </el-form-item>
      <el-form-item>
        <el-input placeholder="请输入死亡人数" v-model="detail.death"></el-input>
      </el-form-item>
    </el-form><el-form :inline="true"  class="demo-form-inline">
      <el-form-item label="记录日期">
        <el-date-picker v-model="date" align="right" type="date" placeholder="选择日期"></el-date-picker>
      </el-form-item>
      <el-form-item label="所在地区">
        <el-cascader
          v-model="province"
          :options="chinaList"
          :props="{ expandTrigger: 'hover' }"
          @change="handleChange"
        ></el-cascader>
      </el-form-item>
      <el-form-item>
        <el-input placeholder="请输入确诊人数" v-model="detail.cofirmed"></el-input>
      </el-form-item>
      <el-form-item>
        <el-input placeholder="请输入治愈人数" v-model="detail.cured"></el-input>
      </el-form-item>
      <el-form-item>
        <el-input placeholder="请输入死亡人数" v-model="detail.death"></el-input>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import axios from "axios";
// import echart from "../plugins/echart";
axios.defaults.withCredentials = true;

export default {
  name: "inputBox",
  props: {},
  data() {
    return {
      pickerOptions: {
        shortcuts: [
          {
            text: "今天",
            onClick(picker) {
              picker.$emit("pick", new Date());
            }
          },
          {
            text: "昨天",
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() - 3600 * 1000 * 24);
              picker.$emit("pick", date);
            }
          },
          {
            text: "一周前",
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() - 3600 * 1000 * 24 * 7);
              picker.$emit("pick", date);
            }
          }
        ]
      },
      date: "",
      chinaList: [],
      province: [],
      detail: {}
    };
  },
  async mounted() {
    await this.getProvinces();
  },
  methods: {
    async getProvinces() {
      await axios.get("http://192.168.43.14:8080/world.json").then(res => {
        this.chinaList = res.data.chinaList;
      });
    },
    handleChange(value) {
      console.log(value);
    }
  }
};
</script>

<style scoped>
.input-box {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 0 3%;
  width: 100%;
}
</style>