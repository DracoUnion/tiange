import { useState } from 'react';
import client from '../../api/client';
import { useAuth } from '../../store/AuthContext';
import { useNavigate } from 'react-router-dom';
import { isLoggedIn } from '../../api/client';

export default function UserInfo() {
  const nav = useNavigate();
  const { user, refreshUser } = useAuth();
  const [nickname, setNickname] = useState(user?.nickname || '');
  const [msg, setMsg] = useState('');
  if (!isLoggedIn()) { nav('/login'); return null; }
  const save = async () => {
    await client.put('/user/info', { nickname });
    await refreshUser();
    setMsg('已保存');
  };
  return (
    <div className="page" style={{ maxWidth: 520 }}>
      <div className="page-head"><h1 className="page-title">个人中心</h1></div>
      <div className="card">
        <div className="field" style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
          <div className="seal" style={{ width: 56, height: 56, fontSize: 26 }}>{user?.nickname?.[0] || user?.username?.[0]}</div>
          <div><b>{user?.username}</b><div className="page-sub">{user?.email}</div></div>
        </div>
        <div className="field"><label>昵称</label>
          <input className="input" value={nickname} onChange={(e) => setNickname(e.target.value)} /></div>
        {msg && <div className="page-sub" style={{ color: 'var(--green)' }}>{msg}</div>}
        <button className="btn block" onClick={save}>保存</button>
        <div className="page-sub"><b>邀请码</b>：{user?.invite_code || '—'}</div>
      </div>
    </div>
  );
}