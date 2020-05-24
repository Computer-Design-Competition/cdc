<template>
  <div class="container">
    <el-menu default-active="1" class="el-menu-demo" mode="horizontal" @select="handleSelect">
      <el-menu-item index="1">主页</el-menu-item>
      <el-submenu index="2">
        <template slot="title">地区</template>
        <el-submenu index="2-1" :popper-append-to-body="popper">
          <template slot="title">国内</template>
          <div class="sub-menu">
            <div v-for="item in chinaList" :key="item.value" :index="item.value">
              <el-submenu :index="item.value" v-if="item.children">
                <template slot="title">{{item.label}}</template>
                <div class="sub-menu">
                  <el-menu-item :index="item.value+'-0'">不选择市</el-menu-item>
                  <el-menu-item
                    v-for="city in item.children"
                    :key="city.value"
                    :index="city.value"
                  >{{city.label}}</el-menu-item>
                </div>
              </el-submenu>
              <el-menu-item :index="item.value" v-else>{{item.label}}</el-menu-item>
            </div>
          </div>
        </el-submenu>
        <el-submenu index="2-2" :popper-append-to-body="popper">
          <template slot="title">国外</template>
          <div class="sub-menu">
            <el-menu-item
              v-for="country in worldList"
              :key="country.value"
              :index="country.value"
            >{{country.label}}</el-menu-item>
          </div>
        </el-submenu>
      </el-submenu>
      <el-menu-item index="3">上传数据</el-menu-item>
      <el-menu-item index="4">下载数据</el-menu-item>
    </el-menu>
    <el-carousel height="550px" v-show="showIndex==1">
      <el-carousel-item>
        <div class="chart" id="chart1"></div>
      </el-carousel-item>
      <el-carousel-item>
        <div class="chart" id="chart2"></div>
      </el-carousel-item>
      <el-carousel-item>
        <div class="chart" id="chart3" ref="chart3"></div>
      </el-carousel-item>
      <el-carousel-item>
        <div class="chart" id="chart6"></div>
      </el-carousel-item>
      <el-carousel-item>
        <div class="chart" id="chart7"></div>
      </el-carousel-item>
      <el-carousel-item>
        <div class="chart" id="chart8"></div>
      </el-carousel-item>
      <el-carousel-item>
        <div class="chart" id="chart9"></div>
      </el-carousel-item>
    </el-carousel>
    <div class="box" v-show="showIndex==2">
      <el-carousel height="550px" v-show="worldChart">
        <el-carousel-item>
          <div class="chart" id="chart4"></div>
        </el-carousel-item>
        <el-carousel-item>
          <div class="chart" id="chart5"></div>
        </el-carousel-item>
      </el-carousel>
      <el-carousel height="550px" v-show="provinceChart">
        <el-carousel-item>
          <div class="chart" id="prochart1"></div>
        </el-carousel-item>
        <el-carousel-item>
          <div class="chart" id="prochart2"></div>
        </el-carousel-item>
        <el-carousel-item>
          <div class="chart" id="prochart3"></div>
        </el-carousel-item>
      </el-carousel>
      <el-carousel height="550px" v-show="cityChart">
        <el-carousel-item>
          <div class="chart" id="citychart1"></div>
        </el-carousel-item>
        <el-carousel-item>
          <div class="chart" id="citychart2"></div>
        </el-carousel-item>
      </el-carousel>
    </div>
    <div class="box" v-show="showIndex == 3">
      <inputBox></inputBox>
      <el-button @click="upload">上传</el-button>
      <el-upload
        action="http://118.31.41.159:5000/upload_data/"
        list-type="picture-card"
        :auto-upload="false"
      >
        <i slot="default" class="el-icon-plus"></i>
        <div slot="file" slot-scope="{file}">
          <img class="el-upload-list__item-thumbnail" :src="file.url" alt />
          <span class="el-upload-list__item-actions">
            <span class="el-upload-list__item-preview" @click="handlePictureCardPreview(file)">
              <i class="el-icon-zoom-in"></i>
            </span>
            <span
              v-if="!disabled"
              class="el-upload-list__item-delete"
              @click="handleDownload(file)"
            >
              <i class="el-icon-download"></i>
            </span>
            <span v-if="!disabled" class="el-upload-list__item-delete" @click="handleRemove(file)">
              <i class="el-icon-delete"></i>
            </span>
          </span>
        </div>
      </el-upload>
      <el-dialog :visible.sync="dialogVisible">
        <img width="100%" :src="dialogImageUrl" alt />
      </el-dialog>
    </div>
    <div class="box" v-show="showIndex==4">
      <el-button @click="download">下载</el-button>
    </div>
    <!-- <el-button @click="login">登录</el-button> -->

    <!-- <a id="test" @click="clickDownload(this)" download="file.csv" href=>download</a> -->
  </div>
</template>
<script>
import api from "../api/api";
import axios from "axios";
import inputBox from "../components/inputBox";
// import echart from "../plugins/echart";
axios.defaults.withCredentials = true;

export default {
  name: "index",
  data() {
    return {
      showIndex: 1,
      popper: false,
      provinceChart: false,
      cityChart: false,
      worldChart: false,
      dialogImageUrl: "",
      dialogVisible: false,
      disabled: false,
      file: null,
      chinaList: [],
      worldList: []
    };
  },
  async mounted() {
    const date = this.getDay(-1, "-");
    let globalData = await api.getdata({ date, type: "accumulated" });
    let chinaData = await api.getdata({
      date,
      type: "accumulated",
      country: "china"
    });
    let chinaLine = await api.getLine({
      date,
      type: "accumulated",
      country: "china"
    });
    let worldLine = await api.getLine({ date, type: "accumulated" });
    let somBar = await api.getBar({ date, type: "someday" });
    let allBar = await api.getBar({ date, type: "accumulated" });
    this.drawWorldLine("chart8", "全球累计", worldLine, [
      "累计确诊",
      "累计治愈",
      "累计死亡"
    ]);
    this.drawWorldLine("chart9", "中国累计", chinaLine, [
      "累计确诊",
      "累计治愈",
      "累计死亡"
    ]);
    this.drawWorldBar("chart6", "世界各国累计", allBar, [
      "累计确诊",
      "累计治愈",
      "累计死亡"
    ]);
    this.drawWorldBar("chart7", "世界各国单日新增", somBar, [
      "单日新增确诊",
      "单日新增治愈",
      "单日新增死亡"
    ]);

    globalData = globalData.detail.map(data => {
      return {
        name: data.name,
        value: [data.confirmed, data.cured, data.death]
      };
    });
    chinaData = chinaData.detail.map(data => {
      return {
        name: data.name,
        value: [data.confirmed, data.cured, data.death]
      };
    });

    let namemap = {};
    let chinamap = {};
    await axios.get("http://192.168.43.14:8080/world.json").then(res => {
      namemap = res.data.namemap;
      chinamap = res.data.chinamap;
      this.chinaList = res.data.chinaList;
      this.worldList = res.data.worldList;
      globalData = globalData.map(data => {
        return {
          name: namemap[data.name],
          value: data.value
        };
      });
      chinaData = chinaData.map(data => {
        return {
          name: chinamap[data.name],
          value: data.value
        };
      });
    });

    this.drawChart("chart1", namemap, globalData, "全球累计");
    this.drawChina("chart3", "中国累计", chinamap, chinaData);
  },
  methods: {
    clickDownload(aLink) {
      let str = this.file;
      str = encodeURIComponent(str);
      aLink.href = "data:text/csv;charset=utf-8,\ufeff" + str;
      aLink.click();
    },
    handleRemove(file) {
      console.log(file);
    },
    handleDownload(file) {
      console.log(file);
      let res = api.postFile(file.raw);
      this.file = res;
    },
    async handleSelect(key, keyPath) {
      if (keyPath.length > 1) {
        this.showIndex = keyPath[0];
      } else {
        this.showIndex = key;
      }
      if (keyPath[1] === "2-2") {
        this.worldChart = true;
        let country = this.worldList.filter(item => item.value === keyPath[2]);
        country = country[0].name;
        let somData = await api.getLine({
          date: this.getDay(-1, "-"),
          type: "someday",
          country
        });
        let allData = await api.getLine({
          date: this.getDay(-1, "-"),
          type: "accumulated",
          country
        });
        this.drawWorldLine("chart4", "单日", somData, [
          "单日新增确诊",
          "单日新增治愈",
          "单日新增死亡"
        ]);
        this.drawWorldLine("chart5", "累计", allData, [
          "累计确诊",
          "累计治愈",
          "累计死亡"
        ]);
      }
      if (keyPath[1] === "2-1") {
        let province = this.chinaList.filter(item => item.value === keyPath[2]);
        let city = [];
        if (keyPath.length === 4) {
          city = province[0]["children"].filter(
            city => city.value === keyPath[3]
          );
        }
        province = province[0].label;
        if (city.length !== 0) {
          this.cityChart = true;
          this.provinceChart = false;
          let somCityLin = await api.getLine({
            date: this.getDay(-1, "-"),
            type: "someday",
            country: "china",
            province,
            city: city[0].label.substring(0, city[0].label.length - 1)
          });
          let allCityLin = await api.getLine({
            date: this.getDay(-1, "-"),
            type: "accumulated",
            country: "china",
            province,
            city: city[0].label.substring(0, city[0].label.length - 1)
          });
          this.drawWorldLine("citychart1", "市累计", allCityLin, [
            "累计确诊",
            "累计治愈",
            "累计死亡"
          ]);
          this.drawWorldLine("citychart2", "市单日", somCityLin, [
            "单日新增确诊",
            "单日新增治愈",
            "单日新增死亡"
          ]);
        } else {
          this.provinceChart = true;
          this.cityChart = false;
          let somProLin = await api.getLine({
            date: this.getDay(-1, "-"),
            type: "someday",
            country: "china",
            province
          });
          let allProLin = await api.getLine({
            date: this.getDay(-1, "-"),
            type: "accumulated",
            country: "china",
            province
          });
          this.drawWorldLine("prochart1", "省累计", allProLin, [
            "累计确诊",
            "累计治愈",
            "累计死亡"
          ]);
          this.drawWorldLine("prochart2", "省单日", somProLin, [
            "单日新增确诊",
            "单日新增治愈",
            "单日新增死亡"
          ]);
        }
      }
    },
    async login() {
      await api.login();
    },
    async upload() {
      let data = {
        data: [
          {
            date: {
              year: 2020,
              month: 5,
              day: 28
            },
            area: {
              country: "china",
              province: "guangdong",
              city: "guangzhou"
            },
            detail: {
              confirmed: 2000,
              death: 70,
              cured: 1930
            }
          }
        ]
      };
      let res = await api.postData(data);
      console.log({ res });
    },
    async download() {
      let date = this.getDay(-1, "-");
      let data = {
        date,
        area: {},
        data_type: ["confirmed"],
        level: true
      };
      let res = await api.download(data);
      this.file = res;
      const link = document.createElement("a");
      link.href = encodeURI(res);
      link.download = "fileName.csv";
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    },
    drawChina(id, seriesName, name, data) {
      let chart = this.$echarts.init(this.$refs.chart3);
      chart.setOption({
        title: {
          text: seriesName, // 主标题文本，支持使用 \n 换行
          top: 20, // 定位 值: 'top', 'middle', 'bottom' 也可以是具体的值或者百分比
          left: "center", // 值: 'left', 'center', 'right' 同上
          textStyle: {
            // 文本样式
            fontSize: 25,
            fontWeight: 700,
            color: "#000000"
          }
        },
        visualMap: {
          type: "continuous", // continuous 类型为连续型  piecewise 类型为分段型
          show: true, // 是否显示 visualMap-continuous 组件 如果设置为 false，不会显示，但是数据映射的功能还存在
          min: 0,
          max: 2000,
          // 文本样式
          textStyle: {
            fontSize: 14,
            color: "#000"
          },
          realtime: false, // 拖拽时，是否实时更新
          calculable: true, // 是否显示拖拽用的手柄
          inRange: {
            color: ["#ffffff", "#E80505"] // 图元的颜色
          },
          dimension: 0
        },
        tooltip: {
          backgroundColor: "#ff7f50", //提示标签背景颜色
          textStyle: { color: "#fff" }, //提示标签字体颜色
          formatter: function(val) {
            if (val.data !== undefined) {
              return (
                val.data.name +
                "<br/>确诊人数: " +
                val.data.value[0] +
                "<br/>治愈人数:" +
                val.data.value[1] +
                "<br/>死亡人数:" +
                val.data.value[2]
              );
            } else {
              return val.name + ":no attainable data";
            }
          }
        },
        series: [
          {
            type: "map",
            mapType: "china",
            label: {
              normal: {
                show: true, //显示省份标签
                textStyle: { color: "#c71585" } //省份标签字体颜色
              },
              emphasis: {
                //对应的鼠标悬浮效果
                show: true,
                textStyle: { color: "#800080" }
              }
            },
            itemStyle: {
              normal: {
                borderWidth: 0.5, //区域边框宽度
                borderColor: "#009fe8", //区域边框颜色
                areaColor: "#ffefd5" //区域颜色
              },
              emphasis: {
                borderWidth: 0.5,
                borderColor: "#4b0082",
                areaColor: "#ffdead"
              }
            },
            nameMap: name,
            data: data
          }
        ]
      });
    },
    drawChart(id, name, data, seriesName) {
      let chart = this.$echarts.init(document.getElementById(id));
      window.addEventListener("resize", function() {
        chart.resize();
      });
      chart.setOption({
        title: {
          text: seriesName, // 主标题文本，支持使用 \n 换行
          top: 20, // 定位 值: 'top', 'middle', 'bottom' 也可以是具体的值或者百分比
          left: "center", // 值: 'left', 'center', 'right' 同上
          textStyle: {
            // 文本样式
            fontSize: 25,
            fontWeight: 700,
            color: "#000000"
          }
        },
        tooltip: {
          trigger: "item", // 触发类型, 数据项图形触发，主要在散点图，饼图等无类目轴的图表中使用
          // 提示框浮层内容格式器，支持字符串模板和回调函数两种形式
          // 使用函数模板  传入的数据值 -> value: number | Array
          formatter: function(val) {
            if (val.data !== undefined) {
              return (
                val.data.name +
                "<br/>确诊人数: " +
                val.data.value[0] +
                "<br/>治愈人数:" +
                val.data.value[1] +
                "<br/>死亡人数:" +
                val.data.value[2]
              );
            } else {
              return val.name + ":no attainable data";
            }
          }
        },
        // 视觉映射组件
        visualMap: {
          type: "continuous", // continuous 类型为连续型  piecewise 类型为分段型
          show: true, // 是否显示 visualMap-continuous 组件 如果设置为 false，不会显示，但是数据映射的功能还存在
          min: 0,
          max: 500000,
          // 文本样式
          textStyle: {
            fontSize: 14,
            color: "#000"
          },
          realtime: false, // 拖拽时，是否实时更新
          calculable: true, // 是否显示拖拽用的手柄
          inRange: {
            color: ["#ffffff", "#E80505"] // 图元的颜色
          },
          dimension: 0
        },
        series: [
          {
            type: "map", // 类型
            // 系列名称，用于tooltip的显示，legend 的图例筛选 在 setOption 更新数据和配置项时用于指定对应的系列
            name: seriesName,
            mapType: "world", // 地图类型
            // 是否开启鼠标缩放和平移漫游 默认不开启 如果只想要开启缩放或者平移，可以设置成 'scale' 或者 'move' 设置成 true 为都开启
            roam: true,
            // 图形上的文本标签
            label: {
              show: false // 是否显示对应地名
            },
            // 地图区域的多边形 图形样式
            itemStyle: {
              areaColor: "#7B68EE", // 地图区域的颜色 如果设置了visualMap，areaColor属性将不起作用
              borderWidth: 0.5, // 描边线宽 为 0 时无描边
              borderColor: "#000", // 图形的描边颜色 支持的颜色格式同 color，不支持回调函数
              borderType: "solid" // 描边类型，默认为实线，支持 'solid', 'dashed', 'dotted'
            },
            // 高亮状态下的多边形和标签样式
            emphasis: {
              label: {
                show: true, // 是否显示标签
                color: "auto" // 文字的颜色 如果设置为 'auto'，则为视觉映射得到的颜色，如系列色
              },
              itemStyle: {
                areaColor: "#FF6347" // 地图区域的颜色
              }
            },
            nameMap: name,
            data: data
          }
        ]
      });
    },
    drawWorldLine(id, seriesName, data, legendData) {
      let chart = this.$echarts.init(document.getElementById(id));
      chart.setOption({
        title: {
          text: seriesName
        },
        tooltip: {
          trigger: "axis"
        },
        legend: {
          data: legendData
        },
        grid: {
          left: "3%",
          right: "4%",
          bottom: "3%",
          containLabel: true
        },
        toolbox: {
          feature: {
            saveAsImage: {}
          }
        },
        xAxis: {
          type: "category",
          boundaryGap: false,
          data: data.date
        },
        yAxis: {
          type: "value"
        },
        series: [
          {
            name: legendData[0],
            type: "line",
            data: data.detail[0]
          },
          {
            name: legendData[1],
            type: "line",
            data: data.detail[1]
          },
          {
            name: legendData[2],
            type: "line",
            data: data.detail[2]
          }
        ]
      });
    },
    drawWorldBar(id, seriesName, data, legendData) {
      let chart = this.$echarts.init(document.getElementById(id));
      chart.setOption({
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "shadow",
            label: {
              show: true
            }
          }
        },
        toolbox: {
          show: true,
          feature: {
            mark: { show: true },
            dataView: { show: true, readOnly: false },
            magicType: { show: true, type: ["line", "bar"] },
            restore: { show: true },
            saveAsImage: { show: true }
          }
        },
        calculable: true,
        legend: {
          data: legendData,
          itemGap: 5
        },
        grid: {
          top: "12%",
          left: "1%",
          right: "10%",
          containLabel: true
        },
        xAxis: [
          {
            type: "category",
            data: data.varying
          }
        ],
        yAxis: [
          {
            type: "value",
            name: seriesName,
            axisLabel: {
              formatter: a => {
                a = +a;
                return isFinite(a)
                  ? this.$echarts.format.addCommas(+a / 1000)
                  : "";
              }
            }
          }
        ],
        dataZoom: [
          {
            show: true,
            start: 94,
            end: 100
          },
          {
            type: "inside",
            start: 94,
            end: 100
          },
          {
            show: true,
            yAxisIndex: 0,
            filterMode: "empty",
            width: 30,
            height: "80%",
            showDataShadow: false,
            left: "93%"
          }
        ],
        series: [
          {
            name: legendData[0],
            type: "bar",
            data: data.detail[0]
          },
          {
            name: legendData[1],
            type: "bar",
            data: data.detail[1]
          },
          {
            name: legendData[2],
            type: "bar",
            data: data.detail[2]
          }
        ]
      });
    },
    getDay(num, str) {
      let today = new Date();
      let nowTime = today.getTime();
      let ms = 24 * 3600 * 1000 * num;
      today.setTime(parseInt(nowTime + ms));
      let oYear = today.getFullYear();
      let oMoth = (today.getMonth() + 1).toString();
      if (oMoth.length <= 1) oMoth = "0" + oMoth;
      let oDay = today.getDate().toString();
      if (oDay.length <= 1) oDay = "0" + oDay;
      return oYear + str + oMoth + str + oDay;
    }
  },
  components: {
    inputBox
  }
};
</script>

<style scoped>
.container {
  width: 100%;
  height: 100%;
}
.el-carousel__button {
  background-color: grey !important;
}

.chart {
  width: 100%;
  height: 95%;
  background-size: 100% 100%;
}
.sub-menu {
  height: 500px;
  overflow: scroll;
}
</style>