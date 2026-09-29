import { useState } from 'react';
import client from '../../api/client';
import MemberPicker from '../../components/MemberPicker';
import { useAuth } from '../../store/AuthContext';
import { useNavigate } from 'react-router-dom';
import { isLoggedIn } from '../../api/client';

export default function TenYearLetter() {
  const nav = useNavigate();
  const { selectedMember, refreshUser } = useAuth();
  const [status, setStatus] = useState(null);
  const [letter, setLetter] = useState(null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState('');
  if (!isLoggedIn()) { nav('/login'); return null; }
  const run = async () => {
    setLoading(true); setErr('');
    try {
      const d = await client.post('/ten-year-letter', { type: 'ten_year', member_id: selectedMember?.id });
      setLetter(d);
      refreshUser();
    } catch (e) { setErr(e.message); } finally { setLoading(false); }
  };
  return (
    <div className="page" style={{ maxWidth: 640 }}>
      <div className="page-head"><h1 className="page-title">信 十年之约</h1>
        <div className="page-sub">来自未来的一封信 · 消耗40豆</div></div>
      <div className="card">
        <MemberPicker />
        <button className="btn block" style={{ marginTop: 10 }} disabled={loading} onClick={run}>
          {loading ? '写信中…' : '收信'}
        </button>
      </div>
      {err && <div className="err">{err}</div>}
      {letter && (
        <div className="result-box" style={{ textAlign: 'center' }}>
          <div style={{ fontSize: 26 }}>✉️</div>
          <p style={{ whiteSpace: 'pre-wrap', fontSize: 15 }}>{letter.content}</p>
        </div>
      )}
    </div>
  );
}