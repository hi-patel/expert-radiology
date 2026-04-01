# Workflows

## Workflow 1: Find imaging centers closest to the patient's home address

**User story**: As a physician, I want to find imaging centers closest to the patient's home address so that I can refer them to a location that is most convenient.

**Step-by-step actions**
1. Physician opens the app and sees the 50:50 layout with the left search panel and right results panel.
2. In the left panel under **Parameters Section**, the physician:
   - Clicks into the **Patient address** text field.
   - Types the patient's home address (e.g., "123 Main St, Springfield").
3. The physician leaves the **Target address** field empty (or at its default) so that distance is computed from the patient’s address only.
4. The physician optionally:
   - Leaves **Modalities** unselected to include all modalities, or selects one/more modalities if the exam type is already known.
   - Sets a **Minimum rating** (e.g., 3 or 4 stars) to avoid low-satisfaction centers.
   - Leaves **Offers referral bonus** unchecked if referral bonus is not relevant to this search.
5. In the **Sorting Section**, the physician configures priorities:
   - In the first sort row, selects **"Distance from patient (lowest first)"**.
   - In the second and third sort rows, optionally selects **"Patient Satisfaction (highest first)"** or other secondary criteria.
6. Physician triggers the search (e.g., by clicking a **Search** button in the left panel or the search is auto-run when fields change).  
   - **Missing detail**: The design does not specify how the search is triggered (button vs. auto-search).
7. The right panel updates **Matching Imaging Centers**:
   - Each card shows location name, satisfaction rating, address, and **Distance from patient**.
8. Physician scans the list, focusing on the top cards (shortest distance from patient) and reviews:
   - Travel distance vs. minimum rating.
   - Modalities served to ensure they match the needed exam.
9. Physician clicks on the most appropriate imaging center card (if cards are clickable) to view more detail or copies the address for the referral.  
   - **Missing detail**: The design does not specify whether cards are clickable or if there is a detail view.

**Open questions / more information needed**
- How is the search explicitly triggered (search button, debounce on change, or on enter key)?
  - Enter button or search button
- Are there any required fields (e.g., must patient address be filled before searching)?
  - Patient address is the only required field
- Is there a map or only a list view for assessing location convenience?
  - Only a list view. Map is future scope.
- Are cards interactive (clickable) or purely informational?
  - Purely informational for now

---

## Workflow 2: Find imaging centers closest to the physician's office

**User story**: As a physician, I want to find imaging centers closest to my office so that the patient can minimize their travel when they need to visit both locations.

**Step-by-step actions**
1. Physician opens the app and views the search form on the left and results list on the right.
2. In the **Parameters Section**:
   - The physician may still fill in **Patient address** if they want to consider both locations, or leave it blank if only office proximity matters.
   - In the **Target address** field, the physician enters their office address (e.g., "456 Clinic Ave, Springfield").
3. The physician:
   - Optionally selects relevant **Modalities** based on the imaging order.
   - Sets a **Minimum rating** to avoid low-quality centers.
   - Keeps **Offers referral bonus** unchecked unless incentives are also a consideration.
4. In the **Sorting Section**, the physician configures:
   - First row: **"Distance from patient (lowest first)"** OR (if supported) a distance-from-target metric.  
     - **Missing detail**: The interface only specifies "Distance from patient", not distance from target/office; unclear how office distance is expressed in sorting.
   - Additional rows for **"Patient Satisfaction (highest first)"** or **"Turnaround time (lowest first)"** as tie-breakers.
5. Physician triggers the search using the app’s search mechanism (button or auto-search).  
   - **Missing detail**: Same as Workflow 1, the trigger mechanism is unspecified.
6. The right panel refreshes **Matching Imaging Centers**:
   - Cards show address and distance from patient; office distance may or may not be visible.  
     - **Missing detail**: The design only mentions "Distance from patient", not distance from office/target.
7. Physician uses the list to identify centers that minimize combined travel (patient home + office), prioritizing:
   - Short travel distance (using whatever distance metric is shown).
   - Sufficient rating and supported modalities.
8. Physician chooses a center from the top of the list and proceeds to write or send the referral.

**Open questions / more information needed**
- How is distance from the physician’s office represented in the UI, or is the target address only used for internal ranking?
  - Add an item to the result card for target address (if provided)
- Can sorting explicitly prioritize distance from the **target address** instead of the patient address?
  - Yes. Add that as an option in the sorting section
- Is there any visual indicator tying a center’s location to both addresses (e.g., relative distances or map)?
  - No, out of scope.

---

## Workflow 3: Find imaging centers with the highest patient satisfaction

**User story**: As a physician, I want to find imaging centers with the highest patient satisfaction so that I can build patient trust in my judgement.

**Step-by-step actions**
1. Physician opens the app and focuses on the left **Parameters Section**.
2. Physician optionally:
   - Enters **Patient address** and/or **Target address** if geographic constraints still matter, or leaves them blank for a broader search region.
3. In **Modalities**, the physician:
   - Selects one or more modalities that match the ordered study (e.g., MRI, CT, X-ray).
4. In **Minimum rating**, the physician:
   - Sets a high threshold (e.g., 4 or 5 stars) to filter out low-satisfaction centers.
5. **Offers referral bonus** is typically left unchecked because the primary goal is satisfaction, not incentives.
6. In the **Sorting Section**, the physician configures:
   - First row: **"Patient Satisfaction (highest first)"**.
   - Second/third rows: optional criteria such as **"Distance from patient (lowest first)"** or **"Turnaround time (lowest first)"**.
7. Physician triggers the search.
8. The right panel **Matching Imaging Centers** updates:
   - Cards show **Patient satisfaction rating** prominently in the header right.
   - Only centers meeting the minimum rating appear.
9. Physician scans the top of the list, reviewing:
   - Satisfaction ratings (highest at the top).
   - Modalities served and distances relative to the patient.
10. Physician selects a high-rating imaging center to recommend to the patient and documents it in the referral workflow outside the app.

**Open questions / more information needed**
- Is the minimum rating filter inclusive (e.g., "4 and above") and how is that communicated?
  - Yes. "5", "4+", "3+", "2+", "1+"
- Is there support for showing review counts or other quality metrics alongside the rating?
  - Good point, add review counts next to the rating.
- Can the physician save or favorite certain high-satisfaction centers for quicker selection in the future?
  - Yes. Add a heart icon to the right of the rating in the header. clicking it should save that location as a favorite.

---

## Workflow 4: Find imaging centers with quicker turnaround times

**User story**: As a physician, I want to find imaging centers with quicker turnaround times so that patients with more serious problems can be taken care of sooner.

**Step-by-step actions**
1. Physician opens the app and navigates to the left panel.
2. In the **Parameters Section**, physician:
   - Enters **Patient address** to ensure results are still reasonably close to the patient.
   - Optionally enters **Target address** (e.g., office) if proximity to the office also matters.
   - Selects required **Modalities** for the urgent case.
   - Sets **Minimum rating** high enough to avoid low-quality centers, even when prioritizing speed.
   - Leaves **Offers referral bonus** unchecked; speed and quality are primary.
3. In the **Sorting Section**, physician configures:
   - First row: **"Turnaround time (lowest first)"**.
   - Second/third rows: **"Distance from patient (lowest first)"** and/or **"Patient Satisfaction (highest first)"**.
4. Physician triggers the search.
5. The **Matching Imaging Centers** list updates:
   - Cards show turnaround time somewhere in the body (though not explicitly specified in the UI spec).  
     - **Missing detail**: Turnaround time is mentioned as a sorting option but not in the card fields.
6. Physician scans the top of the list, focusing on:
   - Shortest turnaround time.
   - Adequate rating and convenient distance.
7. Physician chooses one of the top centers and proceeds with an urgent referral.

**Open questions / more information needed**
- Where is **turnaround time** displayed in the card UI?
  - Let's add it to the body
- What is the unit/scale for turnaround time (hours, days? mean vs 90th percentile)?
  - Data = hours. Display = hours if < 48, otherwise days.
- Does the app surface any warnings for centers with excellent speed but poor satisfaction?
  - Sure. In this case, the turaround time should have a warning icon next to the time. When hovering over the icon, user sees a message indicating "Location shows low satisfaction despite quick turnaround time".

---

## Workflow 5: Find imaging centers that provide the highest referral fees

**User story**: As a physician, I want to find imaging centers that provide the highest referral fees so that I can maximize ROI.

**Step-by-step actions**
1. Physician opens the app and is presented with the search form.
2. In the **Parameters Section**, physician:
   - Enters **Patient address** and/or **Target address** as needed to constrain geography.
   - Selects required **Modalities** to ensure only relevant centers are shown.
   - Sets **Minimum rating** to a baseline level of quality.
   - Checks the **"Offers referral bonus"** checkbox to restrict results to centers that provide referral bonuses.
3. In the **Sorting Section**, physician configures:
   - First row: **"Referral Bonus (highest first)"**.
   - Second row: **"Patient Satisfaction (highest first)"** to avoid prioritizing high bonus but very low satisfaction.
   - Third row: **"Distance from patient (lowest first)"** to keep options reasonably close.
4. Physician triggers the search.
5. The right panel list updates:
   - Each card shows **Referral bonus (if any)** in the body; only centers with bonuses should appear when the checkbox is checked.
6. Physician reviews the top cards:
   - Confirms bonus level and verifies acceptable satisfaction rating and distance.
7. Physician selects a center with a favorable combination of bonus and other metrics and records this choice for the referral.

**Open questions / more information needed**
- Is the referral bonus amount numeric, categorical, or just a yes/no indicator?
  - Numeric (flat dollar amount)
- Does checking **"Offers referral bonus"** filter strictly to bonus-offering centers, or does it also affect sorting?
  - Strictly to bonus-offering centers.
- Are there compliance or disclosure hints in the UI regarding referral incentives?
  - Not in scope.

---

## Workflow 6: Find imaging centers that provide specific modalities

**User story**: As a physician, I want to find imaging centers that provide specific modalities so that I can be sure they can serve my patient.

**Step-by-step actions**
1. Physician opens the app.
2. In the **Parameters Section**, physician:
   - Enters **Patient address** (and optionally **Target address**) to set geographic context.
3. In **Modalities** (multi-select):
   - Physician selects one or more modalities required for the order (e.g., MRI + contrast, CT, Ultrasound).
4. In **Minimum rating**, physician:
   - Sets a preferred threshold for quality.
5. For **Offers referral bonus**, physician:
   - Leaves it unchecked unless incentives matter for this case.
6. In the **Sorting Section**, physician:
   - Prioritizes **"Distance from patient (lowest first)"**.
   - Optionally adds **"Patient Satisfaction (highest first)"** and/or **"Turnaround time (lowest first)"** as secondary criteria.
7. Physician triggers the search.
8. **Matching Imaging Centers** updates:
   - Cards display **Modalities served** in the body.
   - Only centers that match all selected modalities are included (assumed behavior).  
     - **Missing detail**: The matching rule for multi-select modalities is not specified (any vs all).
9. Physician scans the cards at the top of the list to confirm:
   - Required modalities are listed explicitly.
   - Distance and rating are acceptable.
10. Physician chooses a compatible center and proceeds with the referral.

**Open questions / more information needed**
- Do results require centers to support **all** selected modalities or **any** of them?
  - All
- How are modality names normalized between the physician’s selection and the center’s offerings?
  - They both need to pull from the same data set
- Is there a way to favorite or pre-filter to centers the practice typically uses for specific modalities?
  - Not in scope.

---

## Workflow 7: Find imaging centers that accept specific insurance

**User story**: As a physician, I want to find imaging centers that accept specific insurance so that the patient's care can be covered.

**Step-by-step actions**
1. Physician opens the app.
2. In the **Parameters Section**, physician:
   - Enters **Patient address** (required) and optionally **Target address** to set geographic context.
3. In **Modalities** (multi-select), physician:
   - Selects one or more modalities required for the order so that only relevant centers are considered.
4. In **Insurance** (multi-select field):
   - Physician selects one or more insurance plans that the patient has (e.g., "BigHealth PPO", "StateCare Gold").
5. In **Minimum rating**, physician:
   - Sets a preferred quality threshold.
6. For **Offers referral bonus**, physician:
   - Leaves it unchecked or checked depending on whether incentives should further filter eligible centers.
7. In the **Sorting Section**, physician:
   - Prioritizes **"Distance from patient (lowest first)"** or **"Patient Satisfaction (highest first)"** as desired.
8. Physician clicks the **Search** button or presses Enter in a text field to trigger the search.
9. **Matching Imaging Centers** updates:
   - Cards display **Modalities served**, **Referral bonus**, **Turnaround time**, and (implicitly) only those centers that accept at least one of the selected insurance plans.
10. Physician scans the cards to confirm:
   - Selected insurance is accepted for each center.
   - Modalities, distance, and rating meet requirements.
11. Physician chooses a center that meets clinical and coverage needs and proceeds with the referral.

**Open questions / more information needed**
- Should centers be shown if they accept **any** of the selected insurance plans or must they accept **all**?
  - Any.
- How is accepted insurance represented on the card (logos, plan names, both)?
  - Plan names only, as a text list.
- Is there a way to mark certain insurance-center combinations as out-of-network or partially covered?
  - Not in scope.

---

## Future Workflow 8: Find imaging centers that are most publicly accessible

**User story (future scope)**: As a physician, I want to find imaging centers that are most publicly accessible so that patients can use public transportation to travel to their appointment.

**Step-by-step actions** (hypothetical, based on current UI)
1. Physician opens the app and goes to the search panel.
2. Physician enters **Patient address** to identify feasible travel routes via public transport.
3. Physician may enter **Target address** (e.g., hospital or clinic) if patients might travel between both locations.
4. Physician selects required **Modalities** and sets a **Minimum rating**.
5. Ideally, there would be:
   - A new **"Public transit accessibility"** parameter (filter) and/or
   - A sort option such as **"Public accessibility (highest first)"**.  
     - **Missing detail**: This parameter is not present in the current interface specification.
6. Physician triggers the search.
7. **Matching Imaging Centers** list would display some public transit–related field on each card (e.g., nearest stop, transit score).  
   - **Missing detail**: Card layout does not currently include any public accessibility info.
8. Physician chooses centers with the best combination of accessibility, modality support, and rating.

**Open questions / more information needed**
- How is "public accessibility" represented in data (transit score, walking distance to nearest stop, number of lines, etc.)?
  - Public transit score.
- Will there be additional UI elements (map overlays, transit icons) to make this visible?
  - No.
- Is public accessibility a filter, a sort option, or both?
  - Filter.

