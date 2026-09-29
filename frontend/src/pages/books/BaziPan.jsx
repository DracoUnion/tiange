import { useState } from 'react';
import client from '../../api/client';

export default function BaziPan() {
  const [f, setF] = useState({ calendar: 'solar', year: 1990, month: 5, day: 15, hour: 12, gender: 'male' });
  const [res, setRes] = useState(null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState('');
  const set = (k) => (e) => setF({ ...f, [k]: e.target.value });
  const run = async () => {
    setLoading(true); setErr('');
    try { setRes(await client.get('/bazi/pan', { params: { ...f } })); }
    catch (e) { setErr(e.message); } finally { setLoading(false); }
  };
  return (
    <div className="page" style={{ maxWidth: 720 }}>
      <div className="page-head"><h1 className="page-title">八 八字排盘</h1>
        <div className="page-sub">输入出生信息，免费排盘</div></div>
      <div className="card">
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(120px,1fr))', gap: 10 }}>
          <div className="field"><label>历法</label>
            <select className="select" value={f.calendar} onChange={set('calendar')}>
              <option value="solar">公历</option><option value="lunar">农历</option></select></div>
          <div className="field"><label>年</label><input className="input" value={f.year} onChange={set('year')} /></div>
          <div className="field"><label>月</label><input className="input" value={f.month} onChange={set('month')} /></div>
          <div className="field"><label>日</label><input className="input" value={f.day} onChange={set('day')} /></div>
          <div className="field"><label>时</label><input className="input" value={f.hour} onChange={set('hour')} /></div>
          <div className="field"><label>性别</label>
            <select className="select" value={f.gender} onChange={set('gender')}>
              <option value="male">男</option><option value="female">女</option></select></div>
        </div>
        <button className="btn block" disabled={loading} onClick={run}>{loading ? '排盘中…' : '开始排盘'}</button>
      </div>
      {err && <div className="err">{err}</div>}
      {res && (
        <div className="result-box">
          <div style={{ overflowX: 'auto' }}>
            <table className="pan-table">
              <thead><tr>
                <th></th>{res.pillars.map((p) => <th key={p.pos}>{p.pos}</th>)}
              </tr></thead>
              <tbody>
                <tr><th>干支</th>{res.pillars.map((p) => <td key={p.pos}><b>{p.gz}</b></td>)}</tr>
                <tr><th>五行</th>{res.pillars.map((p) => <td key={p.pos}>{p.stem_element}</td>)}</tr>
                <tr><th>十神</th>{res.pillars.map((p) => <td key={p.pos}>{p.shishen}</td>)}</tr>
                <tr><th>藏干</th>{res.pillars.map((p) => <td key={p.pos} style={{ fontSize: 12 }}>{p.canggan.join(' ')}</td>)}</tr>
              </tbody>
            </table>
          </div>
          <div className="page-sub" style={{ marginTop: 10 }}>
            日主：<b style={{ color: 'var(--gold-2)' }}>{res.day_master}{res.day_master_element}</b>
            五行：{Object.entries(res.wuxing_count).map(([k, v]) => `${k}${v}`).join('　')}
            缺：{res.wuxing_missing.length ? res.wuxing_missing.join(',') : '无'}
          </div>
          <div style={{ borderTop: '1px solid var(--line)', marginTop: 10, paddingTop: 8 }}>
            <b>大运</b>（{res.yun_forward ? '顺行' : '逆行'}）
            <div className="pan-table" style={{ display: 'grid', gridTemplateColumns: 'repeat(8,1fr)', gap: 4, marginTop: 6 }}>
              {res.dayun.map((d) => (
                <div key={d.index} className="card" style={{ padding: 6, textAlign: 'center' }}>
                  <div style={{ color: 'var(--gold)' }}>{d.gz}</div>
                  <div style={{ fontSize: 10, color: 'var(--muted)' }}>{d.start_age}岁</div>
                  <div style={{ fontSize: 10 }}>{d.shishen}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}