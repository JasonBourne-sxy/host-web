<template>
  <el-container>
    <el-container>
      <el-header>
        <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
          <el-menu-item index="1">host列表</el-menu-item>
          <el-menu-item index="2">历史记录</el-menu-item>
        </el-menu>
      </el-header>
      <el-main>
        <host-main v-if="activeIndex == '1'"></host-main>
        <host-history v-if="activeIndex == '2'"></host-history>
        <div id="myChart"style="width: 100%;height: 300px"></div>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
    import HostMain from "./HostMain";
    import HostHistory from "./HostHistory";
    import $ from 'jquery'
    export default {
        name: 'Main',
        components:{HostMain,HostHistory},
        data() {
            return {
                activeIndex: "1",
            }
        },
        methods: {
            handleSelect(key) {
                this.activeIndex = key;
                if(key == '1'){
                    $('#myChart').hide();
                }else{
                    $('#myChart').show();
                }
            }
        }
    }
</script>

<style>
  .el-header{
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
