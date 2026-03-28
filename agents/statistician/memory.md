# Statistician Memory

## Population sizes (as of session start)

- **>50pp cluster:** n=49. Below threshold for most parametric tests. Use non-parametric methods (bootstrap, Mann-Whitney U) or state low-power caveat explicitly.
- **20-50pp cluster:** n=237. Marginal for parametric tests — verify normality assumptions before using t-tests. Bootstrap CIs preferred.
- **Full graduating trades population:** n=3,664. Adequate for most parametric and non-parametric tests. Central limit theorem applies for means.

## Notable results

- **Guard C result:** 14/49 improved, 0/49 hurt. Directionally strong but n=49 is below the n>=30 soft threshold for parametric tests. Binomial test p-value is significant (p < 0.001 for 14/49 vs 0/49 under null of equal probability), but the small sample means confidence intervals on the improvement rate are wide. Bootstrap CI recommended for the improvement proportion.

## Methodological notes

- Trading PnL distributions are typically right-skewed with fat tails — parametric assumptions (normality) rarely hold. Default to bootstrap CIs.
- When evaluating parameter sweeps, always count the number of combinations tested. At p<0.05, expect 1 false positive per 20 tests. Apply Benjamini-Hochberg correction as default (less conservative than Bonferroni, better suited to exploratory research).
