remove(list=ls())
library(ggplot2)
library(gridExtra)

ML_features <- read.csv(
  "C:/Users/18126/OneDrive - University of Toronto/Projects/sp_branching_order/results/10dim_branchingorder_ML_features.csv")

ML_params <- read.csv(
  "C:/Users/18126/OneDrive - University of Toronto/Projects/sp_branching_order/results/10dim_branchingorder_ML_params.csv")

df <- as.data.frame(cbind(ML_features$BC_BC_var,
                          ML_features$AB_AB_var,
                          ML_features$AB_AB_dist,
                          ML_features$BC_BC_dist,
                          ML_features$AB_freq,
                          ML_features$BC_freq,
                          ML_features$sptree, ML_params$delta,
                          ML_params$dir))

colnames(df) <- c("BC_BC_var", "AB_AB_var", "AB_AB_dist", "BC_BC_dist",
                  "AB_freq", "BC_freq", "sptree", "delta", "dir")

df$sptree <- as.factor(df$sptree)
df$BC_BC_var <- as.numeric(df$BC_BC_var)
df$AB_AB_var <- as.numeric(df$AB_AB_var)
df$AB_AB_dist <- as.numeric(df$AB_AB_dist)
df$BC_BC_dist <- as.numeric(df$BC_BC_dist)
df$AB_freq <- as.numeric(df$AB_freq)
df$BC_freq <- as.numeric(df$BC_freq)
df$delta <- as.numeric(df$delta)
df$dir <- as.factor(df$dir)

BC_BC_var_line_plot <- ggplot(df, aes(x=delta, y = BC_BC_var,
                                      group = sptree,
                                      color = sptree)) + 
  stat_summary(fun.y=mean, geom="line", size = 1.5) +
  stat_summary(fun.data = mean_se, geom = "errorbar") +
  theme_minimal(base_size = 10) + 
  labs(x = expression(delta),
       y = "BC variance in BC trees",
       color = "Species tree") + 
  facet_wrap(~dir)


AB_AB_var_line_plot <- ggplot(df, aes(x=delta, y = AB_AB_var,
                                      group = sptree,
                                      color = sptree)) + 
  stat_summary(fun.y=mean, geom="line", size = 1.5) +
  stat_summary(fun.data = mean_se, geom = "errorbar") +
  theme_minimal(base_size = 10) + 
  labs(x = expression(delta),
       y = "AB variance in AB trees",
       color = "Species tree") + 
  facet_wrap(~dir)

AB_AB_dist_line_plot <- ggplot(df, aes(x=delta, y = AB_AB_dist,
                                      group = sptree,
                                      color = sptree)) + 
  stat_summary(fun.y=mean, geom="line", size = 1.5) +
  stat_summary(fun.data = mean_se, geom = "errorbar") + 
  theme_minimal(base_size = 10) + 
  labs(x = expression(delta),
       y = "AB distance in AB trees",
       color = "Species tree") + 
  facet_wrap(~dir)

BC_BC_dist_line_plot <- ggplot(df, aes(x=delta, y = BC_BC_dist,
                                       group = sptree,
                                       color = sptree)) + 
  stat_summary(fun.y=mean, geom="line", size = 1.5) +
  stat_summary(fun.data = mean_se, geom = "errorbar") + 
  theme_minimal(base_size = 10) + 
  labs(x = expression(delta),
       y = "BC distance in BC trees",
       color = "Species tree") + 
  facet_wrap(~dir)

AB_freq_line_plot <- ggplot(df, aes(x=delta, y = AB_freq,
                                       group = sptree,
                                       color = sptree)) + 
  stat_summary(fun.y=mean, geom="line", size = 1.5) +
  stat_summary(fun.data = mean_se, geom = "errorbar") + 
  theme_minimal(base_size = 10) + 
  labs(x = expression(delta),
       y = "AB tree frequency",
       color = "Species tree") + 
  facet_wrap(~dir)

BC_freq_line_plot <- ggplot(df, aes(x=delta, y = BC_freq,
                                    group = sptree,
                                    color = sptree)) + 
  stat_summary(fun.y=mean, geom="line", size = 1.5) +
  stat_summary(fun.data = mean_se, geom = "errorbar") + 
  theme_minimal(base_size = 10) + 
  labs(x = expression(delta),
       y = "BC tree frequency",
       color = "Species tree") + 
  facet_wrap(~dir)

grid.arrange(AB_AB_var_line_plot, BC_BC_var_line_plot,
             AB_AB_dist_line_plot, BC_BC_dist_line_plot,
             AB_freq_line_plot, BC_freq_line_plot, ncol=2)

