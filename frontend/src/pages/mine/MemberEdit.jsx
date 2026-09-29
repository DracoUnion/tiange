import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import client from '../../api/client';
import { useAuth } from '../../store/AuthContext';
import { isLoggedIn } from '../../api/client';

const blank = () => ({
  name: '', relation: 'self', gender: 'male', is_self: 0, calendar: 'solar',
  birth_year: 1990, birth_month: 1, birth_day: 1, birth_hour: 12, birth_minute: 0, timezone: 'Asia/Shanghai',
});

export default function MemberEdit() {
  const { id } = useParams();
  const nav = useNavigate();
  const { addMember, refreshMembers } = useAuth();
  const [f, setF] = useState(blank());
  const [err, setErr] = useState('');
  useEffect(() => {
    if (id && isLoggedIn()) client.get('/members').then((list) => {
      const m = list.find((x) => String(x.id) === id);
      if (m) setF({ ...blank(), ...m });
    });
  }, [id]);
  if (!isLoggedIn()) { nav('/login'); return null; }
  const set = (k) => (e) => setF({ ...f, [k]: e.target.value });
  const submit = async () => {
    setErr('');
    try {
      if (id) { await client.put(`/members/${id}`, f); } else { await addMember(f); }
      await refreshMembers();
      nav('/members');
    } catch (e) { setErr(e.message); }
  };
  return (
    <div className="page" style={{ maxWidth: 620 }}>
      <div className="page-head"><h1 className="page-title">{id ? '编辑成员' : '添加成员'}</h1></div>
      <div className="card">
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(140px,1fr))', gap: 10 }}>
          <div className="field"><label>姓名</label><input className="input" value={f.name} onChange={set('name')} /></div>
          <div className="field"><label>性别</label>
            <select className="select" value={f.gender} onChange={set('gender')}>
              <option value="male">男</option><option value="female">女</option></select></div>
          <div className="field"><label>关系</label>
            <select className="select" value={f.relation} onChange={set('relation')}>
              <option value="self">本人</option><option value="parent">父母</option>
              <option value="spouse">伴侣</option><option value="child">子女</option><option value="friend">朋友</option></select></div>
          <div className="field"><label>历法</label>
            <select className="select" value={f.calendar} onChange={set('calendar')}>
              <option value="solar">公历</option><option value="lunar">农历</option></select></div>
          <div className="field"><label>年</label><input className="input" value={f.birth_year} onChange={set('birth_year')} /></div>
          <div className="field"><label>月</label><input className="input" value={f.birth_month} onChange={set('birth_month')} /></div>
          <div className="field"><label>日</label><input className="input" value={f.birth_day} onChange={set('birth_day')} /></div>
          <div className="field"><label>时</label><input className="input" value={f.birth_hour} onChange={set('birth_hour')} /></div>
        </div>
        <label style={{ display: 'flex', gap: 6, alignItems: 'center', fontSize: 13, margin: '6px 0' }}>
          <input type="checkbox" checked={f.is_self === 1} onChange={(e) => setF({ ...f, is_self: e.target.checked ? 1 : 0 })} />
          我本人
        </label>
        {err && <div className="err">{err}</div>}
        <button className="btn block" onClick={submit}>保存</button>
      </div>
    </div>
  );
}