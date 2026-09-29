import { useState } from 'react';
import client, { streamSSE } from '../../api/client';
import { useNavigate } from 'react-router-dom';
import { isLoggedIn } from '../../api/client';
import { useAuth } from '../../store/AuthContext';

const TYPE_META = {
  '64gua': { api: 'qian/64gua/random/q', stream: 'qian/64gua/random/ai/stream' },
  guanyin: { api: 'qian/guanyin/random/q', stream: 'qian/guanyin/random/ai/stream' },
  zhuge: { api: 'qian/zhuGeShenSuan/random/q', stream: 'qian/zhuGeShenSuan/random/ai/stream' },
};

export default function QianPage({ type, title, icon }) {
  const nav = useNavigate();
  const { refreshUser } = useAuth();
  const [things, setThings] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [aiText, setAiText] = useState('');
  const [aiMode, setAiMode] = useState(false);
  const [err, setErr] = useState('');

  const draw = async (useAi) => {
    setLoading(true); setErr(''); setAiText('');
    try {
      if (useAi) {
        if (!isLoggedIn()) { nav('/login'); return; }
        const meta = TYPE_META[type];
        await streamSSE('/' + meta.stream + '?things=' + encodeURIComponent(things), {
          onDraw: (d) => { setResult(d); refreshUser(); },
          onData: (t) => setAiText((p) => p + t),
          onError: (e) => setErr(e.message),
        });
      } else {
        const d = await client.get(`/${TYPE_META[type].api}`, { params: { things } });
        setResult(d);
        refreshUser();
      }
    } catch (e) { setErr(e.message); } finally { setLoading(false); }
  };

  return (
    <div className="page" style={{ maxWidth: 640 }}>
      <div className="page-head"><h1 className="page-title">{icon} {title}</h1>
        <div className="page-sub">诚心默念所问之事，点击抽签</div></div>
      <div className="card">
        <div className="field"><label>所问之事</label>
          <input className="input" value={things} onChange={(e) => setThings(e.target.value)} placeholder="如：近期事业运如何？" /></div>
        <div style={{ display: 'flex', gap: 10 }}>
          <button className="btn" style={{ flex: 1 }} disabled={loading} onClick={() => draw(false)}>
            {loading ? '占卜中…' : '抽签'}
          </button>
          <button className="btn ghost" style={{ flex: 1 }} disabled={loading} onClick={() => draw(true)}>
            ✨ AI 解卦
          </button>
        </div>
        {!isLoggedIn() && <div className="page-sub" style={{ marginTop: 8 }}>登录后可享 AI 解卦服务</div>}
      </div>
      {err && <div className="err">{err}</div>}

      {result && (
        <div className="result-box">
          {result.name && (
            <>
              <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                <span style={{ fontWeight: 700, fontSize: 18 }}>{result.name}</span>
                {result.guxing && <span className={'guxing ' + (['大吉', '中吉', '吉'].includes(result.guxing) ? 'great' : result.guxing === '凶' ? 'bad' : 'mid')}>{result.guxing}</span>}
                {result.order && <span style={{ color: 'var(--muted)', fontSize: 12 }}>第{result.order}卦</span>}
              </div>
              {result.imgURL && <img src={result.imgURL} alt="" style={{ width: 120, borderRadius: 8, marginTop: 8 }} />}
              <p style={{ whiteSpace: 'pre-wrap' }}>{result.guaci}</p>
              <p style={{ color: 'var(--muted)', whiteSpace: 'pre-wrap' }}>{result.baihua}</p>
              <details style={{ marginTop: 8 }}>
                <summary style={{ cursor: 'pointer', color: 'var(--gold)' }}>查看卦辞详解</summary>
                <p style={{ whiteSpace: 'pre-wrap', fontSize: 13, color: 'var(--muted)' }}>{result.yaoci}</p>
              </details>
            </>
          )}
          {result.qian && (
            <>
              <div style={{ fontWeight: 700, fontSize: 18 }}>{result.qian} · {result.title}</div>
              <p>{result.text}</p>
              <p style={{ color: 'var(--muted)' }}>{result.interpret}</p>
            </>
          )}
          {aiText && <div style={{ marginTop: 12, borderTop: '1px solid var(--line)', paddingTop: 10 }}><b>✨ AI 解卦</b><p style={{ whiteSpace: 'pre-wrap' }}>{aiText}</p></div>}
        </div>
      )}
    </div>
  );
}