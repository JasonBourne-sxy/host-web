<template>
  <el-container style="height: 520px; border: 1px solid #eee">
    <el-aside width="200px" style="background-color: rgb(238, 241, 246)">
        <el-tree style="background-color: rgb(238, 241, 246)" :data="treeData" :props="defaultProps" @node-click="handleNodeClick"></el-tree>
    </el-aside>

    <el-container>
      <el-header style="text-align: left; font-size: 12px">
        <el-button type="primary" icon="el-icon-search">新增</el-button>
<!--        <el-dropdown>-->
<!--          <i class="el-icon-setting" style="margin-right:5px"></i>-->
<!--          <el-dropdown-menu slot="dropdown">-->
<!--            <el-dropdown-item>查看</el-dropdown-item>-->
<!--            <el-dropdown-item>新增</el-dropdown-item>-->
<!--            <el-dropdown-item>删除</el-dropdown-item>-->
<!--          </el-dropdown-menu>-->
<!--        </el-dropdown>-->
<!--        <span>王小虎</span>-->
      </el-header>

      <el-main>
        <el-table
          :data="tableData"
          style="width: 100%"
          max-height="250">
          <el-table-column
            prop="date"
            label="日期"
            width="150">
          </el-table-column>
          <el-table-column
            prop="name"
            label="姓名"
            width="120">
          </el-table-column>
          <el-table-column
            prop="province"
            label="省份"
            width="120">
          </el-table-column>
          <el-table-column
            prop="city"
            label="市区"
            width="120">
          </el-table-column>
          <el-table-column
            prop="address"
            label="地址"
            width="300">
          </el-table-column>
          <el-table-column
            prop="zip"
            label="邮编"
            width="120">
          </el-table-column>
          <el-table-column
            fixed="right"
            label="操作"
            width="150">
            <template slot-scope="scope">
              <el-button
                @click.native.prevent="deleteRow(scope.$index, tableData)"
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
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
    export default {
        data() {
            return {
                treeData: [{
                    label: '一级 1',
                    children: [{
                        label: '二级 1-1',
                        children: [{
                            label: '三级 1-1-1'
                        }]
                    }]
                }, {
                    label: '一级 2',
                    children: [{
                        label: '二级 2-1',
                        children: [{
                            label: '三级 2-1-1'
                        }]
                    }, {
                        label: '二级 2-2',
                        children: [{
                            label: '三级 2-2-1'
                        }]
                    }]
                }, {
                    label: '一级 3',
                    children: [{
                        label: '二级 3-1',
                        children: [{
                            label: '三级 3-1-1'
                        }]
                    }, {
                        label: '二级 3-2',
                        children: [{
                            label: '三级 3-2-1'
                        }]
                    }]
                }],
                tableData:[{
                        date: '2016-05-03',
                        name: '王小虎',
                        province: '上海',
                        city: '普陀区',
                        address: '上海市普陀区金沙江路 1518 弄',
                        zip: 200333
                    }, {
                        date: '2016-05-02',
                        name: '王小虎',
                        province: '上海',
                        city: '普陀区',
                        address: '上海市普陀区金沙江路 1518 弄',
                        zip: 200333
                    }],
                defaultProps: {
                    children: 'children',
                    label: 'label'
                },
                currentPage: 4
            }
        },
        methods: {
            handleNodeClick(data) {
                console.log(data);
            },
            deleteRow(index, rows) {
                rows.splice(index, 1);
            },
            handleSizeChange(val) {
                console.log(`每页 ${val} 条`);
            },
            handleCurrentChange(val) {
                console.log(`当前页: ${val}`);
            }
        }
    };
</script>

<style>


  .el-aside {
    color: #7495ed;
  }
</style>
