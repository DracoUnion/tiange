import { useEffect, useState } from 'react';
import client from '../api/client';

export default function Captcha({ onChange, onId }) {
  const [capId, setCapId] = useState('');
  const [img, setImg] = useState('');
  const [answer, setAnswer] = useState('');
  const load = async () => {
    try {
      const d = await client.get('/captcha');
      setImg(`data:image/png;base64,${d.b64s}`);
      setCapId(d.id);
      setAnswer('');
      onId && onId(d.id);
      onChange && onChange('');
    } catch (e) { /* ignore */ }
  };
  useEffect(() => { load(); }, []);
  useEffect(() => { onChange && onChange(answer); onId && onId(capId); }, [answer, capId]);
  return (
    <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
      <input className="input" style={{ flex: 1 }} maxLength={4} placeholder="验证码"
        value={answer} onChange={(e) => setAnswer(e.target.value)} />
      {img && <img src={img} alt="captcha" onClick={load} style={{ height: 44, borderRadius: 8, cursor: 'pointer' }} title="点击刷新" />}
    </div>
  );
}