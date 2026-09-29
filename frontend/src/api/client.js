import axios from 'axios';

export const TOKEN_KEY = 'tiange_token';
export const UID_KEY = 'tiange_uid';

const client = axios.create({ baseURL: '/api/v1', timeout: 60000 });

client.interceptors.request.use((cfg) => {
  const token = localStorage.getItem(TOKEN_KEY);
  if (token) cfg.headers.Authorization = `Bearer ${token}`;
  const uid = localStorage.getItem(UID_KEY);
  if (uid) cfg.headers['X-Uid'] = uid;
  cfg.headers['X-Client-Type'] = 'pc_h5';
  cfg.headers['X-Language'] = 'zh-Hans';
  cfg.headers['X-Client-Timezone'] = 'Asia/Shanghai';
  return cfg;
});

client.interceptors.response.use(
  (resp) => {
    const data = resp.data;
    if (data && data.code === 401 && !data.res) {
      localStorage.removeItem(TOKEN_KEY);
      if (window.location.pathname !== '/login') {
        window.location.hash = '#/login';
      }
    }
    if (data && data.code !== 0) {
      return Promise.reject(new Error(data.msg + (data.reason ? '：' + data.reason : '')));
    }
    return data.res !== undefined ? data.res : data;
  },
  (err) => {
    const d = err.response && err.response.data;
    const msg = (d && (d.msg || d.detail)) || err.message;
    return Promise.reject(new Error(msg));
  },
);

export default client;

// 登录态帮助
export const isLoggedIn = () => !!localStorage.getItem(TOKEN_KEY);
export const setAuth = (token, uid) => {
  localStorage.setItem(TOKEN_KEY, token);
  if (uid) localStorage.setItem(UID_KEY, uid);
};
export const clearAuth = () => {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(UID_KEY);
};

// SSE 流式读取：向 <callback> 推送 {event, data} 直到结束
export async function streamSSE(url, { headers = {}, body, method = 'GET', onData, onDraw, onError, onDone }) {
  const token = localStorage.getItem(TOKEN_KEY);
  const resp = await fetch('/api' + url, {
    method,
    headers: { Authorization: `Bearer ${token}`, ...(body ? { 'Content-Type': 'application/json' } : {}), ...headers },
    ...(body ? { body: JSON.stringify(body) } : {}),
  });
  if (!resp.ok) {
    const t = await resp.text();
    onError && onError(new Error(t || `HTTP ${resp.status}`));
    return;
  }
  const reader = resp.body.getReader();
  const decoder = new TextDecoder();
  let buf = '';
  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buf += decoder.decode(value, { stream: true });
      let idx;
      while ((idx = buf.indexOf('\n\n')) >= 0) {
        const frame = buf.slice(0, idx);
        buf = buf.slice(idx + 2);
        const line = frame.split('\n').find((l) => l.startsWith('data:'));
        if (!line) continue;
        const raw = line.slice(5).trim();
        if (raw === '[DONE]') { onDone && onDone(); return; }
        try {
          const j = JSON.parse(raw);
          if (j.draw && onDraw) onDraw(j.draw);
          if (j.text && onData) onData(j.text);
          if (j.error && onError) onError(new Error(j.error));
        } catch (e) { /* skip */ }
      }
    }
    onDone && onDone();
  } catch (e) {
    onError && onError(e);
  }
}