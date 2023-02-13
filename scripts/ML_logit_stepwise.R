remove(list=ls())
library(dplyr)
library(MASS)

#Load dataset 

df <- read.csv(
  "C:/Users/18126/OneDrive - University of Toronto/Projects/sp_branching_order/results/10dim_branchingorder_ML_features.csv")

#Randomly subset data to mimic training dataset creation 

df <- df[sample(nrow(df), 3000),]
df <- df[,-1]

#Z normalization

df_scaled <- as.data.frame(scale(df[,1:21], center = TRUE, scale = TRUE))

df_scaled <- cbind(df_scaled, sptree = df[,22])

#Fit logistic regression 

df_scaled$sptree[df_scaled$sptree == "AB"] <- 0
df_scaled$sptree[df_scaled$sptree == "BC"] <- 1
df_scaled <- dplyr::mutate_all(df_scaled, function(x) as.numeric(as.character(x)))


model <- glm(formula = sptree ~., family = "binomial", data = df_scaled)

#Stepwise selection

step.model <- model %>% MASS::stepAIC(trace = FALSE)

#Write to file 

sink("ML_logit_stepwise_results.txt")
print(summary(step.model))
sink()