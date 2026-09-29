import { useState } from 'react';
import { streamSSE } from '../../api/client';
import { useNavigate } from 'react-router-dom';
import { isLoggedIn } from '../../api/client';
import { useAuth } from '../../store/AuthContext';

export default function NameFortune() {
  const nav = useNavigate();
  const { refreshUser } = useAuth();
  const [name, setName] = useState('');
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState('');
  if (!isLoggedIn()) { nav('/login'); return null; }
  const run = async () => {
    setLoading(true); setErr(''); setText('');
    try {
      await streamSSE('/analysis/name/stream?name=' + encodeURIComponent(name), {
        onData: (t) => setText((p) => p + t),
        onError: (e) => setErr(e.message),
        onDone: () => refreshUser(),
      });
    } catch (e) { setErr(e.message); } finally { setLoading(false); }
  };
  return (
    <div className="page" style={{ maxWidth: 640 }}>
      <div className="page-head"><h1 className="page-title">吉 姓名分析</h1>
        <div className="page-sub">姓名能量，运势影响 · 每日1次免费，超次40豆</div></div>
      <div className="card">
        <div className="field"><label>姓名</label>
          <input className="input" value={name} onChange={(e) => setName(e.target.value)} placeholder="输入你的姓名" />
        </div>
        <button className="btn block" disabled={loading || !name} onClick={run}>{loading ? '分析中…' : '开始分析'}</button>
      </div>
      {err && <div className="err">{err}</div>}
      {text && <div className="result-box"><p style={{ whiteSpace: 'pre-wrap' }}>{text}</p></div>}
    </div>
  );
}