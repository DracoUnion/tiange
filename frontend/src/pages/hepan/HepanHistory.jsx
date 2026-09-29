import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import client from '../../api/client';
import { isLoggedIn } from '../../api/client';

export default function HepanHistory() {
  const nav = useNavigate();
  const [list, setList] = useState([]);
  useEffect(() => { if (isLoggedIn()) client.get('/hepan/history').then((d) => setList(d.items || [])); }, []);
  const del = async (id) => { await client.delete('/hepan/delete', { params: { hepan_id: id } }); setList((l) => l.filter((x) => x.id !== id)); };
  return (
    <div className="page">
      <div className="page-head"><h1 className="page-title">我的合盘</h1>
        <div className="page-sub">婚姻 · 相处 · 事业</div></div>
      {list.length === 0 && <div className="loading">暂无记录，<a style={{ color: 'var(--gold)' }} onClick={() => nav('/hepan')}>去合盘</a></div>}
      {list.map((h) => (
        <div key={h.id} className="card clickable" style={{ marginBottom: 10 }} onClick={() => nav(`/hepan/${h.id}`)}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <b>{h.title}</b>
            <span><span className="card-price">{new Date(h.created_at).toLocaleDateString()}</span>
              <button className="btn ghost" style={{ padding: '4px 8px' }} onClick={(e) => { e.stopPropagation(); del(h.id); }}>删</button></span>
          </div>
        </div>
      ))}
    </div>
  );
}