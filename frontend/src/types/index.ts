// Types for our application

export interface ScheduledMessage {
  id?: number;
  message: string;
  channel: string;
  scheduled_time: string;
  status?: string;
  created_at?: string;
  updated_at?: string;
}

export interface ApiResponse<T> {
  data: T;
  status: number;
  message?: string;
}
