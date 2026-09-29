import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../store/AuthContext';
import Captcha from '../../components/Captcha';
import { isLoggedIn } from '../../api/client';

export default function Login() {
  const { login, loading } = useAuth();
  const nav = useNavigate();
  const [account, setAccount] = useState('');
  const [password, setPassword] = useState('');
  const [capId, setCapId] = useState('');
  const [capAns, setCapAns] = useState('');
  const [err, setErr] = useState('');

  if (isLoggedIn()) nav('/mine');

  const submit = async (e) => {
    e.preventDefault();
    setErr('');
    try { await login(account, password, capId, capAns); nav('/mine'); }
    catch (ex) { setErr(ex.message); }
  };
  return (
    <div className="page" style={{ maxWidth: 420 }}>
      <div className="card" style={{ marginTop: 20 }}>
        <h1 className="page-title" style={{ textAlign: 'center' }}>登录</h1>
        <div className="page-sub" style={{ textAlign: 'center' }}>欢迎回来，算法为骨 · 六年打磨</div>
        <form onSubmit={submit} style={{ marginTop: 16 }}>
          <div className="field"><label>账号</label>
            <input className="input" value={account} onChange={(e) => setAccount(e.target.value)} placeholder="用户名或邮箱" /></div>
          <div className="field"><label>密码</label>
            <input className="input" type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="密码" /></div>
          <div className="field"><label>验证码</label><Captcha onId={setCapId} onChange={setCapAns} /></div>
          {err && <div className="err">{err}</div>}
          <button className="btn block" disabled={loading}>{loading ? '登录中…' : '登录'}</button>
        </form>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 12, fontSize: 13 }}>
          <Link to="/register" style={{ color: 'var(--gold)' }}>注册账号</Link>
          <Link to="/forget-password" style={{ color: 'var(--muted)' }}>忘记密码</Link>
        </div>
      </div>
    </div>
  );
}