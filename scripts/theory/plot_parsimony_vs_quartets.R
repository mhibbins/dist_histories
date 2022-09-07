remove(list=ls())
library(lattice)
library(RColorBrewer)

get_mindelta_ratio <- function(ts, tm) {
  
  mindelta_parsimony <- ts/(tm + ts)
  mindelta_quartets <- (1 - exp(-ts))/(2 - exp(-tm) - exp(-ts))
  
  ratio <- mindelta_parsimony-mindelta_quartets
  
  return(ratio)
}

mindelta_matrix <- outer(seq(0.0001, 2, length=100), 
                         seq(0.0001, 2, length=100),
                         Vectorize( function(x, y) get_mindelta_ratio(x, y)))

ts_vals <- seq(0.0001, 2, length=100)
get_rate_dis <- function(ts) {return((2/3)*exp(-ts))}
rate_dis <- sapply(ts_vals, FUN = get_rate_dis)

levelplot(mindelta_matrix, cex.axis = 0.5, 
          at = c(-0.12, -0.075, -0.05, -0.025, 0, 0.025, 0.05, 0.075, 0.12),
          xlab = list("Rate of discordance without introgression", cex = 1.25),
          ylab = list("Rate of discordance at introgressed loci", cex = 1.1),
          col.regions = colorRampPalette(rev(brewer.pal(9, 'Blues')), bias = 1),
          #col.regions = heat.colors(100)[length(heat.colors(100)):1],
          par.settings = list(layout.widths = list(axis.key.padding = 0, ylab.right = 2)),
          row.values = rate_dis, 
          column.values = rate_dis,
          aspect = 0.75, xlim = c(rate_dis[-1], rate_dis[1]), ylim = c(rate_dis[-1], rate_dis[1]),
          colorkey = FALSE,
          labels = list(format(c(-0.12, -0.075, -0.05, -0.025, 0, 0.025, 0.05, 0.075, 0.12), cex=1.5)),
          scales = list(x=list(cex=1.5), y=list(cex=1.5)),
          contour = TRUE)