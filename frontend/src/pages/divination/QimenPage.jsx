import { useState } from 'react';
import client from '../../api/client';
import MemberPicker from '../../components/MemberPicker';
import { useAuth } from '../../store/AuthContext';
import { useNavigate } from 'react-router-dom';
import { isLoggedIn } from '../../api/client';

export default function QimenPage() {
  const nav = useNavigate();
  const { selectedMember, refreshUser } = useAuth();
  const [res, setRes] = useState(null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState('');
  if (!isLoggedIn()) { nav('/login'); return null; }
  const run = async () => {
    setLoading(true); setErr('');
    try { setRes(await client.post('/paipan/qimen', { member_id: selectedMember?.id })); refreshUser(); }
    catch (e) { setErr(e.message); } finally { setLoading(false); }
  };
  return (
    <div className="page" style={{ maxWidth: 680 }}>
      <div className="page-head"><h1 className="page-title">奇 奇门遁甲</h1>
        <div className="page-sub">九宫时局，趋吉避凶</div></div>
      <div className="card">
        <MemberPicker />
        <button className="btn block" style={{ marginTop: 10 }} disabled={loading} onClick={run}>{loading ? '起局中…' : '起局'}</button>
      </div>
      {err && <div className="err">{err}</div>}
      {res && (
        <div className="result-box">
          <div className="page-sub">当日干支：{res.day_ganzhi} · 值符：{res.director}</div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: 8, marginTop: 10 }}>
            {res.pan.map((p) => (
              <div key={p.number} className="card" style={{ padding: 10, textAlign: 'center' }}>
                <div style={{ color: 'var(--gold)' }}>{p.palace}</div>
                <div>({p.value})</div>
                <div>{p.star}</div>
                <div style={{ fontSize: 12 }}>{p.door}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}