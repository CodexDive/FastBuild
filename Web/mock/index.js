import { images, progress, checkImage, listSource, listSoftware, tasks } from './images';

export default [
  {
    url: '/mock/api/fast-build/task/all-tasks',
    method: 'get',
    response: () => ({
      code: '200',
      data: {
        result: tasks,
        page: {
          current: 1,
          total: 13,
          pageSize: 10,
        },
      },
    }),
  },
  {
    url: '/mock/api/fast-build/task/images/list-image',
    method: 'get',
    response: () => ({
      code: '200',
      data: {
        result: images,
        page: {
          current: 1,
          total: 12,
          pageSize: 10,
        },
      },
    }),
  },
  {
    url: '/mock/api/fast-build/task/delete-task-by-task-id',
    method: 'delete',
    response: () => ({
      code: '200',
      data: null,
    }),
  },
  {
    url: '/mock/api/fast-build/image/delete-image-by-image-name',
    method: 'delete',
    response: () => ({
      code: '200',
      data: null,
    }),
  },
  {
    url: '/mock/api/fast-build/progress/details',
    method: 'get',
    response: () => ({
      code: '200',
      data: {
        task_id: 1696821710501,
        task_name: '10.101.12.129-admin-1696821710',
        progress: progress,
      },
    }),
  },
  {
    url: '/mock/api/fast-build/task/check-image',
    method: 'post',
    response: () => ({
      code: '200',
      data: checkImage,
    }),
  },
  {
    url: '/mock/api/fast-build/file/list-source',
    method: 'get',
    response: () => ({
      code: '200',
      data: listSource,
    }),
  },
  {
    url: '/mock/api/fast-build/file/list-software',
    method: 'get',
    response: () => ({
      code: '200',
      data: listSoftware,
    }),
  },
  {
    url: '/mock/api/fast-build/task/build-image',
    method: 'post',
    response: () => ({
      code: '200',
      data: null,
    }),
  },
];
