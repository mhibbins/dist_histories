remove(list=ls())
library(plotly)
library(tidyverse)
library(reticulate)
library(plot3D)

get_mindelta <- function(ts, tm) {
  
  top = 1 - exp(-ts)
  bottom = 2 - exp(-tm) - exp(-ts)
  
  mindelta = top/bottom
  
  return(mindelta)
}

mindelta_matrix <- outer(seq(0.0001, 2, length=100), 
                         seq(0.0001, 2, length=100),
                         Vectorize( function(x, y) get_mindelta(x, y)))

ts_vals <- seq(0.0001, 2, length=100)
get_rate_dis <- function(ts) {return((2/3)*exp(-ts))}
rate_dis <- rev(sapply(ts_vals, FUN = get_rate_dis))

axx <- list(title = "Species tree discordance")
axy <- list(title = "Introgressed loci discordance")
axz <- list(title = "Rate of introgression")


fig <- plot_ly(x = rate_dis, y = rate_dis, z = mindelta_matrix, type = "surface",
               showscale = FALSE)
fig <- fig %>% layout(scene = list(xaxis = axx, yaxis = axy, zaxis = axz))

fig

save_image(fig, 
        file = "C:/Users/18126/OneDrive - University of Toronto/Projects/sp_branching_order/figures/mindelta_3D.svg")


