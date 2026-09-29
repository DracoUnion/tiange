import { useNavigate } from 'react-router-dom';
import { ToolCard } from '../../components/BeansHint';

export default function BooksTab() {
  const nav = useNavigate();
  const d = (p) => nav(p);
  return (
    <div className="page">
      <div className="page-head"><h1 className="page-title">命书</h1><div className="page-sub">AI 撰写一生传记，生成后免费回看</div></div>
      <div className="grid">
        <ToolCard icon="书" title="八字命书" desc="基于八字命盘，撰写一生传记" price="消耗40豆" tag="回看免费" onClick={() => d('/books/mingshu/bazi')} />
        <ToolCard icon="书" title="紫微命书" desc="基于紫微命盘，撰写一生传记" price="消耗40豆" tag="回看免费" onClick={() => d('/books/mingshu/ziwei')} />
        <ToolCard icon="命" title="人生天命书" desc="八字紫微合一，阐述天命" price="消耗60豆" tag="回看免费" onClick={() => d('/books/mingshu/tianming')} />
        <ToolCard icon="信" title="十年之约" desc="来自未来的一封信" price="消耗40豆" tag="回看免费" onClick={() => d('/books/ten-year-letter')} />
        <ToolCard icon="骨" title="称骨论命" desc="骨重计算，人生预测" price="免费" onClick={() => d('/books/chenggu')} />
        <ToolCard icon="八" title="八字排盘" desc="四柱十神 · 大运流年" price="免费" onClick={() => d('/books/bazipan')} />
      </div>
    </div>
  );
}