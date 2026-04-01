export type SortOption =
  | "distance_from_patient_asc"
  | "distance_from_target_asc"
  | "patient_satisfaction_desc"
  | "turnaround_time_asc"
  | "referral_bonus_desc";

export type SearchRequest = {
  patientAddress: string;
  targetAddress?: string;
  modalityIds: number[];
  insurancePlanIds: number[];
  minimumRating?: number;
  requiresReferralBonus?: boolean;
  minimumPublicTransitScore?: number;
  sort: SortOption[];
};

export type Modality = {
  id: number;
  name: string;
};

export type InsurancePlan = {
  id: number;
  name: string;
};

export type ImagingCenter = {
  id: number;
  name: string;
  address_line_1: string;
  address_line_2: string;
  city: string;
  state: string;
  postal_code: string;
  latitude: number | null;
  longitude: number | null;
  // DRF serialises DecimalFields as strings; accept both.
  patient_satisfaction_rating: number | string;
  review_count: number;
  referral_bonus_amount: string | null;
  distance_from_patient_km: number | null;
  distance_from_target_km: number | null;
  average_turnaround_hours: number | string;
  patients_previously_referred: number;
  public_transit_score: number | string | null;
  modalities: Modality[];
  insurance_plans: InsurancePlan[];
};

const API_BASE =
  // In dev, point explicitly at the Docker/nginx stack (localhost:8080).
  // In the production-like nginx stack, NEXT_PUBLIC_API_BASE_URL will be unset
  // so the app will use same-origin (empty string here).
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "";

async function fetchJson<TResponse>(path: string, init?: RequestInit): Promise<TResponse> {
  const url = `${API_BASE}${path}`;

  const response = await fetch(url, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || "Request failed");
  }

  return (await response.json()) as TResponse;
}

export async function fetchModalities(): Promise<Modality[]> {
  return fetchJson<Modality[]>("/api/modalities/");
}

export async function fetchInsurancePlans(): Promise<InsurancePlan[]> {
  return fetchJson<InsurancePlan[]>("/api/insurance-plans/");
}

export async function searchImagingCenters(request: SearchRequest): Promise<ImagingCenter[]> {
  const body = {
    patient_address: request.patientAddress,
    target_address: request.targetAddress ?? "",
    modality_ids: request.modalityIds,
    insurance_plan_ids: request.insurancePlanIds,
    minimum_rating: request.minimumRating ?? null,
    requires_referral_bonus: request.requiresReferralBonus ?? false,
    minimum_public_transit_score: request.minimumPublicTransitScore ?? null,
    sort: request.sort,
  };

  return fetchJson<ImagingCenter[]>("/api/imaging-centers/", {
    method: "POST",
    body: JSON.stringify(body),
  });
}

