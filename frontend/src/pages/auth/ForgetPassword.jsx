import { useState } from 'react';
import client from '../../api/client';

export default function ForgetPassword() {
  const [email, setEmail] = useState('');
  const [code, setCode] = useState('');
  const [pw, setPw] = useState('');
  const [step, setStep] = useState(1);
  const [msg, setMsg] = useState('');

  const sendCode = async () => {
    try { await client.post('/email/code/apply', { email, purpose: 'reset' }); setMsg('验证码已发送（控制台可见）'); setStep(2); }
    catch (e) { setMsg(e.message); }
  };
  const reset = async () => {
    try { await client.post('/reset-password', { email, code, new_password: pw }); setMsg('密码已重置，请返回登录'); setStep(3); }
    catch (e) { setMsg(e.message); }
  };
  return (
    <div className="page" style={{ maxWidth: 420 }}>
      <div className="card" style={{ marginTop: 20 }}>
        <h1 className="page-title" style={{ textAlign: 'center' }}>重置密码</h1>
        {step === 1 && (
          <>
            <div className="field" style={{ marginTop: 14 }}><label>邮箱</label>
              <input className="input" value={email} onChange={(e) => setEmail(e.target.value)} /></div>
            {msg && <div className="err" style={{ color: 'var(--green)' }}>{msg}</div>}
            <button className="btn block" onClick={sendCode}>发送验证码</button>
          </>
        )}
        {step === 2 && (
          <>
            <div className="field"><label>验证码</label>
              <input className="input" value={code} onChange={(e) => setCode(e.target.value)} /></div>
            <div className="field"><label>新密码</label>
              <input className="input" type="password" value={pw} onChange={(e) => setPw(e.target.value)} /></div>
            {msg && <div className="err" style={{ color: 'var(--green)' }}>{msg}</div>}
            <button className="btn block" onClick={reset}>重置密码</button>
          </>
        )}
        {step === 3 && <a href="#/login" className="btn block">返回登录</a>}
      </div>
    </div>
  );
}