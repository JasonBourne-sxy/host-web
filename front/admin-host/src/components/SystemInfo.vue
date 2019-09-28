<template>
  <el-container style="height: 100%; border: 1px solid #eee">
    <el-container>
      <el-header style="text-align: left; font-size: 12px">
        <label>系统名称：</label>
        <el-input placeholder="" v-model="name" style="width: 150px"></el-input>
        <label>管理员：</label>
        <el-input placeholder="" v-model="manager" style="width: 150px"></el-input>
        <el-button type="primary" icon="el-icon-search" @click="search">查询</el-button>
        <el-button type="primary" icon="el-icon-refresh" @click="refresh">重置</el-button>
        <el-button type="primary" icon="el-icon-search" @click="add">新增</el-button>
      </el-header>
      <el-main>
        <el-table
          :data="tableData"
          v-loading="loading"
          height="98%"
          style="width: 100%;"
        >
          <el-table-column
            prop="name"
            label="系统名称"
            min-width="30%">
          </el-table-column>
          <el-table-column
            prop="manager"
            label="管理员"
            min-width="20%">
          </el-table-column>
          <el-table-column
            prop="telephone"
            label="电话"
            min-width="20%">
          </el-table-column>
          <el-table-column
            prop="job_number"
            label="工号"
            min-width="20%">
          </el-table-column>
          <el-table-column
            fixed="right"
            label="操作"
            width="150">
            <template slot-scope="scope">
              <el-button
                @click.native.prevent="editorRow(scope.$index, scope.row)"
                type="text"
                icon="el-icon-edit"
                size="small">
                编辑
              </el-button>
              <el-button
                @click.native.prevent="deleteRow(scope.$index,tableData, scope.row)"
                type="text"
                icon="el-icon-delete"
                size="small">
                移除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        <template>
          <el-dialog title="新增" :visible.sync="dialogFormVisible">
            <el-form ref="form" :model="form" label-width="80px">
              <el-form-item label="系统名称">
                <el-input v-model="form.name"></el-input>
              </el-form-item>
              <el-form-item label="管理员">
                <el-input v-model="form.manager"></el-input>
              </el-form-item>
              <el-form-item label="电话">
                <el-input v-model="form.telephone"></el-input>
              </el-form-item>
              <el-form-item label="工号">
                <el-input v-model="form.job_number"></el-input>
              </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
              <el-button @click="dialogFormVisible = false">取 消</el-button>
              <el-button type="primary" @click="handleSubmit">确 定</el-button>
            </div>
          </el-dialog>
        </template>
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
                    name: '',
                    manager: '',
                    telephone: '',
                    job_number: '',
                    delivery: false,
                },
                formLabelWidth: '120px',
                ip: '',
                name: '',
                manager: '',
                checkOptions: [{
                    value: 'ping',
                    label: 'ping'
                }, {
                    value: 'TCP',
                    label: 'TCP'
                }, {
                    value: '半连接',
                    label: '半连接'
                }, {
                    value: '自定义',
                    label: '自定义'
                }],
                SysInfoOptions: [],
                sysInfo: ''
            }
        },
        created() {
            // this.getTreeInfo();
            this.getSysInfoData();
        },
        methods: {
            deleteRow(index, rows, row) {
                this.$confirm('是否确认删除?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    let params = {id: row.id};
                    spuApi.deleteInstance(params).then(res => {
                        rows.splice(index, 1);
                        this.$message({
                            type: 'success',
                            message: '删除成功!'
                        });
                    })
                }).catch(() => {
                    this.$message({
                        type: 'info',
                        message: '已取消删除'
                    });
                });
            },
            editorRow(index, row) {
                let data = row;
                this.form.id = data.id;
                this.form.name = data.name;
                this.form.manager = data.manager;
                this.form.telephone = data.telephone;
                this.form.job_number = data.job_number;
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
                this.form.id = "";
                this.form.name = "";
                this.form.manager = "";
                this.form.telephone = "";
                this.form.job_number = "";
                this.dialogFormVisible = true;
            },
            search() {
                this.loading = true;
                let params = {name: this.name, manager: this.manager};
                spuApi.query_sys_info(params).then(res => {
                    this.tableData = res.data;
                    this.loading = false;
                })
            },
            handleSubmit() {
                this.dialogFormVisible = false;
                let params = {
                    id: this.form.id,
                    name: this.form.name,
                    manager: this.form.manager,
                    telephone: this.form.telephone,
                    job_number: this.form.job_number,
                    timeNum: this.form.timeNum,
                    delivery: this.form.delivery,
                    describe: this.form.describe,
                };
                spuApi.insert_or_update_system_info(params).then(res=>{
                    this.search();
                });
            },
            getSysInfoData() {
                spuApi.query_sys_info({id: ""}).then(res => {
                    this.SysInfoOptions = res.data
                })
            },
            refresh() {
                this.name = '';
                this.manager = '';
                this.dateValue = [new Date(), new Date()];
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
