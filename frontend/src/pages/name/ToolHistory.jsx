import { useEffect, useState } from 'react';
import client from '../../api/client';
import { isLoggedIn } from '../../api/client';

export default function ToolHistory() {
  const [list, setList] = useState([]);
  const load = () => client.get('/tool-history', { params: { page: 1, size: 30 } })
    .then((d) => setList(d.items || []));
  useEffect(() => { if (isLoggedIn()) load(); }, []);
  const del = async (id) => { await client.delete(`/tool-history/${id}`); load(); };
  return (
    <div className="page">
      <div className="page-head"><h1 className="page-title">分析记录</h1>
        <div className="page-sub">起名 · 姓名 · 手机号 结果</div></div>
      {list.length === 0 && <div className="loading">暂无记录</div>}
      {list.map((t) => {
        let parsed = {};
        try { parsed = JSON.parse(t.result || '{}'); } catch (e) { /* */ }
        return (
          <div key={t.id} className="card" style={{ marginBottom: 10 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <b>{t.input || t.tool}</b>
              <button className="btn ghost" style={{ padding: '4px 10px' }} onClick={() => del(t.id)}>删除</button>
            </div>
            <div className="card-desc">{t.tool} · {new Date(t.created_at).toLocaleString()}</div>
            {parsed.names && <div>{parsed.names.join('　')}</div>}
            {parsed.interpret && <div className="page-sub">{parsed.interpret}</div>}
          </div>
        );
      })}
    </div>
  );
}