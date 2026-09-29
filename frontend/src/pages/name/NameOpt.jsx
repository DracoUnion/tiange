import { useState } from 'react';
import client from '../../api/client';
import { useNavigate } from 'react-router-dom';
import { isLoggedIn } from '../../api/client';
import { useAuth } from '../../store/AuthContext';

export default function NameOpt() {
  const nav = useNavigate();
  const { refreshUser } = useAuth();
  const [f, setF] = useState({ surname: '李', gender: 'male', count: 6 });
  const [res, setRes] = useState(null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState('');
  if (!isLoggedIn()) { nav('/login'); return null; }
  const set = (k) => (e) => setF({ ...f, [k]: e.target.value });
  const run = async () => {
    setLoading(true); setErr('');
    try { setRes(await client.post('/name-opt', f)); refreshUser(); }
    catch (e) { setErr(e.message); } finally { setLoading(false); }
  };
  return (
    <div className="page" style={{ maxWidth: 640 }}>
      <div className="page-head"><h1 className="page-title">名 智能起名</h1>
        <div className="page-sub">量身定制，助运改名 · 每日1次免费，超次40豆</div></div>
      <div className="card">
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 10 }}>
          <div className="field"><label>姓氏</label><input className="input" value={f.surname} onChange={set('surname')} /></div>
          <div className="field"><label>性别</label>
            <select className="select" value={f.gender} onChange={set('gender')}>
              <option value="male">男</option><option value="female">女</option></select></div>
          <div className="field"><label>数量</label>
            <select className="select" value={f.count} onChange={set('count')}>
              <option value={6}>6个</option><option value={9}>9个</option><option value={12}>12个</option></select></div>
        </div>
        <button className="btn block" disabled={loading} onClick={run}>{loading ? '起名中…' : '智能起名'}</button>
      </div>
      {err && <div className="err">{err}</div>}
      {res && (
        <div className="grid" style={{ marginTop: 12 }}>
          {res.names.map((n, i) => (
            <div key={i} className="card" style={{ textAlign: 'center' }}>
              <div style={{ fontSize: 20, fontWeight: 700, color: 'var(--gold-2)' }}>{n}</div>
              <div className="page-sub">推荐</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}