import axios from 'axios';
import { message } from 'ant-design-vue';

function HttpError(message, code) {
  const error = new Error(message);
  error.name = 'HttpError';
  if (code) {
    error.code = code;
  }
  return error;
}

const instance = axios.create({
  baseURL: '',
  headers: {},
});

instance.interceptors.request.use(
  config => {
    config.headers['Content-Type'] = config.headers['Content-Type'] || 'application/json';
    return config;
  },
  error => {
    Promise.reject(error);
  }
);

instance.interceptors.response.use(
  function (response) {
    let result = response.data;
    if (!result) {
      message.error('请求异常');
      throw HttpError('请求异常！');
    }
    if (![0, '0', 200, '200'].includes(result.code)) {
      message.error('请求异常：' + result.msg);
      throw HttpError('请求异常：' + result.msg);
    }
    if (typeof result !== 'object') {
      message.error('返回数据格式异常！');
      throw HttpError('返回数据格式异常！');
    }
    return result.data;
  },
  function (error) {
    let err = null;
    if (error.response) {
      err = HttpError('请求异常：' + error.response.statusText);
      message.error('请求异常：' + error.response.statusText);
      throw err;
    }
    if (error.request) {
      err = HttpError('请求异常：无返回结果');
      message.error('请求异常：' + error.response.statusText);
      throw err;
    }

    throw error;
  }
);

export default instance;
