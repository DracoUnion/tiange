import { useState } from 'react';
import client from '../../api/client';
import { useNavigate } from 'react-router-dom';
import { isLoggedIn } from '../../api/client';
import { useAuth } from '../../store/AuthContext';

export default function PhoneAnalysis() {
  const nav = useNavigate();
  const { refreshUser } = useAuth();
  const [phone, setPhone] = useState('');
  const [res, setRes] = useState(null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState('');
  if (!isLoggedIn()) { nav('/login'); return null; }
  const run = async () => {
    setLoading(true); setErr('');
    try { setRes(await client.get(`/baxing/phoneNumber/${phone}`)); refreshUser(); }
    catch (e) { setErr(e.message); } finally { setLoading(false); }
  };
  return (
    <div className="page" style={{ maxWidth: 640 }}>
      <div className="page-head"><h1 className="page-title">数 手机号分析</h1>
        <div className="page-sub">号码吉凶，运势预测 · 消耗20豆</div></div>
      <div className="card">
        <div className="field"><label>手机号</label>
          <input className="input" value={phone} onChange={(e) => setPhone(e.target.value)} placeholder="输入手机号" />
        </div>
        <button className="btn block" disabled={loading || phone.length < 6} onClick={run}>{loading ? '分析中…' : '开始分析'}</button>
      </div>
      {err && <div className="err">{err}</div>}
      {res && (
        <div className="result-box">
          <div style={{ display: 'flex', gap: 20 }}>
            <div><b style={{ color: 'var(--gold-2)' }}>{res.phone}</b></div>
            <div className="page-sub">数理和：{res.digits}</div>
            <div className="guxing mid">五行 {res.five}</div>
          </div>
          <p style={{ marginTop: 10 }}>{res.interpret}</p>
        </div>
      )}
    </div>
  );
}