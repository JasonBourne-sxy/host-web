<template>
  <el-container style="height: 100%; border: 1px solid #eee">
    <el-container>
      <el-header style="text-align: left; font-size: 12px">
        <label>系统名称：</label>
        <el-input placeholder="" v-model="sysName" style="width: 150px"></el-input>
        <label>IP：</label>
        <el-input placeholder="" v-model="ip" style="width: 150px"></el-input>
        <label>检测类型：</label>
        <el-select v-model="checkType" placeholder="请选择">
          <el-option
            v-for="item in checkOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value">
          </el-option>
        </el-select>
        <el-button type="primary" icon="el-icon-search" @click="search">查询</el-button>
        <el-button type="primary" icon="el-icon-refresh" @click="refresh">重置</el-button>
      </el-header>
      <el-main>
        <el-table
          :data="tableData"
          v-loading="loading"
          height="98%"
          style="width: 100%;">
          <el-table-column
            prop="sys_name"
            label="系统名称"
            min-width="10%">
          </el-table-column>
          <el-table-column
            prop="description"
            label="监控描述"
            min-width="20%">
          </el-table-column>
          <el-table-column
            prop="ip"
            label="IP"
            min-width="10%">
          </el-table-column>
          <el-table-column
            prop="port"
            label="端口"
            min-width="6%">
          </el-table-column>
          <el-table-column
            prop="check_type"
            label="监控类型"
            min-width="6%">
          </el-table-column>
          <el-table-column
            prop="check_time"
            label="报警时间"
            min-width="10%">
          </el-table-column>
          <el-table-column
            prop="warning_type"
            label="报警类型"
            min-width="8%">
          </el-table-column>
          <el-table-column
            prop="comment"
            label="备注"
            min-width="10%">
          </el-table-column>
        </el-table>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
    import spuApi from '../api/spu.api'

    export default {
        data() {
            return {
                loading: false,
                treeData: [],
                tableData: [],
                dateValue: [new Date(), new Date()],
                defaultProps: {
                    children: 'children',
                    label: 'name'
                },
                currentPage: 4,
                dialogFormVisible: false,
                form: {
                    id: '',
                    ip: '',
                    port: '',
                    type: '',
                    interval: '',
                    sys_id: '',
                    is_use: '',
                    delivery: false,
                    description: ''
                },
                formLabelWidth: '120px',
                ip: '',
                sysName: '',
                checkType: '',
                checkOptions: [{
                    value: 'ping',
                    label: 'ping'
                }, {
                    value: 'half_connection',
                    label: '半连接'
                }, {
                    value: '自定义',
                    label: '自定义'
                }],
                sys_idOptions: [],
                sys_id: '',
                is_use: ''
            }
        },
        methods: {
            search() {
                this.loading = true;
                let params = {
                    ip: this.ip, sys_name: this.sysName,
                    check_type: this.checkType
                };
                spuApi.get_warning_history(params).then(res => {
                    this.tableData = res.data;
                    this.loading = false;
                })
            },

            refresh() {
                this.sysName = '';
                this.ip = '';
                this.dateValue = [new Date(), new Date()];
                this.checkType = '';
            }
        }
    };
</script>

<style>
  .el-main {
    padding: 0;
  }

  .el-table {
    overflow: auto;
  }

  .el-aside {
    color: #7495ed;
  }
</style>
