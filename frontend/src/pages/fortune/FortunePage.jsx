import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import client from '../../api/client';
import MemberPicker from '../../components/MemberPicker';
import { useAuth } from '../../store/AuthContext';
import { isLoggedIn } from '../../api/client';

const KIND = {
  today: ['今日运势', '日'], week: ['本周运势', '周'], month: ['本月运势', '月'],
  year: ['今年运势', '年'], dayun: ['大运运势', '运'], onelife: ['一生运势', '生'],
};
const API = { today: 'fortune/today', week: 'fortune/thisWeek', month: 'fortune/thisMonth',
  year: 'fortune/thisYear', dayun: 'fortune/thisDayun', onelife: 'fortune/oneLife' };

function LuckBadge({ luck }) {
  const cls = ['大吉', '中吉', '吉'].includes(luck) ? 'great' : ['小吉', '平'].includes(luck) ? 'mid' : 'bad';
  return <span className={'guxing ' + cls}>{luck}</span>;
}

export default function FortunePage() {
  const { kind } = useParams();
  const nav = useNavigate();
  const { selectedMember, refreshUser } = useAuth();
  const [res, setRes] = useState(null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState('');

  if (!isLoggedIn()) { nav('/login'); return null; }

  const run = async () => {
    setLoading(true); setErr('');
    try {
      const d = await client.get(`/${API[kind]}`, { params: { member_id: selectedMember?.id } });
      setRes(d);
      refreshUser();
    } catch (e) { setErr(e.message); } finally { setLoading(false); }
  };

  const [title, icon] = KIND[kind] || [kind, '✨'];
  return (
    <div className="page" style={{ maxWidth: 620 }}>
      <div className="page-head">
        <h1 className="page-title">{icon} {title}</h1>
        <div className="page-sub">选择成员，生成运势</div>
      </div>
      <MemberPicker />
      <button className="btn block" style={{ marginTop: 12 }} disabled={loading} onClick={run}>
        {loading ? '推演中…' : '开始测算'}
      </button>
      {err && <div className="err">{err}</div>}

      {res && (
        <div className="result-box" style={{ marginTop: 16 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <LuckBadge luck={res.luck} />
            <span style={{ color: 'var(--gold-2)', fontWeight: 600 }}>综合评分 {res.score}</span>
            <span style={{ color: 'var(--muted)', fontSize: 12 }}>宜{res.direction} · {res.color}</span>
          </div>
          <p style={{ margin: '10px 0' }}>{res.summary}</p>
          <div className="grid" style={{ gridTemplateColumns: 'repeat(5,1fr)' }}>
            {Object.entries(res.categories).map(([k, v]) => (
              <div key={k} style={{ textAlign: 'center' }}>
                <div style={{ fontSize: 12, color: 'var(--muted)' }}>{k}</div>
                <div style={{ fontWeight: 600, color: v > 70 ? '#8cd68c' : v < 45 ? '#ef9a96' : 'var(--gold-2)' }}>{v}</div>
              </div>
            ))}
          </div>
          <div style={{ display: 'flex', gap: 24, marginTop: 10 }}>
            <div><b style={{ color: 'var(--gold)' }}>宜</b><br />{res.yi.join(' · ')}</div>
            <div><b style={{ color: '#ef9a96' }}>忌</b><br />{res.ji.join(' · ')}</div>
          </div>
          <div className="page-sub" style={{ marginTop: 8 }}>当日干支：{res.day_ganzhi}</div>
        </div>
      )}
    </div>
  );
}