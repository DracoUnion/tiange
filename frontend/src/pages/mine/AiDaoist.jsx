import { useState } from 'react';
import { streamSSE } from '../../api/client';
import { useNavigate } from 'react-router-dom';
import { isLoggedIn } from '../../api/client';

export default function AiDaoist() {
  const nav = useNavigate();
  const [msgs, setMsgs] = useState([{ role: 'assistant', content: '贫道天格，愿听施主心事。有何疑惑，尽可道来。' }]);
  const [input, setInput] = useState('');
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState('');
  if (!isLoggedIn()) { nav('/login'); return null; }
  const send = async () => {
    const text = input.trim();
    if (!text || busy) return;
    setInput(''); setErr('');
    setMsgs((m) => [...m, { role: 'user', content: text }, { role: 'assistant', content: '' }]);
    setBusy(true);
    const idx = msgs.length + 1;
    try {
      await streamSSE('/daoist/chat/stream', {
        body: { message: text },
        method: 'POST',
        onData: (t) => setMsgs((m) => { const n = [...m]; n[idx].content += t; return n; }),
        onError: (e) => setErr(e.message),
      });
    } catch (e) { setErr(e.message); } finally { setBusy(false); }
  };
  return (
    <div className="page" style={{ maxWidth: 680, display: 'flex', flexDirection: 'column', height: 'calc(100vh - 200px)' }}>
      <div className="page-head"><h1 className="page-title">🙏 天格道长</h1>
        <div className="page-sub">一位通达道家智慧的 AI 智者</div></div>
      <div style={{ flex: 1, overflowY: 'auto', paddingBottom: 12 }}>
        {msgs.map((m, i) => (
          <div key={i} style={{ display: 'flex', justifyContent: m.role === 'user' ? 'flex-end' : 'flex-start', marginBottom: 8 }}>
            <div className="result-box" style={{ maxWidth: '82%', margin: 0, background: m.role === 'user' ? 'rgba(139,90,43,.2)' : 'var(--bg2)' }}>
              {m.role === 'assistant' && <b style={{ color: 'var(--gold)' }}>道长 · </b>}
              <span style={{ whiteSpace: 'pre-wrap' }}>{m.content}</span>
            </div>
          </div>
        ))}
        {err && <div className="err">{err}</div>}
      </div>
      <div style={{ display: 'flex', gap: 8, position: 'sticky', bottom: 0 }}>
        <input className="input" value={input} onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && send()} placeholder="向道长请教…" />
        <button className="btn" onClick={send} disabled={busy}>{busy ? '…' : '发送'}</button>
      </div>
    </div>
  );
}