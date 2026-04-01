"use client";

import { useEffect, useMemo, useState } from "react";
import type {
  ImagingCenter,
  InsurancePlan,
  Modality,
  SearchRequest,
  SortOption,
} from "../lib/api";
import { fetchInsurancePlans, fetchModalities, searchImagingCenters } from "../lib/api";

type RatingOption = "5" | "4+" | "3+" | "2+" | "1+";

const ratingToMinimum = (value: RatingOption | ""): number | undefined => {
  if (!value) return undefined;
  if (value === "5") return 5;
  return Number.parseInt(value[0], 10);
};

const sortOptions: { value: SortOption; label: string }[] = [
  { value: "distance_from_patient_asc", label: "Distance from patient (lowest first)" },
  { value: "distance_from_target_asc", label: "Distance from target (lowest first)" },
  { value: "patient_satisfaction_desc", label: "Patient Satisfaction (highest first)" },
  { value: "turnaround_time_asc", label: "Turnaround time (lowest first)" },
  { value: "referral_bonus_desc", label: "Referral Bonus (highest first)" },
];

const Home = () => {
  const [patientAddress, setPatientAddress] = useState("");
  const [targetAddress, setTargetAddress] = useState("");
  const [selectedModalities, setSelectedModalities] = useState<number[]>([]);
  const [selectedInsurancePlans, setSelectedInsurancePlans] = useState<number[]>([]);
  const [minimumRating, setMinimumRating] = useState<RatingOption | "">("4+");
  const [requiresReferralBonus, setRequiresReferralBonus] = useState(false);
  const [minimumTransitScore, setMinimumTransitScore] = useState<number | "">("");
  const [sortSelections, setSortSelections] = useState<(SortOption | "")[]>([
    "distance_from_patient_asc",
    "patient_satisfaction_desc",
    "",
  ]);

  const [modalities, setModalities] = useState<Modality[]>([]);
  const [insurancePlans, setInsurancePlans] = useState<InsurancePlan[]>([]);
  const [centers, setCenters] = useState<ImagingCenter[]>([]);
  const [favorites, setFavorites] = useState<Set<number>>(new Set());
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hasSearched, setHasSearched] = useState(false);

  console.log("pre useEffect");

  useEffect(() => {
    console.log("useEffect: loading reference data");

    const loadReferenceData = async () => {
      try {
        const [mods, plans] = await Promise.all([fetchModalities(), fetchInsurancePlans()]);
        setModalities(mods);
        setInsurancePlans(plans);
      } catch (err) {
        setError("Failed to load reference data. Please try again.");
      }
    };

    void loadReferenceData();
  }, []);

  const handleToggleFavorite = (id: number) => {
    setFavorites((prev) => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  };

  const handleSearch = async () => {
    setError(null);
    setHasSearched(true);

    if (!patientAddress.trim()) {
      setError("Patient address is required.");
      return;
    }

    const sort: SortOption[] = sortSelections.filter(Boolean) as SortOption[];
    const request: SearchRequest = {
      patientAddress,
      targetAddress: targetAddress || undefined,
      modalityIds: selectedModalities,
      insurancePlanIds: selectedInsurancePlans,
      minimumRating: ratingToMinimum(minimumRating),
      requiresReferralBonus,
      minimumPublicTransitScore:
        typeof minimumTransitScore === "number" ? minimumTransitScore : undefined,
      sort,
    };

    try {
      setIsLoading(true);
      const results = await searchImagingCenters(request);
      setCenters(results);
    } catch (err) {
      setError("Search failed. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const ratingLabel = (center: ImagingCenter) => {
    const raw = center.patient_satisfaction_rating;
    const ratingNumber =
      typeof raw === "number" ? raw : Number.parseFloat(raw ?? "0");
    return `${ratingNumber.toFixed(1)} (${center.review_count})`;
  };

  const turnaroundLabel = (hoursRaw: number | string) => {
    const hours =
      typeof hoursRaw === "number" ? hoursRaw : Number.parseFloat(hoursRaw ?? "0");
    if (hours < 48) {
      return `${hours}h`;
    }
    const days = Math.round(hours / 24);
    return `${days}d`;
  };

  const shouldShowTurnaroundWarning = (center: ImagingCenter) => {
    const hoursRaw = center.average_turnaround_hours;
    const hours =
      typeof hoursRaw === "number" ? hoursRaw : Number.parseFloat(hoursRaw ?? "0");
    const ratingRaw = center.patient_satisfaction_rating;
    const rating =
      typeof ratingRaw === "number" ? ratingRaw : Number.parseFloat(ratingRaw ?? "0");
    return hours <= 24 && rating < 3.0;
  };

  const sortedSortOptionsForRow = (rowIndex: number) =>
    sortOptions.filter(
      (opt) =>
        !sortSelections.some(
          (value, idx) => idx !== rowIndex && value === opt.value,
        ),
    );

  const hasResults = centers.length > 0;

  const favoriteIds = useMemo(() => new Set(favorites), [favorites]);

  return (
    <div className="flex min-h-screen flex-col bg-zinc-50 text-zinc-900">
      <header className="border-b border-zinc-200 bg-white px-6 py-4">
        <h1 className="text-xl font-semibold tracking-tight">Imaging Center Directory</h1>
        <p className="mt-1 text-sm text-zinc-600">
          Find the best imaging centers for your patients based on distance, quality, speed, and
          incentives.
        </p>
      </header>

      <main className="flex flex-1 flex-col gap-0 overflow-hidden lg:flex-row">
        {/* Left panel: parameters + sorting */}
        <section className="w-full border-b border-zinc-200 bg-white px-6 py-4 lg:h-[calc(100vh-4rem)] lg:w-1/2 lg:border-b-0 lg:border-r lg:overflow-y-auto">
          <div className="space-y-6">
            <div>
              <h2 className="text-sm font-semibold uppercase tracking-wide text-zinc-500">
                Parameters
              </h2>
              <div className="mt-3 space-y-3">
                <div>
                  <label className="text-xs font-medium text-zinc-700">
                    Patient address <span className="text-red-500">*</span>
                  </label>
                  <input
                    className="mt-1 w-full rounded-md border border-zinc-300 px-3 py-2 text-sm shadow-sm focus:border-zinc-900 focus:outline-none focus:ring-1 focus:ring-zinc-900"
                    placeholder="123 Main St, Springfield"
                    value={patientAddress}
                    onChange={(event) => setPatientAddress(event.target.value)}
                    onKeyDown={(event) => {
                      if (event.key === "Enter") {
                        void handleSearch();
                      }
                    }}
                  />
                </div>

                <div>
                  <label className="text-xs font-medium text-zinc-700">Target address</label>
                  <input
                    className="mt-1 w-full rounded-md border border-zinc-300 px-3 py-2 text-sm shadow-sm focus:border-zinc-900 focus:outline-none focus:ring-1 focus:ring-zinc-900"
                    placeholder="456 Clinic Ave, Springfield"
                    value={targetAddress}
                    onChange={(event) => setTargetAddress(event.target.value)}
                    onKeyDown={(event) => {
                      if (event.key === "Enter") {
                        void handleSearch();
                      }
                    }}
                  />
                </div>

                <div>
                  <label className="text-xs font-medium text-zinc-700">Modalities</label>
                  <div className="mt-1 flex flex-wrap gap-2">
                    {modalities.map((modality) => {
                      const active = selectedModalities.includes(modality.id);
                      return (
                        <button
                          key={modality.id}
                          type="button"
                          className={`rounded-full border px-3 py-1 text-xs ${
                            active
                              ? "border-zinc-900 bg-zinc-900 text-white"
                              : "border-zinc-300 bg-white text-zinc-800"
                          }`}
                          onClick={() => {
                            setSelectedModalities((prev) =>
                              prev.includes(modality.id)
                                ? prev.filter((id) => id !== modality.id)
                                : [...prev, modality.id],
                            );
                          }}
                        >
                          {modality.name}
                        </button>
                      );
                    })}
                  </div>
                </div>

                <div>
                  <label className="text-xs font-medium text-zinc-700">Insurance</label>
                  <div className="mt-1 flex max-h-32 flex-wrap gap-2 overflow-y-auto">
                    {insurancePlans.map((plan) => {
                      const active = selectedInsurancePlans.includes(plan.id);
                      return (
                        <button
                          key={plan.id}
                          type="button"
                          className={`rounded-full border px-3 py-1 text-xs ${
                            active
                              ? "border-zinc-900 bg-zinc-900 text-white"
                              : "border-zinc-300 bg-white text-zinc-800"
                          }`}
                          onClick={() => {
                            setSelectedInsurancePlans((prev) =>
                              prev.includes(plan.id)
                                ? prev.filter((id) => id !== plan.id)
                                : [...prev, plan.id],
                            );
                          }}
                        >
                          {plan.name}
                        </button>
                      );
                    })}
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <div className="flex-1">
                    <label className="text-xs font-medium text-zinc-700">Minimum rating</label>
                    <select
                      className="mt-1 w-full rounded-md border border-zinc-300 bg-white px-3 py-2 text-sm shadow-sm focus:border-zinc-900 focus:outline-none focus:ring-1 focus:ring-zinc-900"
                      value={minimumRating}
                      onChange={(event) =>
                        setMinimumRating(event.target.value as RatingOption | "")
                      }
                    >
                      <option value="">Any</option>
                      <option value="5">5</option>
                      <option value="4+">4+</option>
                      <option value="3+">3+</option>
                      <option value="2+">2+</option>
                      <option value="1+">1+</option>
                    </select>
                  </div>

                  <div className="flex-1">
                    <label className="text-xs font-medium text-zinc-700">
                      Public transit score (min)
                    </label>
                    <input
                      type="number"
                      min={0}
                      max={100}
                      className="mt-1 w-full rounded-md border border-zinc-300 px-3 py-2 text-sm shadow-sm focus:border-zinc-900 focus:outline-none focus:ring-1 focus:ring-zinc-900"
                      value={minimumTransitScore}
                      onChange={(event) => {
                        const value = event.target.value;
                        setMinimumTransitScore(value === "" ? "" : Number(value));
                      }}
                    />
                  </div>
                </div>

                <label className="inline-flex items-center gap-2 text-xs font-medium text-zinc-700">
                  <input
                    type="checkbox"
                    className="h-4 w-4 rounded border-zinc-300 text-zinc-900 focus:ring-zinc-900"
                    checked={requiresReferralBonus}
                    onChange={(event) => setRequiresReferralBonus(event.target.checked)}
                  />
                  Offers referral bonus only
                </label>
              </div>
            </div>

            <div>
              <h2 className="text-sm font-semibold uppercase tracking-wide text-zinc-500">
                Sorting
              </h2>
              <div className="mt-3 space-y-2">
                {sortSelections.map((selected, index) => (
                  <select
                    key={index}
                    className="w-full rounded-md border border-zinc-300 bg-white px-3 py-2 text-sm shadow-sm focus:border-zinc-900 focus:outline-none focus:ring-1 focus:ring-zinc-900"
                    value={selected}
                    onChange={(event) => {
                      const value = event.target.value as SortOption | "";
                      setSortSelections((prev) => {
                        const next = [...prev];
                        next[index] = value;
                        return next;
                      });
                    }}
                  >
                    <option value="">None</option>
                    {sortedSortOptionsForRow(index).map((option) => (
                      <option key={option.value} value={option.value}>
                        {option.label}
                      </option>
                    ))}
                  </select>
                ))}
              </div>
            </div>

            <div className="flex items-center justify-between gap-3">
              <button
                type="button"
                className="inline-flex items-center justify-center rounded-md bg-zinc-900 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-zinc-800 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-zinc-900 focus-visible:ring-offset-2"
                onClick={() => {
                  void handleSearch();
                }}
              >
                {isLoading ? "Searching..." : "Search"}
              </button>
              <p className="text-xs text-zinc-500">
                Press Enter in an address field to search.
              </p>
            </div>

            {error && (
              <p className="text-sm text-red-600" role="alert">
                {error}
              </p>
            )}
          </div>
        </section>

        {/* Right panel: results */}
        <section className="w-full bg-zinc-50 px-6 py-4 lg:h-[calc(100vh-4rem)] lg:w-1/2 lg:overflow-y-auto">
          <h2 className="text-sm font-semibold uppercase tracking-wide text-zinc-500">
            Matching Imaging Centers
          </h2>

          {isLoading && !hasResults ? (
            <p className="mt-4 text-sm text-zinc-500">Searching...</p>
          ) : null}

          {!isLoading && hasSearched && !hasResults ? (
            <p className="mt-4 text-sm text-zinc-500">
              No imaging centers match the current filters.
            </p>
          ) : null}

          <div className="mt-4 space-y-4">
            {centers.map((center) => {
              const isFavorite = favoriteIds.has(center.id);
              const modalitiesLabel = center.modalities.map((m) => m.name).join(", ");
              const plansLabel = center.insurance_plans.map((p) => p.name);
              const maxPlansToShow = 3;
              const primaryPlans = plansLabel.slice(0, maxPlansToShow);
              const remaining = plansLabel.length - primaryPlans.length;

              return (
                <article
                  key={center.id}
                  className="rounded-lg border border-zinc-200 bg-white p-4 shadow-sm"
                >
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <h3 className="text-sm font-semibold text-zinc-900">{center.name}</h3>
                      <p className="mt-1 text-xs text-zinc-600">
                        {center.address_line_1}
                        {center.address_line_2 ? `, ${center.address_line_2}` : ""}
                        <br />
                        {center.city}, {center.state} {center.postal_code}
                      </p>
                    </div>
                    <div className="flex flex-col items-end gap-1">
                      <button
                        type="button"
                        aria-label={isFavorite ? "Remove from favorites" : "Add to favorites"}
                        className={`flex h-6 w-6 items-center justify-center rounded-full border text-xs ${
                          isFavorite
                            ? "border-red-500 bg-red-500 text-white"
                            : "border-zinc-300 bg-white text-zinc-600"
                        }`}
                        onClick={() => handleToggleFavorite(center.id)}
                      >
                        {isFavorite ? "♥" : "♡"}
                      </button>
                      <span className="text-xs font-medium text-zinc-800">
                        {ratingLabel(center)}
                      </span>
                    </div>
                  </div>

                  <div className="mt-3 grid grid-cols-1 gap-2 text-xs text-zinc-700 md:grid-cols-2">
                    <div>
                      <span className="font-medium">Distance from patient: </span>
                      {center.distance_from_patient_km != null
                        ? `${center.distance_from_patient_km.toFixed(1)} km`
                        : "N/A"}
                    </div>
                    {targetAddress && (
                      <div>
                        <span className="font-medium">Distance from target: </span>
                        {center.distance_from_target_km != null
                          ? `${center.distance_from_target_km.toFixed(1)} km`
                          : "N/A"}
                      </div>
                    )}
                    <div>
                      <span className="font-medium">Modalities: </span>
                      {modalitiesLabel || "N/A"}
                    </div>
                    <div>
                      <span className="font-medium">Insurance: </span>
                      {primaryPlans.join(", ")}
                      {remaining > 0 ? ` +${remaining} more` : null}
                    </div>
                    <div className="flex items-center gap-1">
                      <span className="font-medium">Turnaround: </span>
                      <span>{turnaroundLabel(center.average_turnaround_hours)}</span>
                      {shouldShowTurnaroundWarning(center) && (
                        <span
                          className="ml-1 cursor-default text-amber-500"
                          title="Location shows low satisfaction despite quick turnaround time"
                        >
                          !
                        </span>
                      )}
                    </div>
                    <div>
                      <span className="font-medium">Referral bonus: </span>
                      {center.referral_bonus_amount
                        ? `$${center.referral_bonus_amount}`
                        : requiresReferralBonus
                          ? "N/A"
                          : "None"}
                    </div>
                    {center.public_transit_score != null && (
                      <div>
                        <span className="font-medium">Transit score: </span>
                        {center.public_transit_score}
                      </div>
                    )}
                  </div>
                </article>
              );
            })}
          </div>
        </section>
      </main>
    </div>
  );
};

export default Home;
