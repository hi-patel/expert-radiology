# Components
This app will be a single page app with a 50:50 layout.

# Left Panel
This panel will contain search parameters.
- Header: Imaging Center Search
- Body:
  - Parameters Section
    - Single text field for **patient address** (required)
    - Single text field for **target address** (optional; typically the physician's office)
    - Multi-select field for different modalities
    - Single select field for minimum rating (out of 5 stars), with options:
      - "5"
      - "4+"
      - "3+"
      - "2+"
      - "1+"
    - Checkbox field for "Offers referral bonus" (filters strictly to bonus-offering centers when checked)
    - (Future scope) Filter for "Public transit accessibility" using a public transit score
  - Sorting Section
    - Three rows of multi-select fields. Each field has the same options on what to sort results by:
      - "Distance from patient (lowest first)"
      - "Distance from target (lowest first)"
      - "Patient Satisfaction (highest first)"
      - "Referral Bonus (highest first)"
      - "Turnaround time (lowest first)"
- Search controls
  - "Search" button that executes the query
  - Pressing Enter while focused in a text field also triggers search

# Right Panel
This panel will contain the results as a list.
- Header: Matching Imaging Centers
- Body:
  - List of cards
    - Card header left: Location name
    - Card header right:
      - Patient satisfaction rating
      - Review count next to the rating
      - Heart icon to favorite the location (toggle; favorites stored for the physician)
    - Card body: 
      - Address + Distance from patient
      - Distance from target (if a target address was provided)
      - Modalities served
      - Turnaround time
        - Display in hours if < 48, otherwise in days
        - If a location has quick turnaround but low satisfaction, show a warning icon next to the time with tooltip text:
          - "Location shows low satisfaction despite quick turnaround time"
      - Referral bonus (numeric flat dollar amount, if any)
      - Patients that were previously referred
      - (Future scope) Public transit score

