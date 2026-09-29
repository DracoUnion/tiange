import { useState } from 'react';
import client from '../../api/client';
import MemberPicker from '../../components/MemberPicker';
import { useAuth } from '../../store/AuthContext';
import { useNavigate } from 'react-router-dom';
import { isLoggedIn } from '../../api/client';

const METHODS = [
  ['suiji', '随机起卦'], ['shouyao', '手摇铜钱'], ['shijian', '时间起卦'],
  ['shuzi', '数字起卦'], ['ai', 'AI 起卦'],
];
const LINE_POS = ['初爻', '二爻', '三爻', '四爻', '五爻', '上爻'];

function Line({ l, i }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '5px 0' }}>
      <span style={{ width: 44, color: 'var(--muted)' }}>{LINE_POS[i]}</span>
      <span style={{ fontSize: 20, letterSpacing: 7, color: l.yang ? 'var(--gold-2)' : 'var(--muted)' }}>
        {l.moving ? (l.yang ? '━━━━━ ×' : '── ── ×') : (l.yang ? '━━━━━' : '── ──')}
      </span>
      {l.moving && <span style={{ color: 'var(--gold)', fontSize: 11 }}>动</span>}
    </div>
  );
}

export default function PaipanPage({ type, title, icon }) {
  const nav = useNavigate();
  const { selectedMember, refreshUser } = useAuth();
  const [method, setMethod] = useState('suiji');
  const [things, setThings] = useState('');
  const [res, setRes] = useState(null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState('');

  if (!isLoggedIn()) { nav('/login'); return null; }

  const run = async () => {
    setLoading(true); setErr('');
    try {
      const d = await client.post(`/paipan/liuyao/${method}`, { things, member_id: selectedMember?.id });
      setRes(d);
      refreshUser();
    } catch (e) { setErr(e.message); } finally { setLoading(false); }
  };

  return (
    <div className="page" style={{ maxWidth: 620 }}>
      <div className="page-head"><h1 className="page-title">{icon} {title}</h1>
        <div className="page-sub">六爻起卦，五种起卦法</div></div>
      <div className="card">
        <div className="field"><label>起卦方式</label>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
            {METHODS.map(([k, label]) => (
              <button key={k} className={'btn ' + (method === k ? '' : 'ghost')} onClick={() => setMethod(k)}>{label}</button>
            ))}
          </div></div>
        <div className="field"><label>所问之事</label>
          <input className="input" value={things} onChange={(e) => setThings(e.target.value)} placeholder="问事业/感情/财运…" /></div>
        <button className="btn block" disabled={loading} onClick={run}>{loading ? '起卦中…' : '起卦'}</button>
      </div>
      {err && <div className="err">{err}</div>}

      {res && (
        <div className="result-box">
          <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
            <span style={{ fontWeight: 700, fontSize: 18 }}>{res.gua.full}</span>
            {res.gua.guxing && <span className={'guxing ' + (['大吉', '中吉', '吉'].includes(res.gua.guxing) ? 'great' : res.gua.guxing === '凶' ? 'bad' : 'mid')}>{res.gua.guxing}</span>}
            {res.paipan.moving_yao.length > 0 && <span style={{ color: 'var(--gold)', fontSize: 12 }}>动爻：{res.paipan.moving_yao.join(',')}</span>}
          </div>
          <div style={{ marginTop: 8 }}>
            {res.paipan.lines.map((l, i) => <Line key={i} l={l} i={i} />)}
          </div>
          <div style={{ borderTop: '1px solid var(--line)', marginTop: 10, paddingTop: 8 }}>
            <b>本卦解</b>
            <p>{res.gua.guaci}</p>
            <p style={{ color: 'var(--muted)' }}>{res.gua.baihua}</p>
          </div>
        </div>
      )}
    </div>
  );
}