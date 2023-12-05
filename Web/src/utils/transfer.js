import humanFormat from 'human-format';

const K = 1024;

const storageScale = new humanFormat.Scale({
  k: K,
  M: K * K,
  G: K * K * K,
  T: K * K * K * K,
  P: K * K * K * K * K,
});

/**
 * 存储大小格式化
 * @param size 文件大小
 * @returns 1337 ↔ 1.34kB
 */
export const storageFormatter = size => {
  if (isNaN(size)) return;
  return humanFormat(size, {
    scale: storageScale,
    separator: '',
    maxDecimals: 1,
  });
};
