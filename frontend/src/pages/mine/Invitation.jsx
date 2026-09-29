import { useEffect, useState } from 'react';
import client from '../../api/client';
import { useAuth } from '../../store/AuthContext';
import { isLoggedIn } from '../../api/client';

export default function Invitation() {
  const { user } = useAuth();
  const [records, setRecords] = useState([]);
  useEffect(() => {
    if (isLoggedIn()) {
      client.get('/user/invitation/code').then((d) => setCode(d.code));
      client.get('/user/invitation/records').then((d) => setRecords(d || []));
    }
  }, []);
  const [code, setCode] = useState('');
  return (
    <div className="page" style={{ maxWidth: 560 }}>
      <div className="page-head"><h1 className="page-title">邀请好友</h1>
        <div className="page-sub">邀请好友注册，双方各得 20 心识豆</div></div>
      {isLoggedIn() ? (
        <div className="card" style={{ textAlign: 'center' }}>
          <div className="page-sub">我的邀请码</div>
          <div style={{ fontSize: 26, fontWeight: 700, color: 'var(--gold)', letterSpacing: 3, margin: '8px 0' }}>{code || user?.invite_code}</div>
          <button className="btn" onClick={() => navigator.clipboard?.writeText(code || user?.invite_code || '')}>复制邀请码</button>
          <div className="page-sub" style={{ marginTop: 10 }}>分享链接：https://www.buhuo.xin/?invite={code}</div>
        </div>
      ) : <a href="#/login" className="btn block">登录查看</a>}
      <div className="page-head" style={{ marginTop: 16 }}><h2 className="section-title">已邀请 {records.length} 人</h2></div>
      {records.map((r, i) => (
        <div key={i} className="card" style={{ padding: 10, marginBottom: 8 }}>
          <b>{r.username}</b> <span className="page-sub">{new Date(r.created_at).toLocaleDateString()}</span>
        </div>
      ))}
    </div>
  );
}