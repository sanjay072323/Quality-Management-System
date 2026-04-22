import { configureStore } from '@reduxjs/toolkit';
import interactionsReducer from '../features/interactions/interactionsSlice';
import hcpsReducer from '../features/hcps/hcpsSlice';

export const store = configureStore({
  reducer: {
    interactions: interactionsReducer,
    hcps: hcpsReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
