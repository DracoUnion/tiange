import { useAuth } from '../store/AuthContext';
import { useNavigate } from 'react-router-dom';

export default function MemberPicker({ onSelect }) {
  const { members, selectedMember, setSelectedMember } = useAuth();
  const nav = useNavigate();
  if (!members || members.length === 0) {
    return (
      <div className="page-sub">
        暂无成员信息，
        <a style={{ color: 'var(--gold)', cursor: 'pointer' }} onClick={() => nav('/members/new')}>去添加</a>
      </div>
    );
  }
  const cur = onSelect ? onSelect : selectedMember;
  return (
    <select
      className="select"
      value={(onSelect && onSelect.id) || (selectedMember && selectedMember.id) || ''}
      onChange={(e) => {
        const m = members.find((x) => String(x.id) === e.target.value);
        if (m) { setSelectedMember(m); onSelect && onSelect(m); }
      }}
    >
      {members.map((m) => (
        <option key={m.id} value={m.id}>
          {m.name} · {m.birth_year}年{m.birth_month}月{m.birth_day}日
        </option>
      ))}
    </select>
  );
}