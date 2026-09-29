import { useNavigate } from 'react-router-dom';
import { ToolCard } from '../../components/BeansHint';
import MemberPicker from '../../components/MemberPicker';

export default function FortuneTab() {
  const nav = useNavigate();
  const d = (p) => nav(p);
  return (
    <div className="page">
      <div className="page-head">
        <h1 className="page-title">运势</h1>
        <div className="page-sub">选择成员，查看多周期运势</div>
      </div>
      <MemberPicker />
      <div className="grid" style={{ marginTop: 14 }}>
        <ToolCard icon="日" title="今日运势" desc="查看今日吉凶宜忌" price="消耗5豆" onClick={() => d('/fortune/today')} />
        <ToolCard icon="周" title="本周运势" desc="了解本周整体运势" price="消耗10豆" onClick={() => d('/fortune/week')} />
        <ToolCard icon="月" title="本月运势" desc="掌握本月气运变化" price="消耗15豆" onClick={() => d('/fortune/month')} />
        <ToolCard icon="年" title="今年运势" desc="全年运势结构分析" price="消耗30豆" onClick={() => d('/fortune/year')} />
        <ToolCard icon="运" title="大运运势" desc="十年大运气机解析" price="消耗20豆" onClick={() => d('/fortune/dayun')} />
        <ToolCard icon="生" title="一生运势" desc="纵观人生起伏轨迹" price="消耗50豆" onClick={() => d('/fortune/onelife')} />
        <ToolCard icon="册" title="历史记录" desc="查看所有运势记录" onClick={() => d('/fortune/history')} />
      </div>
    </div>
  );
}