import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import client from '../../api/client';
import MemberPicker from '../../components/MemberPicker';
import { useAuth } from '../../store/AuthContext';
import { isLoggedIn } from '../../api/client';

const META = {
  bazi: ['八 八字命书', '36', '基于八字命盘，撰写一生传记'],
  ziwei: ['紫 紫微命书', '36', '基于紫微命盘，撰写一生传记'],
  tianming: ['命 人生天命书', '50', '八字紫微合一，阐述天命'],
};

export default function MingshuPage() {
  const { type } = useParams();
  const nav = useNavigate();
  const { selectedMember, refreshUser } = useAuth();
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState('');
  const [meta, cost, desc] = META[type] || [type, '40', ''];
  if (!isLoggedIn()) { nav('/login'); return null; }

  const run = async () => {
    setLoading(true); setErr('');
    try {
      if (!selectedMember) { setErr('请先添加并选择成员'); return; }
      const d = await client.post('/birth/', { type, member_id: selectedMember.id });
      setResult(d);
      refreshUser();
    } catch (e) { setErr(e.message); } finally { setLoading(false); }
  };

  return (
    <div className="page" style={{ maxWidth: 640 }}>
      <div className="page-head"><h1 className="page-title">{meta}</h1>
        <div className="page-sub">{desc} · 消耗{cost}豆 · 生成后免费回看</div></div>
      <div className="card">
        <MemberPicker />
        <button className="btn block" style={{ marginTop: 10 }} disabled={loading} onClick={run}>
          {loading ? '撰书中…' : '生成命书'}
        </button>
        <div className="page-sub" style={{ marginTop: 8 }}>
          {!selectedMember ? '请先添加成员' : `将为「${selectedMember.name}」撰写命书`}
        </div>
      </div>
      {err && <div className="err">{err}</div>}
      {result && (
        <div className="result-box">
          <b style={{ fontSize: 16 }}>{result.title}</b>
          <p style={{ whiteSpace: 'pre-wrap' }}>{result.content}</p>
          <div className="page-sub">状态：{result.status} · 本次消耗 {result.beans_cost} 豆</div>
        </div>
      )}
    </div>
  );
}