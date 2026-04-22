import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import api from '../../services/api';

export interface HCP {
  id: number;
  full_name: string;
  specialty: string;
  hospital_name: string;
  city: string;
  tier: string;
  preferred_channel: string;
  notes?: string;
}

interface HCPState {
  items: HCP[];
  loading: boolean;
}

const initialState: HCPState = {
  items: [],
  loading: false,
};

export const fetchHcps = createAsyncThunk('hcps/fetch', async () => {
  const response = await api.get<HCP[]>('/hcps');
  return response.data;
});

const hcpsSlice = createSlice({
  name: 'hcps',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchHcps.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchHcps.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload;
      })
      .addCase(fetchHcps.rejected, (state) => {
        state.loading = false;
      });
  },
});

export default hcpsSlice.reducer;
