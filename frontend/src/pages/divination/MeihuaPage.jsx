import { useState } from 'react';
import client from '../../api/client';
import MemberPicker from '../../components/MemberPicker';
import { useAuth } from '../../store/AuthContext';
import { useNavigate } from 'react-router-dom';
import { isLoggedIn } from '../../api/client';

export default function MeihuaPage() {
  const nav = useNavigate();
  const { selectedMember, refreshUser } = useAuth();
  const [numbers, setNumbers] = useState('');
  const [res, setRes] = useState(null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState('');
  if (!isLoggedIn()) { nav('/login'); return null; }

  const run = async () => {
    setLoading(true); setErr('');
    try {
      const nums = numbers.split(/[,\s，]+/).map(Number).filter(Boolean).slice(0, 2);
      const d = await client.post('/paipan/meihua/suiji', { numbers: nums, member_id: selectedMember?.id });
      setRes(d);
      refreshUser();
    } catch (e) { setErr(e.message); } finally { setLoading(false); }
  };

  return (
    <div className="page" style={{ maxWidth: 620 }}>
      <div className="page-head"><h1 className="page-title">梅 梅花易数</h1>
        <div className="page-sub">梅花心易，万物皆卦</div></div>
      <div className="card">
        <div className="field"><label>起卦数字（可填两个数字，如 3,7）</label>
          <input className="input" value={numbers} onChange={(e) => setNumbers(e.target.value)} placeholder="留空则随机" />
        </div>
        <button className="btn block" disabled={loading} onClick={run}>{loading ? '起卦中…' : '起卦'}</button>
      </div>
      {err && <div className="err">{err}</div>}
      {res && (
        <div className="result-box">
          <b>本卦：{res.ben_gua.name}（{res.ben_gua.full}）</b>
          <div className="page-sub">上卦 {res.paipan.upper}·{res.paipan.upper_attr.nature}　下卦 {res.paipan.lower}·{res.paipan.lower_attr.nature}　动爻：第{res.paipan.moving_yao}爻</div>
          <p>{res.ben_gua.guaci}</p>
          <p style={{ color: 'var(--muted)' }}>{res.ben_gua.baihua}</p>
          {res.bian_gua && <div style={{ borderTop: '1px solid var(--line)', marginTop: 10, paddingTop: 8 }}>
            <b>变卦：{res.bian_gua.name}（{res.bian_gua.full}）</b>
            <p>{res.bian_gua.guaci}</p>
          </div>}
        </div>
      )}
    </div>
  );
}