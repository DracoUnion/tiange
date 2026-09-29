import { createContext, useContext, useEffect, useState, useCallback } from 'react';
import client, { TOKEN_KEY, setAuth, clearAuth, isLoggedIn } from '../api/client';

const AuthCtx = createContext(null);
export const useAuth = () => useContext(AuthCtx);

export default function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [beans, setBeans] = useState(0);
  const [members, setMembers] = useState([]);
  const [selectedMember, setSelectedMember] = useState(null);
  const [loading, setLoading] = useState(false);

  const refreshUser = useCallback(async () => {
    if (!isLoggedIn()) return;
    try {
      const d = await client.get('/user/detail');
      setUser(d);
      setBeans(d.beans || 0);
    } catch (e) { /* 401 handled by interceptor */ }
  }, []);

  const refreshMembers = useCallback(async () => {
    if (!isLoggedIn()) return;
    try {
      const list = await client.get('/members');
      setMembers(list);
      const self = list.find((m) => m.is_self === 1) || list[0];
      setSelectedMember((cur) => cur || self || null);
    } catch (e) { /* ignore */ }
  }, []);

  useEffect(() => { refreshUser(); refreshMembers(); }, [refreshUser, refreshMembers]);

  const login = async (account, password, captchaId, captchaAnswer) => {
    setLoading(true);
    try {
      const d = await client.post('/login', { account, password, captcha_id: captchaId, captcha_answer: captchaAnswer });
      setAuth(d.token, d.uid);
      await refreshUser();
      await refreshMembers();
      return d;
    } finally { setLoading(false); }
  };

  const register = async (payload, captchaId, captchaAnswer) => {
    setLoading(true);
    try {
      const d = await client.post('/register', { ...payload, captcha_id: captchaId, captcha_answer: captchaAnswer });
      setAuth(d.token, d.uid);
      await refreshUser();
      await refreshMembers();
      return d;
    } finally { setLoading(false); }
  };

  const logout = async () => {
    try { await client.post('/logout'); } catch (e) { /* ignore */ }
    clearAuth();
    setUser(null); setMembers([]); setBeans(0); setSelectedMember(null);
  };

  const addMember = async (m) => {
    const d = await client.post('/members', m);
    await refreshMembers();
    return d;
  };

  return (
    <AuthCtx.Provider value={{
      user, beans, setBeans, members, selectedMember, setSelectedMember,
      login, register, logout, refreshUser, refreshMembers, addMember, loading,
    }}>
      {children}
    </AuthCtx.Provider>
  );
}