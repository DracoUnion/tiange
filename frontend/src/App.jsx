import { Routes, Route } from 'react-router-dom';
import AppLayout from './layouts/AppLayout';

import Home from './pages/Home';
import DivinationTab from './pages/tabs/DivinationTab';
import FortuneTab from './pages/tabs/FortuneTab';
import BooksTab from './pages/tabs/BooksTab';
import MineTab from './pages/tabs/MineTab';

import Login from './pages/auth/Login';
import Register from './pages/auth/Register';
import ForgetPassword from './pages/auth/ForgetPassword';

import FortunePage from './pages/fortune/FortunePage';
import FortuneHistory from './pages/fortune/FortuneHistory';

import QianPage from './pages/divination/QianPage';
import PaipanPage from './pages/divination/PaipanPage';
import MeihuaPage from './pages/divination/MeihuaPage';
import XiaoliurenPage from './pages/divination/XiaoliurenPage';
import QimenPage from './pages/divination/QimenPage';
import DaliurenPage from './pages/divination/DaliurenPage';

import BaziPan from './pages/books/BaziPan';
import Chenggu from './pages/books/Chenggu';
import MingshuPage from './pages/books/MingshuPage';
import TenYearLetter from './pages/books/TenYearLetter';

import NameFortune from './pages/name/NameFortune';
import NameOpt from './pages/name/NameOpt';
import PhoneAnalysis from './pages/name/PhoneAnalysis';
import ToolHistory from './pages/name/ToolHistory';

import Hepan from './pages/hepan/Hepan';
import HepanHistory from './pages/hepan/HepanHistory';
import HepanDetail from './pages/hepan/HepanDetail';

import UserInfo from './pages/mine/UserInfo';
import Vip from './pages/mine/Vip';
import XinshiBeans from './pages/mine/XinshiBeans';
import Members from './pages/mine/Members';
import MemberEdit from './pages/mine/MemberEdit';
import Invitation from './pages/mine/Invitation';
import AiDaoist from './pages/mine/AiDaoist';
import Contact from './pages/mine/Contact';
import Agreement from './pages/mine/Agreement';

export default function App() {
  return (
    <AppLayout>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/divination" element={<DivinationTab />} />
        <Route path="/fortune" element={<FortuneTab />} />
        <Route path="/books" element={<BooksTab />} />
        <Route path="/mine" element={<MineTab />} />

        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/forget-password" element={<ForgetPassword />} />

        <Route path="/fortune/:kind" element={<FortunePage />} />
        <Route path="/fortune/history" element={<FortuneHistory />} />

        <Route path="/divination/yaogua" element={<QianPage type="64gua" title="周易占卜" icon="卦" />} />
        <Route path="/divination/guanyin" element={<QianPage type="guanyin" title="观音灵签" icon="签" />} />
        <Route path="/divination/zhuge" element={<QianPage type="zhuge" title="诸葛神算" icon="课" />} />
        <Route path="/divination/liuyao" element={<PaipanPage type="liuyao" title="六爻占卜" icon="爻" />} />
        <Route path="/divination/meihua" element={<MeihuaPage />} />
        <Route path="/divination/xiaoliuren" element={<XiaoliurenPage />} />
        <Route path="/divination/qimen" element={<QimenPage />} />
        <Route path="/divination/daliuren" element={<DaliurenPage />} />

        <Route path="/books/bazipan" element={<BaziPan />} />
        <Route path="/books/chenggu" element={<Chenggu />} />
        <Route path="/books/mingshu/:type" element={<MingshuPage />} />
        <Route path="/books/ten-year-letter" element={<TenYearLetter />} />

        <Route path="/name-fortune" element={<NameFortune />} />
        <Route path="/name-opt" element={<NameOpt />} />
        <Route path="/phone-analysis" element={<PhoneAnalysis />} />
        <Route path="/tool-history" element={<ToolHistory />} />

        <Route path="/hepan" element={<Hepan />} />
        <Route path="/hepan/history" element={<HepanHistory />} />
        <Route path="/hepan/:id" element={<HepanDetail />} />

        <Route path="/user-info" element={<UserInfo />} />
        <Route path="/vip" element={<Vip />} />
        <Route path="/xinshi-beans" element={<XinshiBeans />} />
        <Route path="/members" element={<Members />} />
        <Route path="/members/new" element={<MemberEdit />} />
        <Route path="/members/:id" element={<MemberEdit />} />
        <Route path="/invitation" element={<Invitation />} />
        <Route path="/ai-daoist" element={<AiDaoist />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="/agreement" element={<Agreement />} />
      </Routes>
    </AppLayout>
  );
}