import { useEffect, useState } from 'react';
import client from '../../api/client';
import { isLoggedIn } from '../../api/client';

export default function FortuneHistory() {
  const [list, setList] = useState([]);
  useEffect(() => {
    if (!isLoggedIn()) return;
    client.get('/question/records', { params: { page: 1, size: 30 } }).then((d) => setList(d.items || []));
  }, []);
  return (
    <div className="page">
      <div className="page-head"><h1 className="page-title">占卜历史</h1></div>
      {list.length === 0 && <div className="loading">暂无记录</div>}
      {list.map((x) => (
        <div key={x.id} className="card" style={{ marginBottom: 10 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <b>{x.things || '（未填问题）'}</b>
            <span className="card-price">{new Date(x.created_at).toLocaleString()}</span>
          </div>
          <div className="card-desc">{x.type}</div>
        </div>
      ))}
    </div>
  );
}