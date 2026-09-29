import { useNavigate } from 'react-router-dom';
import { ToolCard } from '../../components/BeansHint';

export default function DivinationTab() {
  const nav = useNavigate();
  const d = (p) => nav(p);
  return (
    <div className="page">
      <div className="page-head"><h1 className="page-title">占卜</h1><div className="page-sub">每日各类型免费一次，超次消耗心识豆</div></div>
      <div className="grid">
        <ToolCard icon="卦" title="周易占卜" desc="六十四卦，指引前程" price="每日1次免费 · 超次5豆" onClick={() => d('/divination/yaogua')} />
        <ToolCard icon="签" title="观音灵签" desc="心中疑问，善神指引" price="每日1次免费 · 超次5豆" onClick={() => d('/divination/guanyin')} />
        <ToolCard icon="课" title="诸葛神算" desc="遇事不决，神机妙算" price="每日1次免费 · 超次5豆" onClick={() => d('/divination/zhuge')} />
        <ToolCard icon="爻" title="六爻占卜" desc="问事决断，指点迷津" price="每日1次免费 · 超次15豆" onClick={() => d('/divination/liuyao')} />
        <ToolCard icon="梅" title="梅花易数" desc="梅花心易，万物皆卦" price="每日1次免费 · 超次15豆" onClick={() => d('/divination/meihua')} />
        <ToolCard icon="小" title="小六壬" desc="快速起课，问事明晰" price="每日1次免费 · 超次5豆" onClick={() => d('/divination/xiaoliuren')} />
        <ToolCard icon="奇" title="奇门遁甲" desc="九宫时局，趋吉避凶" price="每日1次免费 · 超次15豆" onClick={() => d('/divination/qimen')} />
        <ToolCard icon="壬" title="大六壬" desc="四课三传，综合占断" price="每日1次免费 · 超次15豆" onClick={() => d('/divination/daliuren')} />
        <ToolCard icon="册" title="历史记录" desc="查看所有占卜历史" onClick={() => d('/fortune/history')} />
      </div>
    </div>
  );
}