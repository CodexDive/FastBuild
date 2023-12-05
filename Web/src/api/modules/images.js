import axios from '../index';

//查询构建列表
export function getBuildList(params) {
  return axios.get('/api/fast-build/task/list-task', { params });
}

// 查询镜像列表
export function getImageList(params) {
  return axios.get('/api/fast-build/image/list-image', { params }); //list-image
}

// 删除构建记录
export function delBuild(params) {
  return axios.delete('/api/fast-build/task/delete-task-by-task-id', { params });
}

// 删除镜像
export function delImage(params) {
  return axios.delete('/api/fast-build/image/delete-image-by-image-name', { params });
}

//查询构建记录
export function buildDetail(params) {
  return axios.get('/api/fast-build/progress/details', { params });
}

// 解析镜像信息
export function parseImageInfo(data) {
  return axios.post(`/api/fast-build/task/check-image?image_name=${data}`);
}

// 查询安装源信息
export function fetchSourceList() {
  return axios.get('/api/fast-build/file/list-source');
}

// 查询安装器信息
export function fetchSoftwareList() {
  return axios.get('/api/fast-build/file/list-software');
}

//创建镜像
export function buildImage(data) {
  return axios.post('/api/fast-build/task/build-image', data);
}
