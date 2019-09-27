<template>
  <el-container style="height: 100%; border: 1px solid #eee">
    <el-container>
      <el-header style="text-align: left; font-size: 12px">
        <label>系统名称：</label>
        <el-input placeholder="" v-model="sysName" style="width: 150px"></el-input>
        <label>管理员：</label>
        <el-input placeholder="" v-model="name" style="width: 150px"></el-input>
        <el-button type="primary" icon="el-icon-search" @click="search">查询</el-button>
        <el-button type="primary" icon="el-icon-refresh" @click="refresh">重置</el-button>
        <el-button type="primary" icon="el-icon-search" @click="add">新增</el-button>
      </el-header>
      <el-main>
        <el-table
          :data="tableData"
          style="width: 100%;height: 98%;">
          <el-table-column
            prop="name"
            label="系统名称"
            min-width="23%">
          </el-table-column>
          <el-table-column
            prop="manager"
            label="管理员"
            min-width="20%">
          </el-table-column>
          <el-table-column
            prop="telephone"
            label="联系电话"
            min-width="30%">
          </el-table-column>
          <el-table-column
            prop="job_number"
            label="工号"
            min-width="13%">
          </el-table-column>
          <el-table-column
            fixed="right"
            label="操作"
            min-width="13%">
            <template slot-scope="scope">
              <el-button
                @click.native.prevent="editorRow(scope.$index, tableData)"
                type="text"
                icon="el-icon-edit"
                size="small">
                编辑
              </el-button>
              <el-button
                @click.native.prevent="deleteRow(scope.$index, tableData)"
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
              <el-form-item label="IP">
                <el-input v-model="form.ip"></el-input>
              </el-form-item>
              <el-form-item label="端口">
                <el-input v-model="form.port"></el-input>
              </el-form-item>
              <el-form-item label="间隔">
                <el-input v-model="form.timeNum"></el-input>
              </el-form-item>
              <el-form-item label="描述">
                <el-input type="textarea" v-model="form.describe"></el-input>
              </el-form-item>

            </el-form>
            <div slot="footer" class="dialog-footer">
              <el-button @click="dialogFormVisible = false">取 消</el-button>
              <el-button type="primary" @click="dialogFormVisible = false">确 定</el-button>
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
                    sys_name: '',
                    name: '',
                    telephone: '',
                    job_number: '',
                    delivery: false,
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
            getTableList(sysId, check_type) {
                spuApi.getTableDetails(sysId, check_type).then(res => {
                    this.tableData = res.data;
                })
            },
            handleNodeClick(data) {
                this.getTableList(data.id, data.type);
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
                this.loading = true;
                let params = {ip: this.ip, sys_name: this.sysName, check_type: this.checkType};
                spuApi.query_sys_info(params).then(res => {
                    this.tableData = res.data;
                    this.loading = false;
                })
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
    padding: 0;
  }

  .el-table {
    overflow: auto;
  }

  .el-aside {
    color: #7495ed;
  }
</style>
