import { useState } from 'react';
import client from '../../api/client';

export default function Chenggu() {
  const [f, setF] = useState({ calendar: 'solar', year: 1990, month: 5, day: 15, hour: 12 });
  const [res, setRes] = useState(null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState('');
  const set = (k) => (e) => setF({ ...f, [k]: e.target.value });
  const run = async () => {
    setLoading(true); setErr('');
    try { setRes(await client.get('/chenggu', { params: { ...f } })); }
    catch (e) { setErr(e.message); } finally { setLoading(false); }
  };
  return (
    <div className="page" style={{ maxWidth: 620 }}>
      <div className="page-head"><h1 className="page-title">骨 称骨论命</h1>
        <div className="page-sub">骨重计算，免费人生预测</div></div>
      <div className="card">
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(120px,1fr))', gap: 10 }}>
          <div className="field"><label>历法</label>
            <select className="select" value={f.calendar} onChange={set('calendar')}>
              <option value="solar">公历</option><option value="lunar">农历</option></select></div>
          <div className="field"><label>年</label><input className="input" value={f.year} onChange={set('year')} /></div>
          <div className="field"><label>月</label><input className="input" value={f.month} onChange={set('month')} /></div>
          <div className="field"><label>日</label><input className="input" value={f.day} onChange={set('day')} /></div>
          <div className="field"><label>时</label><input className="input" value={f.hour} onChange={set('hour')} /></div>
        </div>
        <button className="btn block" disabled={loading} onClick={run}>{loading ? '计算中…' : '称骨'}</button>
      </div>
      {err && <div className="err">{err}</div>}
      {res && (
        <div className="result-box">
          <div style={{ fontSize: 26, fontWeight: 700, color: 'var(--gold)' }}>{res.total}</div>
          <span className={'guxing ' + (res.luck.startsWith('上') ? 'great' : res.luck.startsWith('中') ? 'mid' : 'bad')}>{res.luck}</span>
          <div className="grid" style={{ gridTemplateColumns: 'repeat(4,1fr)', marginTop: 10 }}>
            {Object.entries(res.parts).map(([k, p]) => (
              <div key={k} className="card" style={{ padding: 8, textAlign: 'center' }}>
                <div style={{ fontSize: 11, color: 'var(--muted)' }}>{p.label}</div>
                <b style={{ color: 'var(--gold-2)' }}>{p.value}</b>
              </div>
            ))}
          </div>
          <div style={{ borderTop: '1px solid var(--line)', marginTop: 12, paddingTop: 10 }}>
            <b>称骨歌诀</b>
            <p>{res.song}</p>
          </div>
        </div>
      )}
    </div>
  );
}