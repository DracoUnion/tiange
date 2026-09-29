import { useState } from 'react';
import client from '../../api/client';
import MemberPicker from '../../components/MemberPicker';
import { useAuth } from '../../store/AuthContext';
import { useNavigate } from 'react-router-dom';
import { isLoggedIn } from '../../api/client';

export default function XiaoliurenPage() {
  const nav = useNavigate();
  const { selectedMember, refreshUser } = useAuth();
  const [res, setRes] = useState(null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState('');
  if (!isLoggedIn()) { nav('/login'); return null; }
  const run = async () => {
    setLoading(true); setErr('');
    try { setRes(await client.post('/paipan/xiaoliuren', { member_id: selectedMember?.id })); refreshUser(); }
    catch (e) { setErr(e.message); } finally { setLoading(false); }
  };
  return (
    <div className="page" style={{ maxWidth: 620 }}>
      <div className="page-head"><h1 className="page-title">小 小六壬</h1>
        <div className="page-sub">快速起课，问事明晰 · 大安-留连-速喜-赤口-小吉-空亡</div></div>
      <div className="card">
        <MemberPicker />
        <button className="btn block" style={{ marginTop: 10 }} disabled={loading} onClick={run}>{loading ? '起课中…' : '起课'}</button>
      </div>
      {err && <div className="err">{err}</div>}
      {res && (
        <div className="result-box">
          <b style={{ fontSize: 22, color: 'var(--gold)' }}>{res.gong}</b>
          <p>{res.text}</p>
        </div>
      )}
    </div>
  );
}