import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../store/AuthContext';
import { isLoggedIn } from '../../api/client';

export default function MineTab() {
  const nav = useNavigate();
  const { user, beans, logout } = useAuth();
  const d = (p) => nav(p);
  const Item = ({ icon, title, sub, onClick }) => (
    <div className="card clickable" onClick={onClick}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div><div className="card-title" style={{ margin: 0 }}>{icon} {title}</div>
          {sub && <div className="card-desc" style={{ minHeight: 0 }}>{sub}</div>}</div>
        <div style={{ color: 'var(--muted)' }}>›</div>
      </div>
    </div>
  );
  return (
    <div className="page">
      <div className="card" style={{ display: 'flex', alignItems: 'center', gap: 14, marginBottom: 14 }}>
        <div className="seal" style={{ width: 54, height: 54, fontSize: 26 }}>{user?.nickname?.[0] || '客'}</div>
        <div style={{ flex: 1 }}>
          <div className="card-title" style={{ margin: 0 }}>{user?.nickname || (isLoggedIn() ? '我的' : '未登录')}</div>
          <div className="page-sub">心识豆余额：<b style={{ color: 'var(--gold)' }}>{beans ?? 0}</b> 豆</div>
        </div>
        {!isLoggedIn() ? <button className="btn" onClick={() => d('/login')}>登录</button>
          : <button className="btn ghost" onClick={logout}>退出</button>}
      </div>
      <div className="grid">
        <Item icon="👤" title="个人中心" sub="资料与设置" onClick={() => d('/user-info')} />
        <Item icon="💎" title="VIP会员" sub="折扣与权益" onClick={() => d('/vip')} />
        <Item icon="✦" title="心识豆" sub="充值 · 明细 · 兑换" onClick={() => d('/xinshi-beans')} />
        <Item icon="👨‍👩‍👧" title="我的成员" sub="管理出生信息" onClick={() => d('/members')} />
        <Item icon="🙏" title="天格道长" sub="AI 智者对话" onClick={() => d('/ai-daoist')} />
        <Item icon="💍" title="我的合盘" sub="婚姻 · 相处 · 事业" onClick={() => d('/hepan/history')} />
        <Item icon="✉️" title="邀请好友" sub="邀请得豆" onClick={() => d('/invitation')} />
        <Item icon="✍️" title="分析记录" sub="起名 · 姓名 · 手机" onClick={() => d('/tool-history')} />
        <Item icon="📞" title="联系我们" sub="联系方式" onClick={() => d('/contact')} />
        <Item icon="📄" title="用户协议" sub="服务条款" onClick={() => d('/agreement')} />
      </div>
    </div>
  );
}