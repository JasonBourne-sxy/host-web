<template>
  <el-container style="height: 100%; border: 1px solid #eee">
    <el-container>
      <el-header style="text-align: left; font-size: 12px">
        <label>系统名称：</label>
        <el-input placeholder="" v-model="sysName" style="width: 150px"></el-input>
        <label>描述：</label>
        <el-input placeholder="" v-model="description" style="width: 150px"></el-input>
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
            label="PORT"
            min-width="6%">
          </el-table-column>
          <el-table-column
            prop="type"
            label="监控类型"
            min-width="6%">
          </el-table-column>
          <el-table-column
            prop="interval"
            label="检测间隔(s)"
            min-width="6%">
          </el-table-column>
          <el-table-column
            prop="is_use"
            label="是否启用"
            min-width="6%">
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
                sys_idOptions: [],
                sys_id: '',
                is_use: '',
                description: ''
            }
        },
        created() {
            this.get_sys_id_data();
        },
        methods: {
            getTableList(sysId, check_type) {
                spuApi.getTableDetails(sysId, check_type).then(res => {
                    this.tableData = res.data;
                })
            },
            deleteRow(index, rows, row) {
                this.$confirm('是否确认删除?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    let params = {id: row.id};
                    spuApi.deleteInstance(params).then(_ => {
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
                this.form.ip = data.ip;
                this.form.port = data.port;
                this.form.type = data.type;
                this.form.interval = data.interval;
                this.form.sys_id = data.sys_id;
                this.form.is_use = data.is_use;
                this.form.description = data.description;
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
                this.form.id = '';
                this.form.ip = '';
                this.form.port = '';
                this.form.type = '';
                this.form.is_use = '';
                this.form.interval = '';
                this.form.sys_id = '';
                this.form.description = '';
                this.dialogFormVisible = true;
            },
            search() {
                this.loading = true;
                let params = {
                    ip: this.ip, sys_name: this.sysName, check_type: this.checkType
                    , description: this.description
                };
                spuApi.getMonitorOperateDetails(params).then(res => {
                    this.tableData = res.data;
                    this.loading = false;
                })
            },
            handleSubmit() {
                this.dialogFormVisible = false;
                let params = {
                    id: this.form.id,
                    ip: this.form.ip,
                    port: this.form.port,
                    type: this.form.type,
                    sys_id: this.form.sys_id,
                    is_use: this.form.is_use,
                    interval: this.form.interval,
                    delivery: this.form.delivery,
                    description: this.form.description,
                };
                spuApi.insertOrUpdateInstance(params).then(res => {
                    this.search();
                })
            },
            get_sys_id_data() {
                spuApi.query_sys_info({id: ""}).then(res => {
                    console.log(res);
                    this.sys_idOptions = res.data
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
