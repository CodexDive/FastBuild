import CryptoJS from 'crypto-js';

// Blob 下载文件，可解决 download 设置不生效，任然会打开图片等类型的文件的问题
/**
 *
 * @param {string} url 地址
 * @param {string} fileName 文件名称
 */
export function downloadByBlob(url, fileName) {
  const x = new XMLHttpRequest();
  x.open('GET', url, true);
  x.responseType = 'blob';
  x.onload = function (e) {
    const url = window.URL.createObjectURL(x.response);
    const elink = document.createElement('a');
    elink.href = url;
    elink.target = '_self'; // 当前也 target打开新页面
    elink.download = fileName;
    elink.style.display = 'none';
    document.body.appendChild(elink);
    setTimeout(() => {
      elink.click();
      document.body.removeChild(elink);
    }, 66);
  };
  x.send();
}

// AES加密
/**
 *
 * @param {string} word 要加密的值
 * @param {string} keyStr 加密的 key,前后端一致
 * @param {string} ivStr 加密的偏移量， 前后端一致
 * @returns 加密后的数据
 */
export function encryptByAES(word, keyStr, ivStr) {
  let key = '';
  let iv = '';

  key = CryptoJS.enc.Utf8.parse(keyStr);
  iv = CryptoJS.enc.Utf8.parse(ivStr);

  let srcs = CryptoJS.enc.Utf8.parse(word);
  // 加密模式为CBC，补码方式为PKCS5Padding（也就是PKCS7）
  let encrypted = CryptoJS.AES.encrypt(srcs, key, {
    iv: iv,
    mode: CryptoJS.mode.CBC,
    padding: CryptoJS.pad.Pkcs7,
  });

  //返回base64
  return CryptoJS.enc.Base64.stringify(encrypted.ciphertext);
}

// AES解密
/**
 *
 * @param {string} word 要解密的值
 * @param {string} keyStr 解密的 key,前后端一致
 * @param {string} ivStr 解密的偏移量， 前后端一致
 * @returns 解密后的数据
 */
export function decryptByAES(word, keyStr, ivStr) {
  let key = '';
  let iv = '';

  key = CryptoJS.enc.Utf8.parse(keyStr);
  iv = CryptoJS.enc.Utf8.parse(ivStr);

  let base64 = CryptoJS.enc.Base64.parse(word);

  let src = CryptoJS.enc.Base64.stringify(base64);

  // 解密模式为CBC，补码方式为PKCS5Padding（也就是PKCS7）
  let decrypt = CryptoJS.AES.decrypt(src, key, {
    iv: iv,
    mode: CryptoJS.mode.CBC,
    padding: CryptoJS.pad.Pkcs7,
  });

  let decryptedStr = decrypt.toString(CryptoJS.enc.Utf8);
  return decryptedStr.toString();
}
