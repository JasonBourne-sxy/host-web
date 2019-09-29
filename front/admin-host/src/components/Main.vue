<template>
  <el-container style="height: 100%">
    <el-header>
      <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
        <el-menu-item index="1">实时监控</el-menu-item>
        <el-menu-item index="2">监控管理</el-menu-item>
        <el-menu-item index="3">系统信息</el-menu-item>
        <el-menu-item index="4">网络联通性监控</el-menu-item>
        <!--        <el-menu-item index="4">历史记录</el-menu-item>-->
      </el-menu>
    </el-header>
    <el-main>
      <real-time-monitor v-if="activeIndex === '1'"></real-time-monitor>
      <host-operate v-if="activeIndex === '2'"></host-operate>
      <system-info v-if="activeIndex === '3'"></system-info>
      <host-main v-if="activeIndex === '4'"></host-main>
      <!--      <hostrun-history v-if="activeIndex === '4'"></hostrun-history>-->

      <!--   <div id="myChart" style="width: 100%;height: 300px"></div>   -->
    </el-main>
  </el-container>
</template>

<script>
    import HostMain from "./HostMain";
    import HostHistory from "./HostHistory";
    import HostOperate from "./MonitorOperate";
    import SystemInfo from "./SystemInfo";
    import RealTimeMonitor from "./RealTimeMonitor";
    import $ from 'jquery'

    export default {
        name: 'Main',
        components: {HostMain, HostHistory, HostOperate, SystemInfo, RealTimeMonitor},
        data() {
            return {
                activeIndex: "1",
            }
        },
        methods: {
            handleSelect(key) {
                this.activeIndex = key;
                let my_chart_div = $('#myChart');
                my_chart_div.hide();
                if (key === '1') {
                    my_chart_div.hide();
                } else {
                    my_chart_div.show();
                }
            }
        }
    }
</script>
<style>
  .el-header {
    background-color: #B3C0D1;
    color: #333;
    text-align: center;
    line-height: 60px;
  }

  .el-main {
    background-color: #E9EEF3;
    color: #333;
    text-align: center;
  }


</style>
