const routes = [
  {
    path: '/home',
    name: 'Home',
    redirect: { name: 'Home' },
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('@/views/home/index.vue'),
      },
    ],
  },
];

export default routes;
