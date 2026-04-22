import { useEffect } from 'react';
import Header from '../components/common/Header';
import InteractionResult from '../components/common/InteractionResult';
import RecentInteractions from '../components/common/RecentInteractions';
import ChatLogger from '../components/chat/ChatLogger';
import InteractionForm from '../components/form/InteractionForm';
import { useAppDispatch, useAppSelector } from '../app/hooks';
import { fetchHcps } from '../features/hcps/hcpsSlice';
import { fetchInteractions } from '../features/interactions/interactionsSlice';

export default function App() {
  const dispatch = useAppDispatch();
  const current = useAppSelector((state) => state.interactions.current);
  const items = useAppSelector((state) => state.interactions.items);

  useEffect(() => {
    dispatch(fetchHcps());
    dispatch(fetchInteractions());
  }, [dispatch]);

  return (
    <div className="page-shell">
      <Header />
      <main className="layout-grid">
        <div className="left-column">
          <InteractionForm />
          <ChatLogger />
        </div>
        <div className="right-column">
          <InteractionResult data={current} />
        </div>
      </main>
      <RecentInteractions items={items} />
    </div>
  );
}
