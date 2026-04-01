# Roadmap

## Current State
Imaging Center search using a manual search process with limited parameters:
- Patient Location
- Target Location
- Modalities
- Insurance
- Patient Ratings
- Transit Score
- Referral Bonuses

Multi-parameter sorting will allow users to rank imaging centers based on parameters they find most valuable.

## Long Term Goal
Fully automated within normal day-to-day workflow. Patient chart should have information about the patient's problem and preferences. The system should have revenue information, which we can use to calculate financial data points for each imaging center. Ideally, physician puts in an order for Radiology Appointment Request and signs it. Behind the scenes, the request gets routed using the parameters above to the best-fit imaging center for scheduling.

# General Plan
The goal of this feature is to recommend imaging centers that bring the most value to the physician. "Value" can mean different things to different physicians so during Phase 1, we need to build a framework with the flexibility to allow physicians to define their "value". In phase 2, we collect the data from their usage to create pre-defined automation strategies (e.g. "Referral Strategy: Maximize ROI", "Referral Strategy: Maximize Patient Success", etc). Once configured, the physician just needs to decide if an appointment is needed (yes/no) and the platform takes care of the rest.

# Phase 1 - Manual Workflows

# 1.1 - Parameter Definitions
During this step, we'll research and define all parameters that are taken into consideration when a physician is choosing an Imaging Center for their patients. These parameters will be incorporated into the Search utility

# 1.2 - AI-powered suggestions
We will collect data on what search parameters are being used and in what combinations to train an AI model to make suggestions to other users. The AI can be an assistant to make sure the physician is using as many search parameters as possible and using them correctly. We will also train the AI to suggest search parameters based on what the physician is trying to accomplish. If can access the patient chart, we can also use AI to suggest search parameters based on the patient's preferences. If we are allowed to aggregate data across all of our physicians, we can train the AI to suggest parameters based on what works well for their physicians.

# Phase 2 - Automation
# 2.1 - Human In the Loop Automation
Instead of a an empty search form with results, we will being pre-populating the search form with parameters (probably based on AI) and we will show a Top 3 matches in the results with a highlight on the one we most recommend. The user can choose one of the suggested results or expand the search and choose something else. We take the results and adapt the Top 3 matches logic until we get physicians consistently choosing results from our suggestions.

# 2.2 - Full Automation
We incorporate imaging center matching directly into physician's clinical workflows. Physician puts in an order for a radiology appointment and we use the Top 3 matching logic to automatically pick an imaging center.

# Definition of Success
80% of physicians in our network are using full automation. 80% of all patients in a partner location are being scheduled to imaging centers based on suggetions from our platform.
