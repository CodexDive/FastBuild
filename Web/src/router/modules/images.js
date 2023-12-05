const routes = [
  {
    path: '/',
    name: 'Images',
    redirect: { name: 'Images' },
    children: [
      {
        path: '',
        name: 'Images',
        component: () => import('@/views/images/index.vue'),
      },
    ],
  },
];

export default routes;
