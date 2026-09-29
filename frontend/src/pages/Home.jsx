import { useNavigate } from 'react-router-dom';
import { ToolCard } from '../components/BeansHint';
import MemberPicker from '../components/MemberPicker';
import { isLoggedIn } from '../api/client';

function Section({ title, note, children, more, onMore }) {
  return (
    <section className="page" style={{ paddingTop: 14 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
        <div>
          <h2 className="section-title">{title}</h2>
          {note && <div className="section-note">{note}</div>}
        </div>
        {more && <a style={{ color: 'var(--gold)', fontSize: 13, cursor: 'pointer' }} onClick={onMore}>{more} →</a>}
      </div>
      <div className="grid" style={{ marginTop: 12 }}>{children}</div>
    </section>
  );
}

export default function Home() {
  const nav = useNavigate();
  const div = (p) => nav(p);
  return (
    <div>
      <section className="page">
        <MemberPicker />
        <div style={{ marginTop: 6 }}>
          {!isLoggedIn() && (
            <div className="page-sub" style={{ color: 'var(--gold)' }}>
              ✨ 首次登录赠送 50 心识豆 —— <a style={{ cursor: 'pointer' }} onClick={() => div('/login')}>立即登录</a>
            </div>
          )}
        </div>
      </section>

      <section className="page" style={{ paddingTop: 0 }}>
        <div className="grid">
          <div className="card clickable" onClick={() => div('/ai-daoist')}>
            <div className="coin">🧘</div>
            <div className="card-title">天格道长</div>
            <div className="card-desc">AI 智者，答疑解惑，点化迷津</div>
            <div className="card-tag">AI</div>
          </div>
          <div className="card clickable" onClick={() => div('/books/bazipan')}>
            <div className="coin">八</div>
            <div className="card-title">八字排盘</div>
            <div className="card-desc">四柱十神 · 大运流年</div>
            <div className="card-tag" style={{ background: 'rgba(76,175,80,.2)' }}>免费</div>
          </div>
        </div>
      </section>

      <Section title="占卜预测" note="无需登录即可使用，登录后可享AI解卦" more="历史记录" onMore={() => div('/fortune/history')}>
        <ToolCard icon="卦" title="周易占卜" desc="六十四卦，指引前程" price="每日1次免费 · 超次5豆" onClick={() => div('/divination/yaogua')} />
        <ToolCard icon="签" title="观音灵签" desc="心中疑问，善神指引" price="每日1次免费 · 超次5豆" onClick={() => div('/divination/guanyin')} />
        <ToolCard icon="课" title="诸葛神算" desc="遇事不决，神机妙算" price="每日1次免费 · 超次5豆" onClick={() => div('/divination/zhuge')} />
        <ToolCard icon="爻" title="六爻占卜" desc="问事决断，指点迷津" price="每日1次免费 · 超次15豆" onClick={() => div('/divination/liuyao')} />
        <ToolCard icon="梅" title="梅花易数" desc="梅花心易，万物皆卦" price="每日1次免费 · 超次15豆" onClick={() => div('/divination/meihua')} />
        <ToolCard icon="小" title="小六壬" desc="快速起课，问事明晰" price="每日1次免费 · 超次5豆" onClick={() => div('/divination/xiaoliuren')} />
        <ToolCard icon="奇" title="奇门遁甲" desc="九宫时局，趋吉避凶" price="每日1次免费 · 超次15豆" onClick={() => div('/divination/qimen')} />
        <ToolCard icon="壬" title="大六壬" desc="四课三传，综合占断" price="每日1次免费 · 超次15豆" onClick={() => div('/divination/daliuren')} />
      </Section>

      <Section title="天格命书" note="AI为您撰写一生传记，需要登录">
        <ToolCard icon="书" title="八字命书" desc="基于八字命盘，撰写一生传记" price="消耗40豆" tag="生成后免费回看" onClick={() => div('/books/mingshu/bazi')} />
        <ToolCard icon="书" title="紫微命书" desc="基于紫微命盘，撰写一生传记" price="消耗40豆" tag="生成后免费回看" onClick={() => div('/books/mingshu/ziwei')} />
        <ToolCard icon="命" title="人生天命书" desc="八字紫微合一，阐述天命" price="消耗60豆" tag="生成后免费回看" onClick={() => div('/books/mingshu/tianming')} />
        <ToolCard icon="信" title="十年之约" desc="来自未来的一封信" price="消耗40豆" tag="生成后免费回看" onClick={() => div('/books/ten-year-letter')} />
        <ToolCard icon="骨" title="称骨论命" desc="骨重计算，人生预测" price="免费" onClick={() => div('/books/chenggu')} />
        <ToolCard icon="八" title="八字/紫微排盘" desc="八字与紫微命盘，命运解析" price="免费" onClick={() => div('/books/bazipan')} />
      </Section>

      <Section title="运势预测" note="部分功能需要登录">
        <ToolCard icon="日" title="今日运势" desc="查看今日吉凶宜忌" price="消耗5豆" onClick={() => div('/fortune/today')} />
        <ToolCard icon="周" title="本周运势" desc="了解本周整体运势" price="消耗10豆" onClick={() => div('/fortune/week')} />
        <ToolCard icon="月" title="本月运势" desc="掌握本月气运变化" price="消耗15豆" onClick={() => div('/fortune/month')} />
        <ToolCard icon="年" title="今年运势" desc="全年运势结构分析" price="消耗30豆" onClick={() => div('/fortune/year')} />
        <ToolCard icon="运" title="大运运势" desc="十年大运气机解析" price="消耗20豆" onClick={() => div('/fortune/dayun')} />
        <ToolCard icon="生" title="一生运势" desc="纵观人生起伏轨迹" price="消耗50豆" onClick={() => div('/fortune/onelife')} />
      </Section>

      <Section title="合盘分析" note="需要登录 · 120心识豆/次" more="查看历史" onMore={() => div('/hepan/history')}>
        <ToolCard icon="💍" title="婚姻合盘" desc="感情缘分 · 婚姻质量 · 家庭和谐" price="消耗99豆" onClick={() => div('/hepan')} />
        <ToolCard icon="🤝" title="相处之道" desc="性格互补 · 沟通模式 · 相处建议" price="消耗99豆" onClick={() => div('/hepan?type=communication')} />
        <ToolCard icon="💼" title="事业合伙" desc="合作默契 · 财运互补 · 事业发展" price="消耗99豆" onClick={() => div('/hepan?type=career')} />
      </Section>

      <Section title="起名改名" note="部分功能需要登录">
        <ToolCard icon="名" title="智能起名" desc="量身定制，助运改名" price="每日1次免费 · 超次40豆" onClick={() => div('/name-opt')} />
        <ToolCard icon="吉" title="姓名分析" desc="姓名能量，运势影响" price="每日1次免费 · 超次40豆" onClick={() => div('/name-fortune')} />
        <ToolCard icon="数" title="手机号分析" desc="号码吉凶，运势预测" price="消耗20豆" onClick={() => div('/phone-analysis')} />
        <ToolCard icon="录" title="分析记录" desc="查看起名、姓名与手机号结果" onClick={() => div('/tool-history')} />
      </Section>

      <footer className="page" style={{ textAlign: 'center', color: 'var(--muted)', fontSize: 12, paddingBottom: 20 }}>
        <div>© 2026 天格 版权所有</div>
        <div>自我探索 • 内在成长 • 智慧指引</div>
      </footer>
    </div>
  );
}