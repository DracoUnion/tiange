import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../store/AuthContext';
import Captcha from '../../components/Captcha';

export default function Register() {
  const { register, loading } = useAuth();
  const nav = useNavigate();
  const [f, setF] = useState({ username: '', password: '', email: '', invite_code: '' });
  const [capId, setCapId] = useState('');
  const [capAns, setCapAns] = useState('');
  const [err, setErr] = useState('');
  const set = (k) => (e) => setF({ ...f, [k]: e.target.value });

  const submit = async (e) => {
    e.preventDefault();
    setErr('');
    try { await register(f, capId, capAns); nav('/mine'); }
    catch (ex) { setErr(ex.message); }
  };
  return (
    <div className="page" style={{ maxWidth: 420 }}>
      <div className="card" style={{ marginTop: 20 }}>
        <h1 className="page-title" style={{ textAlign: 'center' }}>注册</h1>
        <div className="page-sub" style={{ textAlign: 'center' }}>首次注册赠送 50 心识豆 ✨</div>
        <form onSubmit={submit} style={{ marginTop: 16 }}>
          <div className="field"><label>用户名</label>
            <input className="input" required value={f.username} onChange={set('username')} placeholder="3-32位" /></div>
          <div className="field"><label>密码</label>
            <input className="input" type="password" required value={f.password} onChange={set('password')} placeholder="至少6位" /></div>
          <div className="field"><label>邮箱（可选）</label>
            <input className="input" type="email" value={f.email} onChange={set('email')} /></div>
          <div className="field"><label>邀请码（可选）</label>
            <input className="input" value={f.invite_code} onChange={set('invite_code')} /></div>
          <div className="field"><label>验证码</label><Captcha onId={setCapId} onChange={setCapAns} /></div>
          {err && <div className="err">{err}</div>}
          <button className="btn block" disabled={loading}>{loading ? '注册中…' : '注册并登录'}</button>
        </form>
        <div style={{ textAlign: 'center', marginTop: 12 }}>
          <a href="#/login" style={{ color: 'var(--gold)', fontSize: 13 }}>已有账号，去登录</a>
        </div>
      </div>
    </div>
  );
}