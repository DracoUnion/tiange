import { useState } from 'react';
import client from '../api/client';
import { useAuth } from '../store/AuthContext';

/* 豆余额提示 + 可关闭 */
export default function BeansHint() {
  const { beans } = useAuth();
  return beans === undefined ? null : (
    <div className="page-sub" style={{ margin: '4px 0' }}>
      当前心识豆余额：<b style={{ color: 'var(--gold)' }}>{beans}</b> 豆
    </div>
  );
}

/* 通用工具卡片（跳转 + 定价） */
export function ToolCard({ icon, title, desc, price, tag, onClick }) {
  return (
    <div className="card clickable" onClick={onClick}>
      <div className="coin">{icon}</div>
      <div className="card-title">{title}</div>
      <div className="card-desc">{desc}</div>
      {price && <div className="card-price">{price}</div>}
      {tag && <span className="card-tag">{tag}</span>}
    </div>
  );
}