#!/usr/bin/env Rscript
# Generate reference values from R catdap package for cross-validation.
#
# Requirements:
#   install.packages("catdap")   # version 1.3.5 used for the committed CSVs
#
# Usage:
#   Rscript docs/r_reference/generate_reference.R
#
# Output files (written to the same directory as this script):
#   health_catdap1.csv               -- catdap1 ΔAIC, symptoms vs categorical cols
#   health_catdap2_aic.csv           -- catdap2 single-variable ΔAIC, categorical
#                                       (pool=2) explanatory variables only
#   health_catdap2_fixed_partition.csv -- catdap2 ΔAIC for continuous variables
#                                       at R's chosen bin cut points
#
# SCOPE NOTE (see CONTRIBUTING.md "R version cross-check"):
#   pycatdap's AIC engine is bit-exact with R catdap for any *fixed* partition.
#   The continuous-variable binning *selection* differs by design (pycatdap uses
#   a greedy AIC-merge from fine bins; R catdap pool=0 is a coarser split-based
#   heuristic), so the strict cross-check validates the engine on fixed
#   partitions, NOT the choice of bins. health_catdap2_fixed_partition.csv
#   therefore records R's cut points so pycatdap can be evaluated on the
#   identical partition.
#
# R catdap version used: 1.3.5

library(catdap)

# Resolve this script's directory robustly. ``Rscript <path>`` exposes the path
# via the ``--file=`` command-line argument; an interactive ``source()`` exposes
# it via ``sys.frame(1)$ofile``. Fall back to the working directory otherwise.
script_dir <- function() {
  file_arg <- grep("^--file=", commandArgs(trailingOnly = FALSE), value = TRUE)
  if (length(file_arg) > 0) {
    return(dirname(normalizePath(sub("^--file=", "", file_arg[1]))))
  }
  ofile <- tryCatch(sys.frame(1)$ofile, error = function(e) NULL)
  if (!is.null(ofile)) {
    return(dirname(normalizePath(ofile)))
  }
  getwd()
}
outdir <- script_dir()

data(HealthData)

# --- HealthData: catdap1 (categorical columns only) --------------------------
# r1$aic is an unnamed (n x n) matrix in input-column order; the diagonal is NA.

cat_names <- c("symptoms", "opthalmo.", "ecg", "cholesterol")
cat_cols <- HealthData[, cat_names]
r1 <- catdap1(cat_cols, plot = 0)
aic1 <- r1$aic
dimnames(aic1) <- list(cat_names, cat_names)

aic_symptoms <- aic1["symptoms", ]
aic_df <- data.frame(
  variable = names(aic_symptoms),
  aic = as.numeric(aic_symptoms),
  stringsAsFactors = FALSE
)
aic_df <- aic_df[!is.na(aic_df$aic), ]
write.csv(aic_df, file.path(outdir, "health_catdap1.csv"), row.names = FALSE)

# --- HealthData: catdap2 -----------------------------------------------------
# pool/accuracy are aligned to HealthData's column order. pool codes:
#   2 = no pooling (categorical), 0 = continuous (R: equally-spaced top-down).

col_names <- names(HealthData)
pool <- c(2, 2, 2, 0, 0, 0, 0, 2)
accuracy <- c(0., 0., 0., 1., 1., 1., 0.1, 0.)
response <- "symptoms"

r2 <- catdap2(HealthData, pool, response, accuracy, plot = 0)
aic2 <- r2$aic
names(aic2) <- col_names

# (a) Single-variable AIC for the CATEGORICAL (pool=2) explanatory variables.
#     These match pycatdap bit-exactly (no binning involved).
cat_expl <- col_names[pool == 2 & col_names != response]
aic2_df <- data.frame(
  variable = cat_expl,
  aic = as.numeric(aic2[cat_expl]),
  stringsAsFactors = FALSE
)
write.csv(aic2_df, file.path(outdir, "health_catdap2_aic.csv"), row.names = FALSE)

# (b) Continuous variables: record R's chosen internal cut points + R's AIC.
#     r2$interval[[i]] = c(min, cut_1, ..., cut_k, max); internal cuts drop ends.
cont_idx <- which(pool == 0)
cont_rows <- lapply(cont_idx, function(i) {
  iv <- r2$interval[[i]]
  cuts <- iv[-c(1, length(iv))]
  data.frame(
    variable = col_names[i],
    cuts = paste(format(cuts, trim = TRUE), collapse = ";"),
    aic = as.numeric(aic2[col_names[i]]),
    stringsAsFactors = FALSE
  )
})
fixed_df <- do.call(rbind, cont_rows)
write.csv(
  fixed_df,
  file.path(outdir, "health_catdap2_fixed_partition.csv"),
  row.names = FALSE
)

cat("Reference files generated in:", outdir, "\n")
