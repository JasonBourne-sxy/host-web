import {axios} from './axios.config'

class SpuApi {
  static getTreeData() {
    return axios.get('/get_tree_info');
  }

  static getTableDetails(sysId, check_type) {
    return axios.post('/get_detail',
      {sys_id: sysId, check_type: check_type})
  }
  static get_warning_history(data) {
    return axios.post('/get_warning_history', data)
  }
  static getMonitorOperateDetails(data) {
    return axios.post('/get_monitor_instance', data)
  }

  static get_real_time_monitor_result(data) {
    return axios.post('/get_real_time_monitor_result', data)
  }
  static insertOrUpdateInstance(data) {
    return axios.post('/insert_or_update_instance', data)
  }

  static deleteInstance(data) {
    return axios.post('/delete_instance', data)
  }

  static query_sys_info(data) {
    return axios.post('/query_sys_info', data)
  }
  static delete_sys_info(data) {
    return axios.post('/delete_sys_info', data)
  }
  static insert_or_update_system_info(data) {
    return axios.post('/insert_or_update_system_info', data)
  }
}

export default SpuApi
