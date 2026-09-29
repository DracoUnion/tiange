import { useEffect, useState } from 'react';
import client from '../../api/client';
import { useAuth } from '../../store/AuthContext';
import { isLoggedIn } from '../../api/client';

export default function XinshiBeans() {
  const { beans, refreshUser } = useAuth();
  const [pkgs, setPkgs] = useState([]);
  const [logs, setLogs] = useState([]);
  const [code, setCode] = useState('');
  const [msg, setMsg] = useState('');
  useEffect(() => {
    if (!isLoggedIn()) return;
    client.get('/xinshi/package/list').then((d) => setPkgs(d || []));
    client.get('/xinshi/beans/log', { params: { page: 1, size: 20 } }).then((d) => setLogs(d.items || []));
  }, []);
  const redeem = async () => {
    try { await client.post('/xinshi/code/redeem', { code }); setMsg('兑换成功'); refreshUser(); setCode(''); }
    catch (e) { setMsg(e.message); }
  };
  return (
    <div className="page" style={{ maxWidth: 720 }}>
      <div className="page-head"><h1 className="page-title">✦ 心识豆</h1>
        <div className="page-sub">当前余额：<b style={{ color: 'var(--gold)' }}>{beans}</b> 豆</div></div>
      <div className="grid">
        {pkgs.map((p) => (
          <div key={p.id} className="card" style={{ textAlign: 'center' }}>
            <div style={{ fontSize: 16, fontWeight: 700 }}>{p.name}</div>
            <div style={{ fontSize: 22, color: 'var(--gold)', margin: '6px 0' }}>{p.beans} 豆</div>
            <div className="page-sub">¥{p.price_cny}{p.bonus ? ` + ${p.bonus}` : ''}</div>
            <button className="btn block" style={{ marginTop: 10, opacity: .6 }}>充值（占位）</button>
          </div>
        ))}
      </div>
      <div className="card" style={{ marginTop: 14 }}>
        <div className="page-sub">兑换码（演示码 XINSHI50）</div>
        <div style={{ display: 'flex', gap: 8 }}>
          <input className="input" value={code} onChange={(e) => setCode(e.target.value)} placeholder="输入兑换码" />
          <button className="btn" onClick={redeem}>兑换</button>
        </div>
        {msg && <div className="err" style={{ color: 'var(--green)' }}>{msg}</div>}
      </div>
      <div className="page-head" style={{ marginTop: 16 }}><h2 className="section-title">收支明细</h2></div>
      {logs.map((l, i) => (
        <div key={i} className="card" style={{ padding: 10, marginBottom: 8 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span>{l.note || l.reason}</span>
            <b style={{ color: l.delta > 0 ? 'var(--green)' : '#ef9a96' }}>{l.delta > 0 ? `+${l.delta}` : l.delta}</b>
          </div>
          <div className="page-sub">{new Date(l.created_at).toLocaleString()} · 余额 {l.balance_after}</div>
        </div>
      ))}
    </div>
  );
}