import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../store/AuthContext';
import { isLoggedIn } from '../api/client';
import { useState } from 'react';

const TABS = [
  { path: '/', label: '首页', ico: '🏠' },
  { path: '/divination', label: '占卜', ico: '☯' },
  { path: '/books', label: '命书', ico: '📜' },
  { path: '/fortune', label: '运势', ico: '✨' },
  { path: '/mine', label: '我的', ico: '👤' },
];

export default function AppLayout({ children }) {
  const nav = useNavigate();
  const loc = useLocation();
  const { user, beans, logout } = useAuth();
  const [menu, setMenu] = useState(false);

  const active = (p) => (p === '/' ? loc.pathname === '/' || loc.pathname.startsWith('/home')
    : loc.pathname.startsWith(p));

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="topbar-inner">
          <div className="brand" onClick={() => nav('/')} style={{ cursor: 'pointer' }}>
            <div className="seal">心</div>
            <div>
              <span className="brand-name">天格</span>
              <span className="brand-slogan">算法为骨 · 六年打磨</span>
            </div>
          </div>
          <div className="nav-actions">
            {beans != null && beans > 0 && <span className="beans-pill">✦ {beans} 豆</span>}
            {isLoggedIn() ? (
              <>
                <button className="nav-btn" onClick={() => nav('/user-info')}>{user?.nickname || '我的'}</button>
                <button className="nav-btn primary" onClick={() => nav('/vip')}>VIP</button>
                <button className="nav-btn danger" onClick={logout}>退出</button>
              </>
            ) : (
              <>
                <button className="nav-btn" onClick={() => nav('/login')}>登录</button>
                <button className="nav-btn primary" onClick={() => nav('/vip')}>VIP</button>
              </>
            )}
          </div>
        </div>
        {menu && (
          <div className="mobile-menu">
            <button className="mobile-menu-item" onClick={() => { nav('/user-info'); setMenu(false); }}>
              ✨ 登录享好礼 <span className="login-bonus">首次登录赠送50心识豆</span>
            </button>
            <button className="mobile-menu-item" onClick={() => { nav('/ai-daoist'); setMenu(false); }}>🙏 天格道长</button>
          </div>
        )}
      </header>

      <main>{children}</main>

      <div className="float-balls">
        <div className="float-ball tiange" title="天格道长" onClick={() => nav('/ai-daoist')}>道</div>
        <div className="float-ball xinshi" title="心识豆" onClick={() => nav('/xinshi-beans')}>心</div>
      </div>

      <nav className="tabbar">
        {TABS.map((t) => (
          <div key={t.path} className={'tab' + (active(t.path) ? ' active' : '')} onClick={() => nav(t.path)}>
            <span className="ico">{t.ico}</span>{t.label}
          </div>
        ))}
      </nav>
    </div>
  );
}