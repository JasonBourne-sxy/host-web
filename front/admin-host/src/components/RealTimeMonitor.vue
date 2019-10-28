<template>
  <el-container style="height: 100%; border: 1px solid #eee">
    <el-container>
      <el-header style="text-align: left; font-size: 12px">
        <label>系统名称：</label>
        <el-input placeholder="" v-model="sysName" style="width: 150px"></el-input>
        <label>IP：</label>
        <el-input placeholder="" v-model="ip" style="width: 150px"></el-input>
        <label>检测类型：</label>
        <el-select v-model="checkType" style="width: 120px" placeholder="请选择">
          <el-option
            v-for="item in checkOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value">
          </el-option>
        </el-select>
        <label>检测结果：</label>
        <el-select v-model="check_result" style="width: 120px" placeholder="请选择类型">
          <el-option label="正常" value="True"></el-option>
          <el-option label="异常" value="False"></el-option>
        </el-select>
        <el-button type="primary" icon="el-icon-search" @click="search">查询</el-button>
        <el-button type="primary" icon="el-icon-refresh" @click="refresh">重置</el-button>
      </el-header>
      <el-main>
        <el-table
          :data="tableData"
          v-loading="loading"
          height="98%"
          style="width: 100%;"
        >
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
            prop="type"
            label="监控类型"
            min-width="6%">
          </el-table-column>
          <el-table-column
            prop="check_result"
            label="检测结果"
            min-width="6%">
          </el-table-column>
          <el-table-column
            prop="response_time"
            label="响应时间(ms)"
            min-width="8%">
          </el-table-column>
          <el-table-column
            prop="interval"
            label="检测间隔(s)"
            min-width="8%">
          </el-table-column>
          <el-table-column
            prop="start_time"
            label="检查时间"
            min-width="10%">
          </el-table-column>
          <el-table-column
            fixed="right"
            label="操作"
            width="150">
            <template slot-scope="scope">
              <el-button
                @click.native.prevent="searchHistory(scope.$index, scope.row)"
                type="text"
                icon="el-icon-search"
                size="small">
                历史状态
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        <template>
          <el-dialog title="新增" :visible.sync="dialogFormVisible">
            <el-form ref="form" :model="form" label-width="80px">
              <el-form-item label="系统名称">
                <el-select v-model="form.sys_id" placeholder="请系统名称">
                  <el-option
                    v-for="item in sys_idOptions"
                    :key="item.id"
                    :label="item.name"
                    :value="item.id">
                  </el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="描述">
                <el-input type="textarea" v-model="form.description"></el-input>
              </el-form-item>
              <el-form-item label="IP">
                <el-input v-model="form.ip"></el-input>
              </el-form-item>
              <el-form-item label="端口">
                <el-input v-model="form.port"></el-input>
              </el-form-item>
              <el-form-item label="类型">
                <el-select v-model="form.type" placeholder="请选择类型">
                  <el-option label="ping" value="ping"></el-option>
                  <el-option label="半连接" value="半连接"></el-option>
                  <el-option label="自定义" value="自定义"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="是否启用">
                <el-select v-model="form.is_use" placeholder="请选择类型">
                  <el-option label="是" value="1"></el-option>
                  <el-option label="否" value="0"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="间隔">
                <el-input v-model="form.interval"></el-input>
              </el-form-item>


            </el-form>
          </el-dialog>
        </template>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
    import spuApi from '../api/spu.api'
    import HostHistory from "./HostHistory"

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
                    value: '半连接',
                    label: '半连接'
                }, {
                    value: '自定义',
                    label: '自定义'
                }],
                check_result: '',
                sys_idOptions: [],
                sys_id: '',
                is_use: ''
            }
        },
        methods: {
            getTableList(sysId, check_type) {
                spuApi.getTableDetails(sysId, check_type).then(res => {
                    this.tableData = res.data;
                })
            },
            search() {
                this.loading = true;
                let params = {
                    ip: this.ip, sys_name: this.sysName, check_type: this.checkType
                    , check_result: this.check_result
                };
                spuApi.get_real_time_monitor_result(params).then(res => {
                    this.tableData = res.data;
                    this.loading = false;
                })
            },
            refresh() {
                this.sysName = '';
                this.ip = '';
                this.dateValue = [new Date(), new Date()];
                this.checkType = '';
                this.check_result = '';
            },
            searchHistory(index,row){
                console.log(row);
                // this.$router.push({name: "HostHistory", params: row});
                let routerData = this.$router.resolve({
                    name: `HostHistory`,
                    params:row
                });
                window.open(routerData.href+'?ip='+row.ip+'&port='+row.port+'&check_type='+row.type, "_blank");
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
