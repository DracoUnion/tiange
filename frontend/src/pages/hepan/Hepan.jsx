import { useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import client from '../../api/client';
import { useAuth } from '../../store/AuthContext';
import { isLoggedIn } from '../../api/client';

export default function Hepan() {
  const nav = useNavigate();
  const [sp] = useSearchParams();
  const { members, refreshUser } = useAuth();
  const [type, setType] = useState(sp.get('type') || 'marriage');
  const [a, setA] = useState('');
  const [b, setB] = useState('');
  const [res, setRes] = useState(null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState('');
  if (!isLoggedIn()) { nav('/login'); return null; }
  const types = [['marriage', '💍 婚姻合盘'], ['communication', '🤝 相处之道'], ['career', '💼 事业合伙']];
  const run = async () => {
    setLoading(true); setErr('');
    try {
      const d = await client.post('/hepan/create', { type, member_a_id: Number(a), member_b_id: Number(b) });
      setRes(d);
      refreshUser();
    } catch (e) { setErr(e.message); } finally { setLoading(false); }
  };
  return (
    <div className="page" style={{ maxWidth: 640 }}>
      <div className="page-head"><h1 className="page-title">合 合盘分析</h1>
        <div className="page-sub">选择两位成员，分析姻缘/相处/事业 · 消耗99豆</div></div>
      <div className="card">
        <div className="field"><label>合盘类型</label>
          <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
            {types.map(([k, label]) => (
              <button key={k} className={'btn ' + (type === k ? '' : 'ghost')} onClick={() => setType(k)}>{label}</button>
            ))}
          </div></div>
        <div className="field"><label>成员一</label>
          <select className="select" value={a} onChange={(e) => setA(e.target.value)}>
            <option value="">请选择</option>{members.map((m) => <option key={m.id} value={m.id}>{m.name}</option>)}</select></div>
        <div className="field"><label>成员二</label>
          <select className="select" value={b} onChange={(e) => setB(e.target.value)}>
            <option value="">请选择</option>{members.map((m) => <option key={m.id} value={m.id}>{m.name}</option>)}</select></div>
        <button className="btn block" disabled={loading || !a || !b} onClick={run}>{loading ? '合盘中…' : '开始合盘'}</button>
        <div className="page-sub" style={{ marginTop: 8 }}><a style={{ color: 'var(--gold)' }} onClick={() => nav('/hepan/history')}>查看我的合盘 →</a></div>
      </div>
      {err && <div className="err">{err}</div>}
      {res && (
        <div className="result-box">
          <div style={{ fontSize: 18, fontWeight: 700 }}>{res.title}</div>
          <div style={{ fontSize: 26, color: 'var(--gold)', margin: '8px 0' }}>契合度 {res.result.overall}</div>
          <p>{res.result.insights}</p>
          <div className="grid" style={{ gridTemplateColumns: 'repeat(3,1fr)' }}>
            {Object.entries(res.result.dimensions).map(([k, v]) => (
              <div key={k} className="card" style={{ padding: 8, textAlign: 'center' }}>
                <div style={{ fontSize: 11, color: 'var(--muted)' }}>{k}</div>
                <b className="page-sub" style={{ color: 'var(--gold-2)' }}>{v}</b>
              </div>
            ))}
          </div>
          <div style={{ borderTop: '1px solid var(--line)', marginTop: 10, paddingTop: 8 }}>
            <b>相处建议</b>
            {res.result.suggestions.map((s, i) => <div key={i} className="page-sub">· {s}</div>)}
          </div>
        </div>
      )}
    </div>
  );
}