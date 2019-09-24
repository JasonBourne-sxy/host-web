<template>
  <el-container style="height: 520px; border: 1px solid #eee">
    <el-aside width="200px" style="background-color: rgb(238, 241, 246)">
      <el-tree style="background-color: rgb(238, 241, 246)" :data="treeData" :props="defaultProps"
               @node-click="handleNodeClick"></el-tree>
    </el-aside>

    <el-container>
      <el-header style="text-align: left; font-size: 12px">
        <label>时间：</label>
        <el-date-picker
          v-model="dateValue"
          type="datetimerange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期">
        </el-date-picker>
        <label>系统名称：</label>
        <el-input placeholder="" v-model="sysName" style="width: 150px"></el-input>
        <label>IP：</label>
        <el-input placeholder="" v-model="ip" style="width: 150px"></el-input>
        <el-button type="primary" icon="el-icon-search" @click="search">查询</el-button>
        <el-button type="primary" icon="el-icon-refresh" @click="refresh">重置</el-button>
      </el-header>
      <el-header style="text-align: left; font-size: 12px">
        <el-button type="primary" icon="el-icon-search" @click="add">新增</el-button>
      </el-header>

      <el-main>
        <el-table
          :data="tableData"
          style="width: 100%;height: 100%;"
        >
          <el-table-column
            prop="check_result"
            label="状态"
            width="150">
          </el-table-column>
          <el-table-column
            prop="check_time"
            label="时间"
            width="150">
          </el-table-column>
          <el-table-column
            prop="interval"
            label="间隔"
            width="120">
          </el-table-column>
          <el-table-column
            prop="ip"
            label="ip"
            width="120">
          </el-table-column>
          <el-table-column
            prop="sys_name"
            label="系统名称"
            width="150">
          </el-table-column>
          <el-table-column
            prop="type"
            label="类型"
            width="120">
          </el-table-column>
          <el-table-column
            fixed="right"
            label="操作"
            width="150">
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
          <div class="block">
            <el-pagination
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
              :current-page="currentPage"
              :page-sizes="[10, 20, 50, 100]"
              :page-size="100"
              layout="total, sizes, prev, pager, next, jumper"
              :total="400">
            </el-pagination>
          </div>
        </template>
        <template>
          <el-dialog title="新增" :visible.sync="dialogFormVisible">
            <el-form ref="form" :model="form" label-width="80px">
              <el-form-item label="IP">
                <el-input v-model="form.ip"></el-input>
              </el-form-item>
              <el-form-item label="端口">
                <el-input v-model="form.port"></el-input>
              </el-form-item>
              <el-form-item label="类型">
                <el-select v-model="form.type" placeholder="请选择类型">
                  <el-option label="ping" value="ping"></el-option>
                  <el-option label="tcp" value="tcp"></el-option>
                  <el-option label="tcp" value="半连接"></el-option>
                  <el-option label="tcp" value="自定义"></el-option>
                </el-select>
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
            getTableList(sysId, check_type) {
                spuApi.getTableDetails(sysId,check_type).then(res => {
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


  .el-aside {
    color: #7495ed;
  }
</style>
