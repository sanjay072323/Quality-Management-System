import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import api from '../../services/api';

export interface Interaction {
  id: number;
  hcp_id: number;
  interaction_type: string;
  channel: string;
  interaction_date: string;
  raw_notes: string;
  ai_summary: string;
  key_topics: string;
  next_best_action: string;
  follow_up_email?: string;
  compliance_status: string;
}

interface InteractionState {
  items: Interaction[];
  current?: Interaction;
  loading: boolean;
  submitting: boolean;
  error?: string;
}

const initialState: InteractionState = {
  items: [],
  loading: false,
  submitting: false,
};

export const fetchInteractions = createAsyncThunk('interactions/fetch', async () => {
  const response = await api.get<Interaction[]>('/interactions');
  return response.data;
});

export const createFormInteraction = createAsyncThunk(
  'interactions/createForm',
  async (payload: {
    hcp_id: number;
    interaction_type: string;
    channel: string;
    interaction_date: string;
    raw_notes: string;
  }) => {
    const response = await api.post<Interaction>('/interactions/form', payload);
    return response.data;
  },
);

export const createChatInteraction = createAsyncThunk(
  'interactions/createChat',
  async (payload: { hcp_id: number; transcript: string; interaction_date: string }) => {
    const response = await api.post<Interaction>('/interactions/chat', payload);
    return response.data;
  },
);

const interactionsSlice = createSlice({
  name: 'interactions',
  initialState,
  reducers: {
    clearCurrentInteraction: (state) => {
      state.current = undefined;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchInteractions.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchInteractions.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload;
      })
      .addCase(createFormInteraction.pending, (state) => {
        state.submitting = true;
        state.error = undefined;
      })
      .addCase(createFormInteraction.fulfilled, (state, action) => {
        state.submitting = false;
        state.current = action.payload;
        state.items.unshift(action.payload);
      })
      .addCase(createFormInteraction.rejected, (state, action) => {
        state.submitting = false;
        state.error = action.error.message;
      })
      .addCase(createChatInteraction.pending, (state) => {
        state.submitting = true;
        state.error = undefined;
      })
      .addCase(createChatInteraction.fulfilled, (state, action) => {
        state.submitting = false;
        state.current = action.payload;
        state.items.unshift(action.payload);
      })
      .addCase(createChatInteraction.rejected, (state, action) => {
        state.submitting = false;
        state.error = action.error.message;
      });
  },
});

export const { clearCurrentInteraction } = interactionsSlice.actions;
export default interactionsSlice.reducer;
