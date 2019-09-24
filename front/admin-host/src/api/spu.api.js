import {axios} from './axios.config'

class SpuApi {
  static getTreeData() {
    return axios.get('/get_tree_info');
  }

  static getTableDetails(sysId, check_type) {
    return axios.post('/get_detail',
      {sys_id: sysId, check_type: check_type})
  }
}

export default SpuApi
