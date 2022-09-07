remove(list=ls())
library(lattice)
library(RColorBrewer)
library(gridExtra)

### Function to get minimum gene tree node height

get_min_node_height <- function(tm, t1, t2, delta2, delta3) {
  
  #Internal branch lengths and rates of ILS / introgression
  
  tau_pt1 <- t2 - t1
  tau_pt2 <- t2 - tm
  tau_pt3 <- t1 - tm
  
  pt1_sort <- 1 - exp(-tau_pt1)
  pt1_ILS <- (1/3)*exp(-tau_pt1)
  pt2_sort <- 1 - exp(-tau_pt2)
  pt2_ILS <- (1/3)*exp(-tau_pt2)
  pt3_sort <- 1 - exp(-tau_pt3)
  pt3_ILS <- (1/3)*exp(-tau_pt3)
  
  no_intro <- (1 - delta2 - delta3)
  
  #Conditional gene tree frequencies 
  
  f_AB11 <- (no_intro*pt1_sort)/(no_intro*pt1_sort + no_intro*pt1_ILS +
                                  delta2*pt2_ILS + delta3*pt3_ILS)
  f_AB21 <- (no_intro*pt1_ILS)/(no_intro*pt1_sort + no_intro*pt1_ILS +
                                   delta2*pt2_ILS + delta3*pt3_ILS)
  f_AB2 <- (delta2*pt2_ILS)/(no_intro*pt1_sort + no_intro*pt1_ILS +
                                  delta2*pt2_ILS + delta3*pt3_ILS)
  f_AB3 <- (delta3*pt3_ILS)/(no_intro*pt1_sort + no_intro*pt1_ILS +
                               delta2*pt2_ILS + delta3*pt3_ILS)
  
  f_BC12 <- (delta2*pt2_sort)/(delta2*pt2_sort + delta2*pt2_ILS + 
                                 no_intro*pt1_ILS + delta3*pt3_sort + 
                                 delta3*pt3_ILS)
  f_BC22 <- (delta2*pt2_ILS)/(delta2*pt2_sort + delta2*pt2_ILS + 
                                 no_intro*pt1_ILS + delta3*pt3_sort + 
                                 delta3*pt3_ILS)
  f_BC1 <- (no_intro*pt1_ILS)/(delta2*pt2_sort + delta2*pt2_ILS + 
                                no_intro*pt1_ILS + delta3*pt3_sort + 
                                delta3*pt3_ILS)
  f_BC13 <- (delta3*pt3_sort)/(delta2*pt2_sort + delta2*pt2_ILS + 
                                 no_intro*pt1_ILS + delta3*pt3_sort + 
                                 delta3*pt3_ILS)
  f_BC23 <- (delta3*pt3_ILS)/(delta2*pt2_sort + delta2*pt2_ILS + 
                                 no_intro*pt1_ILS + delta3*pt3_sort + 
                                 delta3*pt3_ILS)
  
  f_AC1 <- (no_intro*pt1_ILS)/(no_intro*pt1_ILS + delta2*pt2_ILS + 
                                 delta3*pt3_ILS)
  f_AC2 <- (delta2*pt2_ILS)/(no_intro*pt1_ILS + delta2*pt2_ILS + 
                                 delta3*pt3_ILS)
  f_AC3 <- (delta3*pt3_ILS)/(no_intro*pt1_ILS + delta2*pt2_ILS + 
                               delta3*pt3_ILS)
  
  
  #Heights of shortest node in each gene tree topology
  
  AB_AB11 <- t1 + (1 - tau_pt1/(exp(tau_pt1) - 1))
  AB_AB21 <- t2 + (1/3)
  AB_AB2 <- t2 + (1/3)
  AB_AB3 <- t1 + (1/3)
  
  AB_AB_height <- f_AB11*AB_AB11 + f_AB21*AB_AB21 + f_AB2*AB_AB2 + f_AB3*AB_AB3
  
  BC_BC1 <- t2 + 1/3
  BC_BC12 <- tm + (1 - tau_pt2/(exp(tau_pt2) - 1))
  BC_BC22 <- t2 + 1/3
  BC_BC13 <- tm + (1 - tau_pt3/(exp(tau_pt3) - 1))
  BC_BC23 <- t1 + 1/3
  
  BC_BC_height <- f_BC1*BC_BC1 + f_BC12*BC_BC12 + f_BC22*BC_BC22 + 
    f_BC13*BC_BC13 + f_BC23*BC_BC23
  
  AC_AC1 <- t2 + 1/3
  AC_AC2 <- t2 + 1/3
  AC_AC3 <- t1 + 1/3
  
  AC_AC_height <- f_AC1*AC_AC1 + f_AC2*AC_AC2 + f_AC3*AC_AC3
  
  if ((AB_AB_height < BC_BC_height) && (AB_AB_height < AC_AC_height)) {
    return(0)
  }
  else if ((BC_BC_height < AB_AB_height) && (BC_BC_height < AC_AC_height)) {
    return(1)
  }
  else {
    return(-1)
  }
}

### Make matrices over parameter space

make_minnode_matrix <- function(tm, t1, dir) {
  
  if (dir == "CintoB") {
    minnode_matrix <- outer(seq(0.61, 2, length=100), 
                            seq(0, 1, length=100),
      Vectorize( function(x, y) get_min_node_height(tm, t1, x, y, 0)))
  }
  else if (dir == "BintoC") {
    minnode_matrix <- outer(seq(0.61, 2, length=100), 
                                          seq(0, 1, length=100),
      Vectorize( function(x, y) get_min_node_height(tm, t1, x, 0, y)))
  }
  else if (dir == "Both") {
    minnode_matrix <- outer(seq(0.61, 2, length=100), 
                            seq(0, 0.5, length=100),
      Vectorize( function(x, y) get_min_node_height(tm, t1, x, y, y)))
  }
  
  return(minnode_matrix)
}

tm0.15_delta2_minnode_matrix <- make_minnode_matrix(0.15, 0.6, "CintoB")
tm0.15_delta3_minnode_matrix <- make_minnode_matrix(0.15, 0.6, "BintoC")
tm0.15_delta23_minnode_matrix <- make_minnode_matrix(0.15, 0.6, "Both")
tm0.3_delta2_minnode_matrix <- make_minnode_matrix(0.3, 0.6, "CintoB")
tm0.3_delta3_minnode_matrix <- make_minnode_matrix(0.3, 0.6, "BintoC")
tm0.3_delta23_minnode_matrix <- make_minnode_matrix(0.3, 0.6, "Both")
tm0.45_delta2_minnode_matrix <- make_minnode_matrix(0.45, 0.6, "CintoB")
tm0.45_delta3_minnode_matrix <- make_minnode_matrix(0.45, 0.6, "BintoC")
tm0.45_delta23_minnode_matrix <- make_minnode_matrix(0.45, 0.6, "Both")

### Plot matrices 

plot_minnode_matrix <- function(minnode_matrix) {

  ts_vals <- seq(0.61, 2, length=100)-0.6
  get_rate_dis <- function(ts) {return((2/3)*exp(-ts))}
  rate_dis <- sapply(ts_vals, FUN = get_rate_dis)

  minnode_plot <- levelplot(minnode_matrix, cex.axis = 0.5, 
                       at = c(-1, 0, 1),
                       xlab = list("Rate of discordance without introgression", 
                                   cex = 1),
                       ylab = list("Rate of introgression", cex = 1),
                       col.regions = colorRampPalette(rev(brewer.pal(3, 'RdBu')), 
                                                      bias = 1),
                       par.settings = list(layout.widths = 
                                             list(axis.key.padding = 0, 
                                                       ylab.right = 2)),
                       row.values = rate_dis, 
                       column.values = seq(0, 1, length=100),
                       aspect = "fill", xlim = c(rate_dis[-1], rate_dis[1]), 
                       ylim = c(0, 1), colorkey = FALSE,
                       labels = list(format(c("AC", "AB", "BC"), cex=0.5)),
                       scales = list(x=list(cex=0.5), y=list(cex=0.5)))
  
  return(minnode_plot)
}

tm0.15_delta2_minnode_plot <- plot_minnode_matrix(tm0.15_delta2_minnode_matrix)
tm0.15_delta3_minnode_plot <- plot_minnode_matrix(tm0.15_delta3_minnode_matrix)
tm0.15_delta23_minnode_plot <- plot_minnode_matrix(tm0.15_delta23_minnode_matrix)
tm0.3_delta2_minnode_plot <- plot_minnode_matrix(tm0.3_delta2_minnode_matrix)
tm0.3_delta3_minnode_plot <- plot_minnode_matrix(tm0.3_delta3_minnode_matrix)
tm0.3_delta23_minnode_plot <- plot_minnode_matrix(tm0.3_delta23_minnode_matrix)
tm0.45_delta2_minnode_plot <- plot_minnode_matrix(tm0.45_delta2_minnode_matrix)
tm0.45_delta3_minnode_plot <- plot_minnode_matrix(tm0.45_delta3_minnode_matrix)
tm0.45_delta23_minnode_plot <- plot_minnode_matrix(tm0.45_delta23_minnode_matrix)

minnode_plot <- grid.arrange(arrangeGrob(tm0.15_delta2_minnode_plot,
                                         top = "C into B", left = "0.15"),
                             arrangeGrob(tm0.15_delta3_minnode_plot,
                                         top = "B into C"),
                             arrangeGrob(tm0.15_delta23_minnode_plot,
                                         top = "Both"),
                             arrangeGrob(tm0.3_delta2_minnode_plot,
                                         left = "0.3"),
                             arrangeGrob(tm0.3_delta3_minnode_plot),
                             arrangeGrob(tm0.3_delta23_minnode_plot),
                             arrangeGrob(tm0.45_delta2_minnode_plot,
                                         left = "0.45"),
                             arrangeGrob(tm0.45_delta3_minnode_plot),
                             arrangeGrob(tm0.45_delta23_minnode_plot),
                             ncol = 3, top = "Direction of introgression",
                             left = "Timing of introgression")



