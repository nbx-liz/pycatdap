#!/usr/bin/env Rscript
# Generate reference values from R catdap package for cross-validation.
#
# Requirements:
#   install.packages("catdap")
#
# Usage:
#   Rscript generate_reference.R
#
# Output files (written to the same directory as this script):
#   health_catdap1.csv          -- catdap1 AIC for categorical columns
#   health_catdap2_aic.csv      -- catdap2 single-variable AIC
#   health_catdap2_subsets.csv  -- catdap2 best subsets
#
# R catdap version used: 1.3.5

library(catdap)

outdir <- dirname(sys.frame(1)$ofile)

# --- HealthData: catdap1 (categorical columns only) --------------------------

data(HealthData)
cat_cols <- HealthData[, c("symptoms", "opthalmo.", "ecg", "cholesterol")]
r1 <- catdap1(cat_cols)

# Extract AIC matrix for symptoms as response
aic_symptoms <- r1$aic["symptoms", ]
aic_df <- data.frame(
  variable = names(aic_symptoms),
  aic = as.numeric(aic_symptoms),
  stringsAsFactors = FALSE
)
aic_df <- aic_df[!is.na(aic_df$aic), ]
write.csv(aic_df, file.path(outdir, "health_catdap1.csv"), row.names = FALSE)

# --- HealthData: catdap2 -----------------------------------------------------

r2 <- catdap2(
  HealthData,
  c(2, 2, 2, 0, 0, 0, 0, 2),
  "symptoms",
  c(0., 0., 0., 1., 1., 1., 0.1, 0.)
)

# Single-variable AIC
aic2_df <- data.frame(
  variable = names(r2$aic),
  aic = as.numeric(r2$aic),
  stringsAsFactors = FALSE
)
write.csv(aic2_df, file.path(outdir, "health_catdap2_aic.csv"), row.names = FALSE)

# Best subsets
subsets_list <- r2$best.model
subsets_df <- data.frame(
  n_vars = sapply(subsets_list, function(x) length(x$variables)),
  variables = sapply(subsets_list, function(x) paste(x$variables, collapse = ";")),
  aic = sapply(subsets_list, function(x) x$aic),
  stringsAsFactors = FALSE
)
write.csv(subsets_df, file.path(outdir, "health_catdap2_subsets.csv"), row.names = FALSE)

cat("Reference files generated in:", outdir, "\n")
