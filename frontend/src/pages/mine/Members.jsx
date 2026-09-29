import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import client from '../../api/client';
import { useAuth } from '../../store/AuthContext';
import { isLoggedIn } from '../../api/client';

export default function Members() {
  const nav = useNavigate();
  const { members, refreshMembers } = useAuth();
  useEffect(() => { if (isLoggedIn()) refreshMembers(); }, []);
  const del = async (id) => { await client.delete(`/members/${id}`); refreshMembers(); };
  return (
    <div className="page">
      <div className="page-head"><h1 className="page-title">我的成员</h1>
        <div className="page-sub">管理出生信息，用于运势与命书</div></div>
      <button className="btn block" onClick={() => nav('/members/new')}>＋ 添加成员</button>
      <div style={{ marginTop: 12 }}>
        {members.map((m) => (
          <div key={m.id} className="card clickable" style={{ marginBottom: 10 }} onClick={() => nav(`/members/${m.id}`)}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <b>{m.name}{m.is_self === 1 && '（本人）'}</b>
                <div className="page-sub">{m.gender === 'male' ? '男' : '女'} · {m.birth_year}年{m.birth_month}月{m.birth_day}日{m.birth_hour}时 · {m.calendar === 'solar' ? '公历' : '农历'}</div>
              </div>
              <button className="btn ghost" style={{ padding: '4px 10px' }} onClick={(e) => { e.stopPropagation(); del(m.id); }}>删</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}