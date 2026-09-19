export interface CitizenAnalysis {
  language: string | null;
  category: string | null;
  intent: string | null;
  issue: string | null;
  location_text: string | null;
}

export interface CitizenRequestResponse {
  id: number;
  anonymous_reference: string;
  raw_text: string;

  language: string | null;
  category: string | null;
  intent: string | null;
  issue: string | null;
  location_text: string | null;

  region_id: number | null;

  latitude: number | null;
  longitude: number | null;

  status: string;
  source: string;
  created_at: string;
}