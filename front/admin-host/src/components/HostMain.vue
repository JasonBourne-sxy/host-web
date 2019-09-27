<template>
  <el-container style="height: 100%; border: 1px solid #eee">
    <el-aside width="200px" style="background-color: rgb(238, 241, 246)">
      <el-tree style="background-color: rgb(238, 241, 246)" :data="treeData" :props="defaultProps"
               @node-click="handleNodeClick"></el-tree>
    </el-aside>
    <el-main>
      <el-table
        :data="tableData"
        height="98%"
        v-loading="loading"
        style="width: 100%;"
      >
        <el-table-column
          prop="ip"
          label="IP"
          min-width="10%" align="center">
        </el-table-column>
        <el-table-column
          prop="port"
          label="port"
          min-width="8%" align="center">
        </el-table-column>
        <el-table-column
          prop="type"
          label="类型"
          min-width="8%"  align="center">
        </el-table-column>
        <el-table-column
          prop="check_result"
          label="状态"
          min-width="8%"  align="center">
        </el-table-column>
        <el-table-column
          prop="space_time"
          label="响应时间(ms)"
          min-width="10%"  align="center">
        </el-table-column>
        <el-table-column
          prop="start_time"
          label="检测时间"
          min-width="15%"  align="center">
        </el-table-column>
        <el-table-column
          prop="interval"
          label="检测间隔(s)"
          min-width="10%"  align="center">
        </el-table-column>

        <el-table-column
          prop="sys_name"
          label="系统名称"
          min-width="10%"  align="center">
        </el-table-column>
        <el-table-column
          prop="description"
          label="描述"
          min-width="20%"  align="center">
        </el-table-column>
      </el-table>

    </el-main>
  </el-container>
</template>

<script>
    import spuApi from '../api/spu.api'

    export default {
        data() {
            return {
                loading:false,
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
                    ip: '',
                    port: '',
                    type: '',
                    timeNum: '',
                    delivery: false,
                    describe: ''
                },
                formLabelWidth: '120px',
                ip: '',
                sysName: ''
            }
        },
        created() {
            this.getTreeInfo();
        },
        methods: {
            getTreeInfo() {
                spuApi.getTreeData().then(res => {
                    this.treeData = res.data.results.data;
                });
            },
            getTableList(sysId,check_type) {
                this.loading = true;
                spuApi.getTableDetails(sysId,check_type).then(res => {
                    this.tableData = res.data;
                    this.loading = false;
                })
            },
            handleNodeClick(data) {
                this.getTableList(data.id,data.type);
            },
            deleteRow(index, rows) {
                rows.splice(index, 1);
            },
            editorRow(index, rows) {
                let data = rows[0];
                this.form.ip = data.ip;
                this.form.port = '';
                this.form.type = data.type;
                this.form.timeNum = data.interval;
                this.form.describe = data.description;
                this.dialogFormVisible = true;
                console.log(this.form);
            },
            handleSizeChange(val) {
                console.log(`每页 ${val} 条`);
            },
            handleCurrentChange(val) {
                console.log(`当前页: ${val}`);
            },
            add() {
                this.form.ip = '';
                this.form.port = '';
                this.form.type = '';
                this.form.timeNum = '';
                this.form.describe = '';
                this.dialogFormVisible = true;
            },
            search() {

            },
            refresh() {
                this.sysName = '';
                this.ip = '';
                this.dateValue = [new Date(), new Date()]
            }
        }
    };
</script>

<style>
  .el-main {
    padding-top: 0;
  }
  .el-table{
    overflow: auto;
  }
  .el-aside {
    color: #7495ed;
  }
</style>
