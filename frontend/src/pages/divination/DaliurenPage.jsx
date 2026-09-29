import { useState } from 'react';
import client from '../../api/client';
import MemberPicker from '../../components/MemberPicker';
import { useAuth } from '../../store/AuthContext';
import { useNavigate } from 'react-router-dom';
import { isLoggedIn } from '../../api/client';

export default function DaliurenPage() {
  const nav = useNavigate();
  const { selectedMember, refreshUser } = useAuth();
  const [res, setRes] = useState(null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState('');
  if (!isLoggedIn()) { nav('/login'); return null; }
  const run = async () => {
    setLoading(true); setErr('');
    try { setRes(await client.post('/paipan/daliuren', { member_id: selectedMember?.id })); refreshUser(); }
    catch (e) { setErr(e.message); } finally { setLoading(false); }
  };
  return (
    <div className="page" style={{ maxWidth: 620 }}>
      <div className="page-head"><h1 className="page-title">壬 大六壬</h1>
        <div className="page-sub">四课三传，综合占断</div></div>
      <div className="card">
        <MemberPicker />
        <button className="btn block" style={{ marginTop: 10 }} disabled={loading} onClick={run}>{loading ? '起课中…' : '起课'}</button>
      </div>
      {err && <div className="err">{err}</div>}
      {res && (
        <div className="result-box">
          <div style={{ display: 'flex', gap: 24 }}>
            <div><b>日干</b><br />{res.day_gz}</div>
            <div><b>时干</b><br />{res.hour_gz}</div>
          </div>
          <div style={{ borderTop: '1px solid var(--line)', marginTop: 10, paddingTop: 8 }}>
            <b>四课</b>
            {res.ke.map((k) => <div key={k.pos} className="page-sub">{k.pos}：{k.value}</div>)}
          </div>
          <div style={{ borderTop: '1px solid var(--line)', marginTop: 10, paddingTop: 8 }}>
            <b>三传</b>：<span style={{ color: 'var(--gold)' }}>{res.chuan.join(' → ')}</span>
          </div>
        </div>
      )}
    </div>
  );
}