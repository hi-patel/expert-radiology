# Components
This app will be a single page app with a 50:50 layout.

# Left Panel
This panel will contain search parameters.
- Header: Imaging Center Search
- Body:
  - Parameters Section
    - Single text field for patient address
    - Single text field for target address
    - Multi-select field for different modalities
    - Single select field for minimum rating (out of 5 stars)
    - Checkbox field for "Offers referral bonus"
  - Sorting Section
    - Three rows of multi-select fields. Each field has the same options on what to sort results by:
      - "Distance from patient (lowest first)"
      - "Patient Satisfaction (highest first)"
      - "Referral Bonus (highest first)"
      - "Turnaround time (lowest first)"

# Right Panel
This panel will contain the results as a list.
- Header: Matching Imaging Centers
- Body:
  - List of cards
    - Card header left: Location name
    - Card header right: Patient satisfaction rating
    - Card body: 
      - Address + Distance from patient
      - Modalities served
      - Referral bonus (if any)
      - Patients that were previously referred

