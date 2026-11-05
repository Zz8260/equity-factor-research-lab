# Factor Library

This is the complete public index of the supplied archive: **65 factor scripts returning 110 source-qualified outputs**, plus **26 named commented output alternatives**. The remaining **12 scripts** handle assembly, labels, correlation or models. Eight separately identified demo factors are executable. One referenced external panel has no supplied definitions.

These are implementation inventory counts, not independent-factor, novelty or performance claims. An identity such as `S023.arctan_fac90` includes its source because names recur across scripts with different formulas. Private source files are excluded; original byte counts and SHA-256 fingerprints remain in [source_inventory.csv](source_inventory.csv).

## Execution status

| Status | Meaning | What happens when requested for computation |
| --- | --- | --- |
| `demo` | One of the eight implemented synthetic reconstructions | Calculates the existing public factor |
| `archive` | Active returned output inspected in the supplied source | Raises `FactorUnavailableError`; data and a reviewed public adapter/implementation are still needed |
| `commented` | Named output alternative commented out in the source | Raises the same explicit availability error |
| `reference` | Upstream feature panel mentioned without supplied definitions | Raises an error; no formula or value is invented |

The [145-entry registry](../src/factorlab/factor_catalog.csv) gives a unique ID, definition, inputs, availability time, related demo proxy, review note and selected source expression. A proxy is a research connection, not evidence that an archive factor was computed. Inspect one entry with `factorlab catalog --factor S076.hifeq_1s` or export all metadata with `factorlab catalog --json`.

## Eight runnable reconstructions

All demo factors use information available by close t; they are evaluated against next-session open-to-close returns. Earnings/book equity/ROE are static synthetic attributes; real financial data requires publication-timestamped joins.

| Demo ID | Formula | Relationship to archive |
| --- | --- | --- |
| `earnings_yield` | Earnings / market capitalization | EP theme; source industry/configuration variants remain separate |
| `book_to_price` | Book equity / market capitalization | BP arithmetic on synthetic fundamentals |
| `profitability_residual` | Cross-sectional ROE residual versus intercept + EP | Related to S004, which instead uses per-security historical slopes and a different residual convention |
| `reversal_20d` | -sum(turnover * simple_return) / sum(turnover), 20 returns | S066 instead sums turnover-weighted gross ratios and uses another size proxy |
| `sampled_volatility` | sqrt(sum(sample_return squared)) | Twelve sampled prices, not the archive's full 240-minute normalization |
| `trade_imbalance` | (Buy volume - sell volume) / total | Classified synthetic flow; no exchange event reconstruction |
| `book_imbalance` | Mean((bid depth - ask depth) / total depth) | Aggregate depth, not ten-level price-weighted or skewness signals |
| `opening_gap` | open[t] / close[t-1] - 1 | Signed session gap, not the archive's exponentiated opening/early-window terms |

## Archive families and construction notes

The expandable source maps below list **every active returned output** and **every named commented output alternative** included in the inventory. Scratch calculations are described as components, not inflated into new factors. The registry provides per-output definitions and timing/blockers; the source table accounts for every original script.

### Valuation and profitability

Publication-timestamped fundamentals, prices, shares, industry and a trading calendar. EP/BP divide accounting values by market capitalization. S004 fits ROE on EP separately for each security over 300 sessions, then neutralizes its slope on a source size proxy. Its first-observation residual omits an intercept. S005/S008 rank within industry; S006/S009 request neutralization in the external backtest configuration rather than returning adjusted EP directly.

<details>
<summary>8 returned outputs: complete source and variant map</summary>

| Source | Research variant | Active returned outputs | Named commented alternatives |
| --- | --- | --- | --- |
| S002 | Daily book-to-price signal | `BP` | None |
| S004 | Earnings-yield and ROE regression | `EP_ROE_beta_mrkt_neu`, `resi` | None |
| S005 | Earnings yield with explicit industry neutralization | `ep_rank` | None |
| S006 | Earnings yield with built-in industry and size neutralization | `ep_rank_size` | None |
| S007 | Daily earnings-yield signal | `ep` | None |
| S008 | Earnings yield with explicit industry and size neutralization | `ep_rank_size` | None |
| S009 | Earnings yield with built-in industry neutralization | `fac1` | None |

</details>

### Intraday return distribution

Complete minute bars and the exact previous-close convention. Let g=close/pre_close and r=g-1. Volatility outputs use sqrt(sum((g-mean(g))^2))/240; positive-side variants apply a return filter. Skewness uses the source finite-sample coefficient. Sum/product outputs aggregate gross ratios g, not ordinary simple returns. A fixed 240 normalization needs a session-completeness rule.

<details>
<summary>6 returned outputs: complete source and variant map</summary>

| Source | Research variant | Active returned outputs | Named commented alternatives |
| --- | --- | --- | --- |
| S039 | Prior-session intraday return volatility | `std` | None |
| S040 | Prior-session negative intraday volatility | `std_ngt` | None |
| S041 | Prior-session positive intraday volatility | `std_pst` | None |
| S042 | Prior-session intraday return skewness | `skewness` | None |
| S043 | Prior-session cumulative intraday returns | `cum_sum_ret`, `cum_prdct_ret` | None |

</details>

### Price, volume, reversal and jumps

Adjusted daily OHLC, turnover, complete minute bars and full cross-sections as needed. S046 sums exp(signed amplitude * sequence index)/turnover^2 over two days. S047 uses a gross open/previous-close ratio. S066 residualizes a 20-day turnover-weighted gross-ratio sum on shares*log(close). S077 is the moth composite defined below.

<details>
<summary>5 returned outputs: complete source and variant map</summary>

| Source | Research variant | Active returned outputs | Named commented alternatives |
| --- | --- | --- | --- |
| S046 | Amplitude and liquidity signal | `fac1` | None |
| S047 | Daily price jump signal | `fac1` | None |
| S066 | Twenty-day turnover-weighted reversal with size neutralization | `rev` | None |
| S069 | Overnight gap with early-session transformation | `over_night` | None |
| S077 | Nonlinear intraday jump and amplitude signal | `moth` | None |

</details>

### Opening and early-session windows

Current-session minute observations including 09:30, with clear bar timestamps. Let g_u=close_u/pre_close_u and O=exp(abs(g_09:30-1)). S048-S052 average g_u+O strictly between 09:30 and the 10/15/20/25/29-minute endpoint. S053 returns O alone over the five-minute window. Do not trade before the required window is complete.

<details>
<summary>6 returned outputs: complete source and variant map</summary>

| Source | Research variant | Active returned outputs | Named commented alternatives |
| --- | --- | --- | --- |
| S048 | Early-session 10-minute signal | `buy_in` | None |
| S049 | Early-session 15-minute signal | `buy_in` | None |
| S050 | Early-session 20-minute signal | `buy_in` | None |
| S051 | Early-session 25-minute signal | `buy_in` | None |
| S052 | Early-session 29-minute signal | `buy_in` | None |
| S053 | Early-session 5-minute signal | `over_night` | None |

</details>

### Trade flow and small-order behavior

Classified trade/order events, prices, volumes, IDs/event codes, size data and exchange-specific direction definitions. S018 averages minute return times volume over five sessions. S044 compares the current opening reference with prior-session trade prices, weighted by prior notional. S054-S059 select small observations by z-score or bottom-decile rank, then return buy-sell differences/ratios, sometimes size residuals. S067/S068 use normalized buy-sell flow.

<details>
<summary>26 returned outputs: complete source and variant map</summary>

| Source | Research variant | Active returned outputs | Named commented alternatives |
| --- | --- | --- | --- |
| S018 | Major trade-flow trend signal | `fac1` | None |
| S044 | Same-session trade-level returns | `prof` | None |
| S045 | Same-session trade-level returns with size neutralization | `ols_resid` | None |
| S054 | Prior-session small-order submitted-amount imbalance | `ord_amt_deduc`, `ord_amt_devis`, `ord_vol_deduc`, `ord_vol_devis` | None |
| S055 | Prior-session small-order submitted-amount imbalance top-ten variant | `ord_amt_deduc`, `ord_amt_devis`, `ord_vol_deduc`, `ord_vol_devis` | None |
| S056 | Prior-session small-trade volume imbalance | `ols_vol_resid`, `ols_amt_resid` | None |
| S057 | Prior-session small-trade volume imbalance top-ten variant | `fac_amt_deduc`, `fac_amt_devis`, `fac_vol_deduc`, `fac_vol_devis` | None |
| S058 | Prior-session small-trade amount imbalance | `mat_amt_deduc`, `mat_amt_devis`, `mat_vol_deduc`, `mat_vol_devis` | None |
| S059 | Prior-session small-trade amount imbalance top-ten variant | `mat_amt_deduc`, `mat_vol_deduc` | None |
| S067 | Trade imbalance with size neutralization | `diff_vol_idst`, `diff_amt_idst` | None |
| S068 | Trade-volume imbalance | `diff_vol` | `diff_amt` |

</details>

### Order-book shape and pressure

Ten-level timestamped bid/ask prices and volumes. Use level notional N_l=price_l*volume_l. S061 weights levels 1..10 by 10..1 before normalizing bid-ask imbalance. S062 computes sums of cubed standardized level notionals. S064 weights bid/ask skewness by their mean notionals. S065 combines far_bid/(1+near_bid) and near_ask/(1+far_ask), with near=levels 1..5 and far=6..10. Aggregate demo depth cannot reproduce these definitions.

<details>
<summary>6 returned outputs: complete source and variant map</summary>

| Source | Research variant | Active returned outputs | Named commented alternatives |
| --- | --- | --- | --- |
| S061 | Weighted order-book notional imbalance | `spread_date` | None |
| S062 | Same-session order-book pressure and skewness | `skew_bid`, `skew_ask` | `skew_price`, `pressure`, `idvs_pred_ystd` |
| S063 | Prior-session order-book pressure and skewness | `idvs_pred_mrning` | `skew_bid`, `skew_ask`, `skew_price`, `pressure` |
| S064 | Prior-session bid-ask order-book skewness difference | `imp_skew` | `skew_bid`, `skew_ask`, `skew_price`, `pressure` |
| S065 | Order-book submitted-depth distribution | `pressure` | `skew_bid`, `skew_ask`, `skew_price`, `idvs_pred_ystd` |

</details>

### Order survival and cancellation timing

Order IDs, submission timestamps/prices, final trade or cancellation links, and aligned minute reference prices. The common output is mean(order_price/reference_pre_close), conditional on observed lifetime above/below a threshold. Prior-session and current-window variants remain distinct. Final observed event time is not automatically a true cancellation time: censored orders, clock units, symbol-aware joins/fills and event cutoffs must be resolved.

<details>
<summary>10 returned outputs: complete source and variant map</summary>

| Source | Research variant | Active returned outputs | Named commented alternatives |
| --- | --- | --- | --- |
| S070 | Same-session order survival longer than one minute | `momentum` | None |
| S071 | Prior-session order survival longer than one minute | `momentum` | None |
| S072 | Same-session longer-lived orders | `non_hifeq_5min_today`, `non_hifeq_10min_today`, `non_hifeq_20min_today` | None |
| S073 | Prior-session longer-lived orders | `non_hifeq_10s` | `non_hifeq_5s`, `non_hifeq_1s` |
| S074 | Same-session high-frequency cancellations | `hifeq_10s_retreat_today` | `hifeq_5s_retreat_today`, `hifeq_1s_retreat_today` |
| S075 | Same-session high-frequency order and cancellation variants | `hifeq_1s_retreat_today` | `hifeq_500ms_retreat_today`, `hifeq_100ms_retreat_today` |
| S076 | Prior-session high-frequency cancellation variants | `hifeq_5s`, `hifeq_1s` | `hifeq_10s` |

</details>

### Nonlinear price adjustment and cross-sectional variants

At least 252 completed daily sessions, five-observation path windows, two recent session returns, and industry/turnover cross-sections. Families use cubic, reciprocal, arctangent or blended path scores; retain the source-specific quantile and denominator choices. The shared construction dictionary below explains the 43 returned variants without presenting them as independent signals.

<details>
<summary>43 returned outputs: complete source and variant map</summary>

| Source | Research variant | Active returned outputs | Named commented alternatives |
| --- | --- | --- | --- |
| S019 | Price adjustment and direction detection quantile 75 | `fac75` | None |
| S020 | Price adjustment and direction detection quantile 80 | `fac80` | None |
| S021 | Price adjustment and direction detection quantile 85 | `fac85` | None |
| S022 | Price adjustment and direction detection quantile 90 | `modify_fac90` | None |
| S023 | Price adjustment quantile 90 arctangent | `arctan_fac90` | None |
| S024 | Price adjustment quantile 90 modified equal-weight arctangent | `arctan_fac90` | None |
| S025 | Price adjustment quantile 90 cubic | `sq3_fac90` | None |
| S026 | Price adjustment quantile 90 full-market | `fac90`, `modify_idvs_deduct_fac`, `modify_idvs_divis_fac` | None |
| S027 | Price adjustment quantile 90 full-market arctangent | `fac90`, `arctan_idvs_deduct_fac`, `arctan_idvs_divis_fac` | None |
| S028 | Price adjustment quantile 90 full-market cubic | `sq3_fac90`, `sq3_idvs_deduct_fac`, `sq3_idvs_divis_fac` | None |
| S029 | Price adjustment quantile 90 turnover orthogonalization | `modify_heat_neutr_fac90`, `modify_heat_rec_beta` | None |
| S030 | Price adjustment quantile 90 turnover orthogonalization arctangent | `arctan_heat_neutr_fac90`, `arctan_heat_rec_beta` | None |
| S031 | Price adjustment quantile 90 turnover orthogonalization cubic | `sq3_heat_neutr_fac90`, `sq3_heat_rec_beta` | None |
| S032 | Price adjustment quantile 90 industry neutralization | `modify_fac_rec_rank` | None |
| S033 | Price adjustment quantile 90 industry neutralization arctangent | `arctan_fac_rec_rank` | None |
| S034 | Price adjustment quantile 90 industry neutralization cubic | `sq3_fac_rec_rank` | None |
| S035 | Price adjustment quantile 90 industry enhancement | `modify_idvs_dd_exp`, `modify_idvs_divis`, `modify_idvs_dd_sta_exp`, `modify_idvs_divis_sta`, `modify_idvs_idst_enhance`, `modify_idvs_idst_sta_enhance`, `modify_idvs_dd_exp_enhance` | None |
| S036 | Price adjustment quantile 90 industry enhancement arctangent | `arctan_idvs_dd_exp`, `arctan_idvs_divis`, `arctan_idvs_idst_enhance`, `arctan_idvs_dd_exp_enhance` | `arctan_idvs_dd_sta_exp`, `arctan_idvs_divis_sta`, `arctan_idvs_idst_sta_enhance` |
| S037 | Price adjustment quantile 90 industry enhancement cubic | `sq3_idvs_dd_exp`, `sq3_idvs_divis`, `sq3_idvs_dd_sta_exp`, `sq3_idvs_divis_sta`, `sq3_idvs_idst_enhance`, `sq3_idvs_idst_sta_enhance`, `sq3_idvs_dd_exp_enhance` | None |

</details>

### Nonlinear construction dictionary

Let p_i denote the i-th close in a completed five-observation window and p_end its endpoint; q_i=abs(p_i/p_end-1). The archive uses several source-specific path deviations W:

- **Cubic:** sum(i^3*q_i). S019-S021 use 1/W and upper quantiles 75/80/85; S025 uses 1/(W+1).
- **Modified reciprocal:** reciprocal-distance terms and tail deviations, with a sign term from the path endpoints. S022 uses 1/(W+1), while some cross-sectional variants use 1/W. Parentheses/reductions must be ported literally and reviewed; this is not one universal reciprocal formula.
- **Arctangent:** deviations from 2*atan(i)/pi, with source-specific centering, direction or division terms. Its full-market, base and industry versions are not formula-identical.
- **Blended:** S024 combines 0.5*(1+W_arctan) with 0.5/(1+W_modified); the shared `arctan_fac90` name does not make S023 and S024 identical.

F denotes the mean selected reciprocal/path score after the source's signed or absolute quantile filtering. D is the product of the two recent **simple** returns multiplied by the sum of their signs. A historical four-observation lead is used to form a completed path window; it must remain inside available history and within the same security. Grouping, sort order, zero denominators and the source-specific filters require review before any live use.

Cross-sectional variants include F*D, exp(F-market_mean(F))*D, and (F/market_mean(F))*D. Industry-rank variants use the within-industry percentile of F times D. Turnover variants regress selected F on turnover rank and export a slope or first-observation residual times D.

For industry enhancement, I is the industry mean of F. As written, Z=(F-global_mean(F))/industry_std(F); it is not conventional industry demeaning. M is the within-industry mean of Z restricted to -1<Z<1. The seven transformations, each multiplied by D, are:

| Output suffix | Transformation |
| --- | --- |
| `idvs_dd_exp` | exp(F-I) |
| `idvs_divis` | F/I |
| `idvs_dd_sta_exp` | exp(Z-M) |
| `idvs_divis_sta` | (Z+1)/(M+1) |
| `idvs_idst_enhance` | F*I |
| `idvs_idst_sta_enhance` | (Z+1)*(M+1) |
| `idvs_dd_exp_enhance` | exp(F-I)*I |

Modified and cubic files return all seven; the arctangent source returns four and comments out three. Source-specific formula conventions and the 75/80/85/90 quantile choices are exploratory research decisions, not separately validated discoveries.

### Moth composite components

S077 combines 20 completed minute-bar sessions. For gross minute ratio g, J=2*(g-1)-2*log(g)-log(g)^2. The monthly jump score is half the mean plus half the sample standard deviation of daily mean J. Two corrected-amplitude terms multiply daily amplitude by the sign of cross-sectional deviations: first for daily J, then for H=2*(R-log(1+R))-log(1+R)^2 with R=intraday_high/intraday_low-1. The final composite is 0.5*monthly_jump + 0.25*mean(corrected_amplitude_1) + 0.25*mean(corrected_amplitude_2). These components are preserved here as components, not additional returned outputs.

## Source issues to resolve before reproduction

| Source | Observed behavior | Required decision |
| --- | --- | --- |
| S004, S066 and several size residuals | Size proxy is shares*log(close), not log(close*shares) | Preserve intentionally or correct with a new documented experiment |
| S040 | Negative-volatility label uses r>0, like S041 | Resolve intended sign; do not claim a distinct negative-side implementation |
| S045 | Minute prices are overwritten by daily prices before a time-filtered opening join | Repair the input/column flow |
| S047 | Previous day is a calendar subtraction | Use a validated exchange-session calendar |
| S053, S069 | Active output contains only the exponentiated opening term | Keep distinct from a signed opening gap or full early-return composite |
| S061 | Filename suggests spread, but formula is weighted notional imbalance | Use the formula-based label |
| S063 | Group operation returns a list, not a scalar factor | Specify and validate a scalar reduction |
| S070 | Current-day event scans have no explicit upper cutoff despite a 10:00 configuration | Bound every event by the prediction timestamp |
| S076 `hifeq_1s` | Active threshold is one minute | Resolve name versus duration before use |
| Nonlinear family | Some shifts/fills lack explicit symbol scoping; reciprocals can be singular | Verify library semantics, completed-window bounds and numerical guards |

These notes describe implementation questions in exploratory material. No archived output is advertised as reproduced merely because a similar demo feature exists.

## Research utilities and unresolved external panel

| Source | Role |
| --- | --- |
| S001 | Feature assembly and model scoring |
| S003 | Cross-factor correlation analysis |
| S010 | Feature parquet assembly baseline |
| S011 | Feature parquet assembly arctangent variant |
| S012 | Feature parquet assembly cubic variant |
| S013 | OLS and logistic regression experiments |
| S014 | Lasso and Ridge regression experiments |
| S015 | Regularized logistic regression with additional feature panel |
| S016 | Forward return label assembly |
| S017 | Forward return label assembly with additional features |
| S038 | Decision-tree training |
| S060 | Model scoring and backtest configuration |

The archive includes OLS, logistic, Lasso/Ridge, tree modeling, cross-factor correlation, rank/direction transforms and parquet assembly. These are recorded as research utilities rather than inflated into original factor definitions. Only Ridge is implemented in the runnable demo.

Several utilities reference an absent external panel described in filenames as "96 factors". A commented list contains fac0 through fac96, but no per-column formulas are supplied. The `external_panel` registry entry preserves this dependency and the count ambiguity; it does not manufacture 96 or 97 definitions.
