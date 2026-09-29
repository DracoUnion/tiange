export default function Contact() {
  return (
    <div className="page" style={{ maxWidth: 560 }}>
      <div className="page-head"><h1 className="page-title">联系我们</h1></div>
      <div className="card">
        <div className="page-sub">命理深度咨询 · 一对一解读 · 紫微斗数 · 人生规划</div>
        <div className="field" style={{ marginTop: 12 }}>
          <label>微信公众号</label><div style={{ fontWeight: 600 }}>天格</div>
        </div>
        <div className="field"><label>商务 / 反馈</label><div style={{ fontWeight: 600 }}>service@buhuo.xin</div></div>
        <div className="field"><label>官方网站</label><a href="https://www.buhuo.xin" style={{ color: 'var(--gold)' }}>https://www.buhuo.xin</a></div>
      </div>
    </div>
  );
}