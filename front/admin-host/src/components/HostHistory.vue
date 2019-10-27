<template>
  <el-container style="height: 100%; border: 1px solid #eee">
    <el-container>
      <el-header style="text-align: left; font-size: 12px">
        <label>日期：</label>
        <el-date-picker
          v-model="dataValue"
          type="datetimerange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期">
        </el-date-picker>
        <el-button type="primary" icon="el-icon-search" @click="search">查询</el-button>
        <el-button type="primary" icon="el-icon-refresh" @click="refresh">重置</el-button>
        <el-button type="primary" icon="el-icon-back" @click="goBack">返回</el-button>

      </el-header>
      <el-main>
        <div id="myChart" style="width: 98%;height: 300px"></div>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>

    import spuApi from '../api/spu.api'


    export default {
        name: "HostHistory",
        data() {
            return {
                echarts: {},
                myCharts: {},
                option: {
                    title: {
                        text: '历史记录',
                        subtext: ''
                    },
                    tooltip: {
                        trigger: 'axis'
                    },
                    legend: {
                        data: ['最高气温']
                    },
                    toolbox: {
                        show: true,
                        feature: {
                            mark: {show: true},
                            dataView: {show: true, readOnly: false},
                            magicType: {show: true, type: ['line', 'bar']},
                            restore: {show: true},
                            saveAsImage: {show: true}
                        }
                    },
                    calculable: true,
                    xAxis: [
                        {
                            type: 'category',
                            boundaryGap: false,
                            data: []
                        }
                    ],
                    yAxis: [
                        {
                            type: 'value',
                            minInterval: 1,
                            axisLabel: {
                                formatter: '{value} '
                            }
                        }
                    ],
                    series: [
                        {
                            name: '状态',
                            type: 'line',
                            data: [],
                            markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                            },

                        },

                    ]
                },
                dataValue: [new Date(), new Date()],
                params: {}
            }
        },
        created() {
            this.params = this.$route.params
            console.log(this.params);
        },
        methods: {
            initEcharts() {
                this.echarts = require('echarts');
                this.myCharts = this.echarts.init(document.getElementById("myChart"));
                this.myCharts.setOption(this.option);
            },
            search() {
                this.loading = true;
                let dataTime = this.dataValue;
                let params = {
                    ip: this.params.ip,
                    port: this.params.port,
                    check_type: this.params.type,
                    start_time: dataTime[0],
                    end_time: dataTime[1]
                };
                spuApi.get_monitor_history(params).then(res => {
                    this.loading = false;
                    console.log(res.data);
                    var query_result = res.data;
                    var grap_data = {
                        title: {
                            text: '历史记录',
                            subtext: ''
                        },
                        tooltip: {
                            trigger: 'axis'
                        },
                        legend: {
                            data: ['最高气温']
                        },
                        toolbox: {
                            show: true,
                            feature: {
                                mark: {show: true},
                                dataView: {show: true, readOnly: false},
                                magicType: {show: true, type: ['line', 'bar']},
                                restore: {show: true},
                                saveAsImage: {show: true}
                            }
                        },
                        calculable: true,
                        xAxis: [
                            {
                                type: 'category',
                                boundaryGap: false,
                                data: ['10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00']
                            }
                        ],
                        yAxis: [
                            {
                                type: 'value',
                                minInterval: 1,
                                axisLabel: {
                                    formatter: '{value} '
                                }
                            }
                        ],
                        series: [
                            {
                                name: '状态',
                                type: 'line',
                                data: [0, 1, 0, 1, 1, 0, 1],
                                markPoint: {
                                    data: [
                                        {type: 'max', name: '最大值'},
                                        {type: 'min', name: '最小值'}
                                    ]
                                },

                            },

                        ]
                    };
                    grap_data.xAxis = [
                        {
                            type: 'category',
                            boundaryGap: false,
                            data: query_result[0]
                        }
                    ];
                    grap_data.series = [
                        {
                            name: '状态',
                            type: 'line',
                            data: query_result[1],
                            markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                            },

                        },

                    ];
                    this.myCharts.setOption(grap_data);
                });
                this.initEcharts();
            },
            refresh() {
                this.dataValue = [new Date(), new Date()];
            },
            goBack() {
                this.$router.push({name: "RealTimeMonitor"});
            }
        }

    }
</script>

<style scoped>

</style>
