# Customer Segmentation & Churn Pattern Analytics in European Banking: A Quantitative Diagnosis of Deposit Attrition Risk Across France, Germany, and Spain

**Author:** Principal Quantitative Banking Analyst & Financial Econometrician
**Classification:** Internal Research — Retail Banking Risk & Retention Analytics
**Dataset:** n = 10,000 retail accounts (France, Germany, Spain)

---

## 1. Abstract & Problem Formulation

### 1.1 Abstract

This study presents a comprehensive econometric and exploratory analysis of customer attrition across a 10,000-account retail banking portfolio spanning three Eurozone jurisdictions — France, Germany, and Spain. The portfolio carries a total deposited balance of **€764,858,892.88**, of which **7,963 accounts (79.63%)** remain retained and **2,037 accounts (20.37%)** have churned, establishing a **baseline portfolio churn rate of 20.37%**. Critically, the capital-weighted impact of attrition substantially exceeds the headcount-weighted rate: **€185,588,094.63** in deposits — **24.26% of the total ledger** — exited the bank alongside departing customers. This divergence between the 20.37% account-level churn rate and the 24.26% balance-level attrition rate is the paper's central empirical anchor, indicating that the bank is disproportionately losing **higher-balance relationships**, a pattern with direct implications for Net Interest Margin (NIM) compression and Customer Lifetime Value (CLV) decay.

The analysis identifies four primary attrition vectors: (i) acute geographic concentration of risk in Germany, where churn reaches 32.44% against a portfolio-wide average of 20.37%; (ii) a pronounced age-cohort effect, with the 46–60 pre-retirement segment exhibiting a 51.12% churn rate — roughly 2.5x the baseline; (iii) a non-monotonic "multi-product saturation paradox," wherein two-product relationships are the most stable configuration (7.58% churn) while three- and four-product relationships churn at 82.71% and 100.00% respectively; and (iv) an engagement-balance interaction in which active membership reduces churn by 12.58 percentage points, while credit card possession — conventionally assumed to be a retention instrument — shows no meaningful protective effect (20.18% vs. 20.81%).

### 1.2 Problem Formulation: Liquidity Risk, CLV Decay, and Regulatory Context

**Liquidity Risk Transmission.** Retail deposits constitute a primary funding source under Basel III's Liquidity Coverage Ratio (LCR) and Net Stable Funding Ratio (NSFR) frameworks. Deposit attrition is not merely a commercial metric — it is a liquidity event. A loss of €185.59M in deposits, concentrated disproportionately in a single jurisdiction (Germany, at 52.79% of all lost balance), represents a funding-stability shock that a purely headcount-based churn KPI would understate by roughly 4 percentage points (20.37% vs. 24.26%). Under the EBA's guidelines on liquidity stress testing, such concentration risk in "less stable" retail deposits should be explicitly modeled in the bank's Internal Liquidity Adequacy Assessment Process (ILAAP).

**CLV Decay Framework.** We treat churn not as a binary terminal event but as the observable endpoint of a latent CLV decay process, where declining product engagement, wealth-stage transitions, and geographic servicing gaps erode the expected discounted value of a customer relationship prior to formal exit. The multi-product paradox described below is best understood through this lens: rather than being causally protective, product count acts as a *revealed marker* of relationship depth and prior engagement quality, with over-saturation (3–4 products) plausibly proxying for distressed cross-sell (forced bundling, mis-selling remediation, or complaint-driven relationship exits) rather than genuine loyalty.

**ECB & Regulatory Implications.** Under the ECB's Single Supervisory Mechanism (SSM) and the broader SREP (Supervisory Review and Evaluation Process), material adverse trends in deposit stability by jurisdiction can affect a bank's business model viability score and capital planning buffers. The German subsidiary/branch network's 32.44% churn rate — more than 1.5x the portfolio average — and its 1.59 Geographic Risk Index (GRI, defined in §2) would likely warrant disclosure as a concentration risk in Pillar 3 reporting and should inform country-specific stress scenarios in the bank's recovery planning.

---

## 2. Methodology & Feature Engineering

### 2.1 Data Structure

The analytical base table comprises 10,000 unique customer-account records with the following core fields: geography (France, Germany, Spain), age, gender, tenure, account balance, number of products held, credit card flag (`HasCrCard`), active membership flag (`IsActiveMember`), estimated income, credit score, and the binary outcome `Exited` (1 = churned, 0 = retained).

### 2.2 Binning & Segmentation Definitions

To convert continuous variables into economically interpretable cohorts, the following binning schema was applied uniformly across all downstream cross-tabulations:

| Feature | Bin / Tier | Definition Logic |
|---|---|---|
| **Age** | Under 30 | Early-career / low-asset accumulation phase |
| | 30–45 | Core working-age / mortgage & family formation phase |
| | 46–60 | Pre-retirement / peak-asset, wealth-consolidation phase |
| | 60+ | Retirement / decumulation phase |
| **Balance Segment** | Zero-Balance | Balance = €0 (dormant or offset/overdraft-linked accounts) |
| | Funded | Balance > €0 (active deposit-holding accounts) |
| **Product Depth** | 1 Product | Single relationship anchor (typically current/checking account) |
| | 2 Products | Cross-sold relationship (checking + savings/card/loan) |
| | 3 Products | Deep bundled relationship |
| | 4 Products | Maximum observed bundling depth |
| **Engagement** | Active Member | `IsActiveMember` = 1 (self-reported/behaviorally confirmed engagement) |
| | Inactive Member | `IsActiveMember` = 0 |
| **Geography** | France / Germany / Spain | Jurisdiction of primary account domicile |

### 2.3 The Geographic Risk Index (GRI)

To normalize cross-country comparison and isolate jurisdictions that contribute disproportionately to capital loss relative to their share of the portfolio, we define:

**GRI_i = (Share of Lost Balance)_i / (Share of Total Accounts)_i**

A GRI of 1.00 indicates a country's contribution to capital loss is exactly proportional to its account share (i.e., no excess risk concentration). GRI > 1.00 indicates disproportionate capital-risk concentration; GRI < 1.00 indicates the country is "under-contributing" to loss relative to its footprint.

### 2.4 Core Portfolio Identity

$$\text{Total Deposited Portfolio} = €764{,}858{,}892.88 \quad | \quad n = 10{,}000$$
$$\text{Churn Rate (headcount)} = \frac{2{,}037}{10{,}000} = 20.37\%$$
$$\text{Capital-at-Risk Rate (balance-weighted)} = \frac{€185{,}588{,}094.63}{€764{,}858{,}892.88} = 24.26\%$$

The **4.26-point wedge** between the headcount churn rate (20.37%) and the balance-weighted attrition rate (24.26%) is the paper's key severity-adjustment finding: departing customers hold, on average, higher balances than the portfolio mean (implied average lost balance per churned account ≈ €91,109, versus a portfolio-wide average balance per account of ≈ €76,486).

---

## 3. Exploratory & Econometric Findings

### 3.1 Geographic Cross-Tabulation

| Country | Accounts | Churned | Churn Rate | Total Deposits | Lost Balance | % of All Lost Balance | GRI |
|---|---|---|---|---|---|---|---|
| **Germany** | 2,509 | 814 | **32.44%** | €300.40M | **€97.97M** | **52.79%** | **1.59** |
| France | 5,014 | 810 | 16.15% | — | €57.67M | 31.08%* | 0.79 |
| Spain | 2,477 | 413 | 16.67% | — | €29.95M | 16.14%* | 0.82 |
| **Total** | **10,000** | **2,037** | **20.37%** | **€764.86M** | **€185.59M** | **100.00%** | **1.00** |

*\*Derived: France and Spain lost-balance shares computed as remainder against Germany's 52.79% to sum to 100.00% of €185.59M.*

**Interpretation.** Germany holds only **25.09%** of total accounts (2,509 / 10,000) yet accounts for **52.79%** of all lost deposit balance — a GRI of 1.59, meaning German attrition is generating capital loss at roughly **59% above** its proportional footprint. France, despite having the largest account base (5,014, or 50.14% of the portfolio), contributes a GRI of only 0.79, indicating relative stability. Spain sits close to parity (GRI 0.82). This is the single most consequential structural finding in the dataset: **the churn problem is not a pan-European phenomenon — it is substantially a German phenomenon.**

### 3.2 Age Cohort Cross-Tabulation

| Age Band | Accounts | Churned | Churn Rate | Lost Balance | Relative to Baseline (20.37%) |
|---|---|---|---|---|---|
| Under 30 | 1,641 | ~124 | 7.56% | €12.45M | −12.81 pts (0.37x baseline) |
| 30–45 | 6,248 | ~956 | 15.30% | €87.40M | −5.07 pts (0.75x baseline) |
| **46–60** | **1,647** | **842** | **51.12%** | **€75.17M** | **+30.75 pts (2.51x baseline)** |
| 60+ | 464 | ~115 | 24.78% | €10.57M | +4.41 pts (1.22x baseline) |

**Interpretation.** The 46–60 cohort is a statistical outlier of severe magnitude: at 1,647 accounts (16.47% of the portfolio), it produces 842 of the 2,037 total churn events — **41.3% of all churned accounts** despite representing only one-sixth of the customer base. Its churn rate of 51.12% means that this cohort is, in effect, a coin-flip population from a retention standpoint. Combined with €75.17M in lost balance (40.5% of total lost balance), this cohort represents the single highest-priority intervention target in the portfolio — a "pre-retirement wealth drain" addressed in detail in §4.2.

### 3.3 Gender Disparity

| Gender | Churned (n) | Churn Rate | Delta vs. Baseline |
|---|---|---|---|
| Female | 1,139 | **25.07%** | +4.70 pts |
| Male | 898 | 16.46% | −3.91 pts |

**Interpretation.** Female-held accounts churn at a rate **1.52x** that of male-held accounts, an 8.61-point absolute gap. Given the dataset does not include income-parity or product-eligibility controls, this differential should be treated as a flagged disparity for further multivariate investigation (e.g., logistic regression controlling for age, balance, and product count) rather than asserted as a direct causal gender effect. However, given its magnitude, it warrants immediate inclusion as a covariate in any propensity-to-churn scoring model.

### 3.4 Multi-Product Saturation Paradox

| Product Count | Accounts | Churned | Churn Rate | Lost Balance |
|---|---|---|---|---|
| 1 Product | 5,084 | ~1,409 | 27.71% | €129.67M |
| **2 Products** | **4,590** | **~348** | **7.58%** | **€31.41M** |
| 3 Products | 266 | 220 | 82.71% | €18.89M |
| 4 Products | 60 | 60 | **100.00%** | €5.62M |

**Interpretation.** The relationship between product depth and retention is sharply non-monotonic. Two-product relationships are the retention "sweet spot," churning at less than one-third the rate of single-product relationships (7.58% vs. 27.71%). Beyond two products, however, churn accelerates catastrophically: three-product accounts churn at 82.71%, and **every single 4-product account in the dataset has exited (100.00%, n=60)**. This pattern is inconsistent with a simple "more products = more loyalty" model and is addressed as the paper's central strategic puzzle in §4.3 and §5.1.

### 3.5 Engagement & Account Funding Cross-Tabulation

| Segment | Churn Rate | Contrast |
|---|---|---|
| Active Member | 14.27% | Baseline reference |
| Inactive Member | 26.85% | **+12.58 pts** ("Activity Penalty") |
| Has Credit Card | 20.18% | — |
| No Credit Card | 20.81% | **−0.63 pts (statistically negligible)** |
| Funded (Balance > €0) | 24.08% | — |
| Zero-Balance | 13.82% | **−10.26 pts vs. Funded** |

**Interpretation.** Three distinct findings emerge:

1. **Activity is the strongest low-cost retention lever available.** The 12.58-point spread between active and inactive members is larger than the effect of holding a credit card, and is achievable through engagement-nudge campaigns (app logins, transaction frequency) rather than costly product bundling.
2. **Credit card possession confers no meaningful retention barrier** (a 0.63-point gap is within normal sampling noise for this population size). This directly contradicts the common retail-banking assumption that card issuance is a "sticky" product, and should be deprioritized as a churn-prevention lever.
3. **Funded accounts churn at nearly double the rate of zero-balance accounts** (24.08% vs. 13.82%). This is counter-intuitive on its face but consistent with the balance-weighted attrition finding in §2.4: customers with capital to move are the ones who move it. Zero-balance accounts are often secondary, dormant, or already-decoupled relationships with little left to lose — their "retention" is a statistical artifact of having nothing left to withdraw, not genuine loyalty.

---

## 4. Risk Diagnostics

### 4.1 Deep Dive: Germany's Capital Flight

Germany presents a compound risk profile that is materially worse than a single-metric view suggests:

- **Headcount risk:** 814 of 2,509 German accounts have churned — a 32.44% rate, 1.59x the portfolio baseline.
- **Capital risk:** €97.97M of the €185.59M in total lost balance (52.79%) originated from Germany, against a total German deposit base of €300.40M. This implies that **32.6% of all German deposits by value** have already exited the bank — a rate nearly identical to the headcount churn rate, suggesting (unlike the portfolio-wide pattern) that German attrition is relatively balance-neutral *within* the country, but the country itself is a balance-heavy contributor overall.
- **GRI of 1.59** confirms Germany is the only jurisdiction generating capital loss meaningfully out of proportion to its footprint; France and Spain are both below parity (GRI 0.79 and 0.82 respectively).

**Root-cause hypotheses requiring validation:** (i) competitive displacement from German neobanks and direct-deposit fintechs (e.g., N26, Trade Republic-style cash products) offering superior digital UX and deposit yields; (ii) potential branch-network rationalization in the German market reducing physical touchpoints; (iii) FX/rate-sensitivity of German savers, who show historically higher price elasticity on deposit yield versus French and Spanish counterparts. These require triangulation against product-level interest rate data not present in this dataset, but the magnitude of the GRI gap makes Germany the unambiguous first-priority remediation market.

### 4.2 Deep Dive: The 46–60 Pre-Retirement Wealth Drain

The 46–60 cohort's 51.12% churn rate, isolated from the other three age bands, describes a "wealth drain" pattern rather than ordinary attrition:

- This cohort loses €75.17M against 842 churned accounts — an **implied average lost balance of ≈€89,275 per churned account**, above the portfolio-wide average lost balance per churn (≈€91,109 is portfolio-wide; the 46-60 figure is comparable in magnitude, confirming this is not a low-value segment exiting).
- The age band directly precedes typical European retirement transition points (60–67 depending on jurisdiction), which is precisely when customers consolidate holdings, seek wealth advisory services, and are most susceptible to being poached by dedicated wealth management competitors offering retirement-planning products the retail bank may not provide.
- Because this cohort represents only 16.47% of accounts but 41.3% of churn events and 40.5% of lost balance, it has by far the highest **loss-density** (lost-balance-per-account-in-cohort) of any segment in the dataset — higher even than Germany's country-level concentration.

### 4.3 Deep Dive: The Product Saturation Trap

The 100.00% churn rate among 4-product holders (n=60) and 82.71% among 3-product holders (n=266) should not be read naively as "products cause churn." More plausibly, these accounts represent one of two latent populations: (a) customers pushed through aggressive cross-sell into products they neither wanted nor use, creating dissatisfaction and eventual full relationship exit; or (b) customers in active off-boarding who accumulate products transiently during a complaint-resolution, renegotiation, or account-closure administrative process before final exit. Both explanations point away from "more products" as a retention strategy and toward **product-fit quality** and **cross-sell governance** as the true variables of interest — reinforcing that the safe, evidence-backed target is the 2-product configuration, not maximal bundling.

---

## 5. Strategic Recommendations

### 5.1 Cross-Sell 1-Product Customers Toward the 2-Product Optimum (Not Beyond)

With 5,084 accounts (50.84% of the portfolio) holding only one product and churning at 27.71% — representing €129.67M of at-risk balance, the single largest lost-balance segment in the entire portfolio — this is the highest-volume opportunity in the dataset. The evidence in §3.4 is unambiguous that migrating these customers to a second product (not a third or fourth) should be the target state: 2-product accounts churn at 7.58%, a reduction of over 20 percentage points. Recommended actions:
- Deploy needs-based (not quota-based) second-product offers — savings account or protection product — targeted at active, funded, single-product customers.
- **Explicitly cap** cross-sell campaigns at two products per household without a documented advisory rationale, given the sharply adverse 3-and-4-product outcomes; introduce a cross-sell governance gate requiring manager sign-off beyond two products.
- Prioritize this initiative in France, where the 5,014-account base and lower baseline churn (16.15%) suggest higher second-product conversion potential without the confounding competitive pressure present in Germany.

### 5.2 German Deposit Yield Re-Pricing & Competitive Response

Given Germany's 1.59 GRI and 52.79% share of lost balance against only a 25.09% account share, immediate action is warranted:
- Commission a rate-sensitivity / elasticity study specific to the German back-book to determine whether targeted yield re-pricing on at-risk deposit tiers (e.g., balances above the portfolio median) can be cost-justified against the €97.97M already lost.
- Benchmark digital account-opening and servicing experience against German fintech competitors; the disproportionate capital loss (rather than proportional headcount loss) suggests higher-balance, digitally-sophisticated customers are the ones leaving.
- Consider a retention-desk model (proactive outbound contact for balances above a defined threshold showing early disengagement signals) specifically staffed for the German market, given it is the only jurisdiction where GRI materially exceeds 1.0.

### 5.3 Wealth Advisory Intervention for the 46–60 Cohort

Given the 51.12% churn rate and €75.17M loss concentration in this single age band:
- Launch a dedicated pre-retirement wealth advisory program (portfolio consolidation, retirement income planning, tax-efficient savings vehicles) targeted specifically at the 46–60 segment, positioned as a relationship deepening — not cross-sell — initiative.
- Introduce proactive relationship-manager outreach triggers for any 46–60 customer showing reduced activity (`IsActiveMember` transitioning to 0), given the +12.58 point activity penalty compounds directly with this cohort's already-elevated baseline risk.
- Evaluate whether existing product shelf includes competitive retirement/wealth products; the absence of such an offering is a plausible structural driver of this cohort's disproportionate exit rate and should be tested via customer-exit surveys.

### 5.4 Secondary Recommendations
- **Deprioritize credit card issuance as a retention lever** — reallocate associated marketing spend toward activity-engagement campaigns, which show a 20x larger effect size (12.58 pts vs. 0.63 pts).
- **Investigate the gender churn gap (25.07% vs. 16.46%)** via a controlled multivariate model (logistic regression with age, balance, product count, and geography as covariates) before designing any gender-targeted intervention, to isolate whether the effect persists after controlling for confounding demographic and product variables.
- **Treat "funded account" status as a risk flag, not a safety signal** — funded accounts churn at nearly 2x the rate of zero-balance accounts (24.08% vs. 13.82%); retention scoring models should weight balance level as a risk-amplifying feature, not a stability indicator.

---

## Appendix: Summary Portfolio Statistics

| Metric | Value |
|---|---|
| Total Accounts | 10,000 |
| Retained | 7,963 |
| Churned | 2,037 |
| Baseline Churn Rate | 20.37% |
| Total Deposited Portfolio | €764,858,892.88 |
| Total Capital at Risk (Lost Deposits) | €185,588,094.63 |
| Capital-at-Risk Rate | 24.26% |
| Highest-Risk Geography | Germany (32.44% churn, GRI 1.59) |
| Highest-Risk Age Cohort | 46–60 (51.12% churn) |
| Optimal Product Depth | 2 Products (7.58% churn) |
| Largest Single Lever | Member Activity (+12.58 pt spread) |
