<template>
</template>

<script>

    export default {
        name: "HostHistory",
        data() {
            return {
                echarts:{},
                myCharts:{},
                option:{
                    title : {
                        text: 'host状态',
                        subtext: '纯属虚构'
                    },
                    tooltip : {
                        trigger: 'axis'
                    },
                    legend: {
                        data:['最高气温']
                    },
                    toolbox: {
                        show : true,
                        feature : {
                            mark : {show: true},
                            dataView : {show: true, readOnly: false},
                            magicType : {show: true, type: ['line', 'bar']},
                            restore : {show: true},
                            saveAsImage : {show: true}
                        }
                    },
                    calculable : true,
                    xAxis : [
                        {
                            type : 'category',
                            boundaryGap : false,
                            data : ['10:00','11:00','12:00','13:00','14:00','15:00','16:00']
                        }
                    ],
                    yAxis : [
                        {
                            type : 'value',
                            minInterval:1,
                            axisLabel : {
                                formatter: '{value} '
                            }
                        }
                    ],
                    series : [
                        {
                            name:'状态',
                            type:'line',
                            data:[0, 1, 0, 1,1, 0,1],
                            markPoint : {
                                data : [
                                    {type : 'max', name: '最大值'},
                                    {type : 'min', name: '最小值'}
                                ]
                            },

                        },

                    ]
                }
            }
        },
        created(){
          this.initEcharts();
        },
        methods:{
           initEcharts(){
               this.echarts = require('echarts');
               this.myCharts = this.echarts.init(document.getElementById("myChart"));
               this.myCharts.setOption(this.option);
           }
        }

    }
</script>

<style scoped>

</style>
