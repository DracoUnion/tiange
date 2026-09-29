import { useEffect, useState } from 'react';
import client from '../../api/client';
import { useAuth } from '../../store/AuthContext';
import { isLoggedIn } from '../../api/client';

export default function Vip() {
  const { user, refreshUser } = useAuth();
  const [tiers, setTiers] = useState([]);
  const [msg, setMsg] = useState('');
  useEffect(() => {
    if (isLoggedIn()) client.get('/xinshi/pricing/list').then((d) => setTiers(d || []));
  }, []);
  const buy = async (tier) => {
    try { await client.post('/vip/order', { tier: tier.level, period: 'monthly' }); setMsg(`已开通 ${tier.name}`); refreshUser(); }
    catch (e) { setMsg(e.message); }
  };
  return (
    <div className="page" style={{ maxWidth: 720 }}>
      <div className="page-head"><h1 className="page-title">💎 VIP 会员</h1>
        <div className="page-sub">当前等级：{user?.vip_level || 'free'} · 享豆消耗折扣与每日额度加成</div></div>
      <div className="grid">
        {tiers.map((t) => (
          <div key={t.level} className="card" style={{ textAlign: 'center' }}>
            <div style={{ fontWeight: 700, fontSize: 17 }}>{t.name}</div>
            <div style={{ fontSize: 24, color: 'var(--gold)', margin: '8px 0' }}>¥{t.price_monthly_cny}<span style={{ fontSize: 12 }}>/月</span></div>
            <div className="page-sub">消耗折扣 {t.discount * 10} 折</div>
            <div className="page-sub">每月赠豆 {t.beans_monthly}</div>
            {user?.vip_level === t.level
              ? <span className="guxing great" style={{ marginTop: 10 }}>当前会员</span>
              : <button className="btn block" style={{ marginTop: 10 }} onClick={() => buy(t)}>开通</button>}
          </div>
        ))}
      </div>
      {msg && <div className="page-sub" style={{ color: 'var(--green)', textAlign: 'center', marginTop: 10 }}>{msg}</div>}
      <div className="page-sub" style={{ textAlign: 'center', marginTop: 8 }}>本地演示为占位支付，生产对接支付网关</div>
    </div>
  );
}