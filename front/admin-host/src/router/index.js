import Vue from 'vue'
import Main from '@/components/Main'
import HostHistory from '@/components/HostHistory'
import RealTimeMonitor from '@/components/RealTimeMonitor'
import Router from 'vue-router'
Vue.use(Router);

export default new Router({
  routes: [
    {path: '/', name: 'main', component: Main},
    {path:'/HostHistory',name:'HostHistory',component: HostHistory},
    {path:'/RealTimeMonitor',name:'RealTimeMonitor',component: RealTimeMonitor}
  ]
})
