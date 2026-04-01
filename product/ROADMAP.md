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

**Time Estimate**: 30 days of dedication observation and feedback. This would be an ongoing task for the life of the platform.

# 1.2 - AI-powered suggestions
We will collect data on what search parameters are being used and in what combinations to train an AI model to make suggestions to other users. The AI can be an assistant to make sure the physician is using as many search parameters as possible and using them correctly. We will also train the AI to suggest search parameters based on what the physician is trying to accomplish. If can access the patient chart, we can also use AI to suggest search parameters based on the patient's preferences. If we are allowed to aggregate data across all of our physicians, we can train the AI to suggest parameters based on what works well for their physicians.

**Time Estimate**: Ship a limited strategy within 4-6 weeks (e.g. an AI agent that helps maximize ROI). If done properly, additional strategies should be deployable within 2-3 weeks each.

# Phase 2 - Automation
# 2.1 - Human In the Loop Automation
Instead of a an empty search form with results, we will being pre-populating the search form with parameters (probably based on AI) and we will show a Top 3 matches in the results with a highlight on the one we most recommend. The user can choose one of the suggested results or expand the search and choose something else. We take the results and adapt the Top 3 matches logic until we get physicians consistently choosing results from our suggestions.

**Time estimate**: 4-6 weeks.

# 2.2 - Full Automation
We incorporate imaging center matching directly into physician's clinical workflows. Physician puts in an order for a radiology appointment and we use the Top 3 matching logic to automatically pick an imaging center.

**Time estimate**: 3+ months depending on the EHR integration.

# Other Features - Not Phase Specific
- Vendor integrations. Have the ability to import imaging centers from third-party vendors instead of maintaining our own list.
- AI-powered imaging center prioritization. Over time, we may see a small subset of imaging centers dominating the results and would make it harder for other centers to get business. We can use AI to help re-prioritize results to help those other centers.
- A map for visual cues.
- Patient Facing platform
- Sponsored listings with ad tech concepts (real-time bidding, competitive exclusion, etc)

# Definition of Success
80% of physicians in our network are using full automation. 80% of all patients in a partner location are being scheduled to imaging centers based on suggetions from our platform.


# Risks/Concerns
- Most physicians or practices will have a limited subset of imaging centers that they work with. It can be either personal relationships or business relationships. If the number of physicians/locations with partnerships like this are high, the platform is useless.
- The cost of implementing AI may not be worth the benefits in this workflow. We might be able to solve the problem with traditional means.
- Too many parameters can become unwieldy
