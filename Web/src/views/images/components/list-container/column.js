import { storageFormatter } from '@/utils/transfer';
import { t } from '@/common/locale/useI18n';
import moment from 'moment';
import { imageTypeEnums } from '@/common/enums';

export const getColumns = (isImageList, noOperate) => {
  const buildListColumn = [
    {
      title: t('TargetImage'),
      dataIndex: 'image_name',
      fixed: 'left',
      width: 200,
    },
    {
      title: t('BasicImage'),
      dataIndex: 'base_image_name',
      width: 200,
    },
    {
      title: t('ImageDesc'),
      dataIndex: 'description',
      width: 200,
    },
    {
      title: t('BuildStatus'),
      dataIndex: 'state',
      width: 200,
    },
    {
      title: t('UpdateTime'),
      dataIndex: 'update_time',
      width: 200,
      customRender: ({ text, record, index, column }) => {
        return text ? moment(new Date(text)).format('YYYY-MM-DD HH:mm:ss') : '';
      },
    },
    {
      title: t('Operate'),
      dataIndex: 'operate',
      fixed: 'right',
      width: 200,
    },
  ];
  const imageListColumn = [
    {
      title: t('ImageName'),
      dataIndex: 'name',
      fixed: 'left',
      width: 200,
    },
    {
      title: t('ImageVersion'),
      dataIndex: 'tag',
      width: 200,
    },
    {
      title: t('ImageDesc'),
      dataIndex: 'description',
      width: 200,
    },
    {
      title: t('ImageType'),
      dataIndex: 'type',
      width: 100,
    },
    {
      title: t('InteractiveMethods'),
      dataIndex: 'interaction',
      width: 100,
    },
    {
      title: t('UpdateTime'),
      dataIndex: 'update_time',
      width: 200,
      customRender: ({ text, record, index, column }) => {
        return text ? moment(new Date(text)).format('YYYY-MM-DD HH:mm:ss') : '';
      },
    },
    {
      title: t('ImageSize'),
      dataIndex: 'size',
      width: 100,
    },
    {
      title: t('Operate'),
      dataIndex: 'operate',
      fixed: 'right',
      width: 200,
    },
  ];
  if (noOperate) {
    return isImageList
      ? imageListColumn.filter(item => item.dataIndex !== 'operate')
      : buildListColumn.filter(item => item.dataIndex !== 'operate');
  }
  return isImageList ? imageListColumn : buildListColumn;
};
