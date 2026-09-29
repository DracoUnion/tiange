import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import client from '../../api/client';

export default function HepanDetail() {
  const { id } = useParams();
  const [d, setD] = useState(null);
  useEffect(() => { client.get('/hepan/detail', { params: { hepan_id: id } }).then(setD).catch(() => {}); }, [id]);
  return (
    <div className="page" style={{ maxWidth: 640 }}>
      <div className="page-head"><h1 className="page-title">合盘详情</h1></div>
      {!d && <div className="loading">加载中…</div>}
      {d && (
        <div className="result-box">
          <div style={{ fontSize: 18, fontWeight: 700 }}>{d.title}</div>
          <div style={{ fontSize: 30, color: 'var(--gold)', margin: '8px 0' }}>契合度 {d.result.overall}</div>
          <p>{d.result.insights}</p>
          <div className="grid" style={{ gridTemplateColumns: 'repeat(3,1fr)' }}>
            {Object.entries(d.result.dimensions).map(([k, v]) => (
              <div key={k} className="card" style={{ padding: 8, textAlign: 'center' }}>
                <div style={{ fontSize: 11, color: 'var(--muted)' }}>{k}</div><b className="page-sub">{v}</b>
              </div>
            ))}
          </div>
          <div style={{ borderTop: '1px solid var(--line)', marginTop: 10, paddingTop: 8 }}>
            <b>建议</b>
            {d.result.suggestions.map((s, i) => <div key={i} className="page-sub">· {s}</div>)}
          </div>
        </div>
      )}
    </div>
  );
}