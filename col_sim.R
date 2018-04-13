library(ggplot2)
library(reshape2)
library(ggradar)
library(scales)

col_sim <- read.csv("data/col_sim/col_sim_summary.csv", header = TRUE)
col_sim <- col_sim[order(col_sim$k_val),]
# add 1am to each of these mementos
col_sim$date <- paste(col_sim$date, " 01:00:00")
col_sim$date <- as.POSIXct(col_sim$date, format='%Y-%m-%d', tz="GMT")
# convert to EST time
col_sim$date <- format(col_sim$date, tz="America/New_York", usetz=TRUE)
# col_sim$date <- strptime(col_sim$date, format = '%Y-%m-%d %H:%M:%S')
col_sim$date <- strptime(col_sim$date, format = '%Y-%m-%d')
col_sim$weekday <- weekdays(as.Date(col_sim$date))
col_sim$date <- as.character(col_sim$date)

# scatterplot
# p <- ggplot(col_sim, aes(date)) + 
#   xlab('Day') + ylab('Cosine/Entity Value') + 
#   geom_point(aes(y = cosine, colour = "cosine")) + 
#   geom_point(aes(y = entity, colour = "entity"))
# print(p)

# helper function for ggplot to return string as date type
str_to_date <- function(x){
  as.Date(strptime(x, format = '%Y/%m/%d'))
}

# helper function for finding date position on facet grid
find_date_pos <- function(x, k_val, type){
  bLong[which(as.Date(bLong$date) == str_to_date(x) & bLong$k_val == k_val & bLong$type == type), ]
}

# helper function for ggplot to return entity value given a date string
find_ent_val <- function(x, k_val, type){
  bLong[which(as.Date(bLong$date) == str_to_date(x) & bLong$k_val == k_val & bLong$type == type), ]
}

# helper function to return all points for a given date and similarity type
find_all_dates <- function(x, type){
  bLong[which(as.Date(bLong$date) == str_to_date(x) & bLong$type == type), ]
}

# grouped bar chart
# counts <- table(col_sim$cosine, col_sim$entity)
bLong <- melt(data          = col_sim,
              id.vars       = c("k_val","date"),
              measure.vars  = c("cosine","entity"),
              variable.name = "type",
              value.name    = "value")
bLong$k_val_facet_order = factor(col_sim$k_val, levels=c('k1','k3','k10'))
p <- ggplot(bLong, aes(x = as.Date(date), y = value, fill=factor(type))) + 
  xlab('Day') + ylab('Similarity') + 
  geom_bar(stat="identity",position="dodge") +
  facet_grid(type ~ k_val_facet_order) +
  scale_x_date(date_labels = "%b %d") +
  theme(legend.title=element_blank())
print(p)

bLong <- subset(bLong, type == "cosine")

# Line graph facet - -2.75
p <- ggplot(bLong, aes(x = as.Date(date), y = value)) + 
  xlab('Day') + ylab('Similarity') + 
  geom_line(stat="identity",position="dodge") +
  facet_grid( ~ k_val_facet_order) +
  scale_x_date(date_labels = "%b %d") +
  theme(legend.title=element_blank()) +
  # Election day
  geom_text(data = find_all_dates("2016/11/08", "cosine"),
            aes(x = as.Date(date), y = max(bLong$value),
                label=" a", hjust=0,vjust=0.0, colour = "red", size = 1.2), check_overlap = FALSE) +
  geom_point(data = find_all_dates("2016/11/08", "cosine"),
             aes(x = as.Date(date), y = value), colour="red", size=0.9) +
  geom_vline(xintercept = as.numeric(as.Date(find_all_dates("2016/11/08", "cosine")$date)), linetype = 3, colour = "red") +
  # # Thanksgiving
  geom_text(data = find_all_dates("2016/11/24", "cosine"),
            aes(x = as.Date(date), y = max(bLong$value),
                label=" b", hjust=0,vjust=0.0, colour = "red", size = 1.2), check_overlap = FALSE) +
  geom_point(data = find_all_dates("2016/11/24", "cosine"),
             aes(x = as.Date(date), y = value), colour="red", size=0.9) +
  geom_vline(xintercept = as.numeric(as.Date(find_all_dates("2016/11/24", "cosine")$date)), linetype = 3, colour = "red") +
  # # Christmas
  geom_text(data = find_all_dates("2016/12/25", "cosine"),
            aes(x = as.Date(date), y = max(bLong$value),
                label=" c", hjust=0,vjust=0.0, colour = "red", size = 1.2), check_overlap = FALSE) +
  geom_point(data = find_all_dates("2016/12/25", "cosine"),
             aes(x = as.Date(date), y = value), colour="red", size=0.9) +
  geom_vline(xintercept = as.numeric(as.Date(find_all_dates("2016/12/25", "cosine")$date)), linetype = 3, colour = "red") +
  # # Travel ban
  geom_text(data = find_all_dates("2017/01/27", "cosine"),
            aes(x = as.Date(date), y = max(bLong$value),
                label=" d", hjust=0,vjust=0.0, colour = "red", size = 1.2), check_overlap = FALSE) +
  geom_point(data = find_all_dates("2017/01/27", "cosine"),
             aes(x = as.Date(date), y = value), colour="red", size=0.9) +
  geom_vline(xintercept = as.numeric(as.Date(find_all_dates("2017/01/27", "cosine")$date)), linetype = 3, colour = "red") +
  theme(legend.position="none")
print(p)

# Line graph
p <- ggplot(col_sim, aes(x = as.Date(date), label = weekday)) + 
  scale_x_date(labels = date_format("%m/%d")) +
  xlab('Day') + ylab('Similarity') + 
  geom_line(aes(y = cosine, colour = "cosine")) +
  geom_point(aes(y = cosine, colour = "cosine")) +
  # geom_text(aes(y = cosine, label=weekday), size = 3) +
  geom_line(aes(y = entity, colour = "entity")) +
  geom_point(aes(y = entity, colour = "entity")) +
  # geom_text(aes(y = entity, label=weekday), size = 3) +
  # mark points with events
  # geom_text(aes(y = find_ent_val("2016/11/08"), x=str_to_date("2016/11/08"),label="Election Day", hjust=0,vjust=0), check_overlap = TRUE) +
  # geom_text(aes(y = find_ent_val("2016/11/11"), x=str_to_date("2016/11/11"),label="Veterans Day",hjust=0,vjust=1.0), check_overlap = TRUE) +
  # geom_text(aes(y = find_ent_val("2016/11/24"), x=str_to_date("2016/11/24"),label="Thanksgiving Day", hjust=0,vjust=0), check_overlap = TRUE) +
  theme_minimal() +
  theme(legend.title=element_blank())
# print(p)

# Line graph with days of the week
# cosine
p <- ggplot(col_sim, aes(x = date, label = weekday)) + 
  xlab('Day') + ylab('Similarity') + 
  geom_line(aes(y = cosine, colour = "cosine")) +
  geom_point(aes(y = cosine, colour = "cosine")) +
  geom_text(aes(y = cosine, label=weekday), size = 3) +
  theme(legend.title=element_blank())
# print(p)
# entity
p <- ggplot(col_sim, aes(x = date, label = weekday)) + 
  xlab('Day') + ylab('Similarity') + 
  geom_line(aes(y = entity, colour = "entity")) +
  geom_point(aes(y = entity, colour = "entity")) +
  geom_text(aes(y = entity, label=weekday), size = 3) +
  theme(legend.title=element_blank())
# print(p)

# Radarplot for day of the weeks
# Add weekdays to data frame
# for(i in 1:nrow(dailyMementos)){
#   date <- paste("2016", "11", sprintf("%02d", dailyMementos[i, "day"]), sep="-")
#   date <- as.POSIXct(date, format='%Y-%m-%d', tz="GMT")
#   dailyMementos[i, "weekday"] <- weekdays(as.Date(date))
# }
# days <- unique(col_sim$weekday)

# average cosine/entity values
# mean(col_sim$cosine[col_sim$weekday=="Sunday"])
# ggradar(dm_radar)
# cos_sim_radar <- dcast(bLong, type~weekday, value.var = "value", fun.aggregate = mean)

# rdar <- ggradar(cos_sim_radar, font.radar = "Times",
#         values.radar = c("0.0", "0.12", "0.25"),
#         # plot.title="Mean Similarity per Weekday",
#         grid.min=0,
#         grid.mid=0.12,
#         grid.max=0.25,
#         axis.label.size=3,
#         grid.label.size=3,
#         legend.text.size=8)
# print(rdar)

# Stats: Max, Min, Mean
cat(paste(max(subset(bLong, k_val == "k1")$value), max(subset(bLong, k_val == "k3")$value), max(subset(bLong, k_val == "k10")$value)))
cat(paste(min(subset(bLong, k_val == "k1")$value), min(subset(bLong, k_val == "k3")$value), min(subset(bLong, k_val == "k10")$value)))
cat(paste(mean(subset(bLong, k_val == "k1")$value), mean(subset(bLong, k_val == "k3")$value), mean(subset(bLong, k_val == "k10")$value)))
