library(ggplot2)
library(reshape2)
library(ggradar)
library(scales)

col_sim <- read.csv("data/col_sim/k3/2016_11-old/col_sim_summary.csv", header = TRUE)
col_sim <- col_sim[order(col_sim$day),]
# add 1am to each of these mementos
col_sim$date <- paste(col_sim$date, " 01:00:00")
col_sim$date <- as.POSIXct(col_sim$date, format='%Y-%m-%d', tz="GMT")
# convert to EST time
col_sim$date <- format(col_sim$date, tz="America/New_York", usetz=TRUE)
col_sim$date <- strptime(col_sim$date, format = '%Y-%m-%d %H:%M:%S')
col_sim$weekday <- weekdays(as.Date(col_sim$date))

# scatterplot
# p <- ggplot(col_sim, aes(day)) + 
#   xlab('Day') + ylab('Cosine/Entity Value') + 
#   geom_point(aes(y = cosine, colour = "cosine")) + 
#   geom_point(aes(y = entity, colour = "entity"))
# print(p)

# helper function for ggplot to return string as date type
str_to_date <- function(x){
  as.Date(strptime(x, format = '%Y/%m/%d'))
}

# helper function for ggplot to return entity value given a date string
find_ent_val <- function(x){
  col_sim[which(as.Date(col_sim$date) == str_to_date(x)), ]$entity
}

# grouped bar chart
# counts <- table(col_sim$cosine, col_sim$entity)
bLong <- melt(data          = col_sim,
              id.vars       = c("day", "weekday"),
              measure.vars  = c("cosine","entity"),
              variable.name = "type",
              value.name    = "value")
p <- ggplot(bLong, aes(x = day, y = value, fill=factor(type))) + 
  xlab('Day') + ylab('Similarity') + 
  geom_bar(stat="identity",position="dodge") +
  facet_grid(type ~ .) +
  theme(legend.title=element_blank())
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
  geom_text(aes(y = find_ent_val("2016/11/08"), x=str_to_date("2016/11/08"),label="Election Day", hjust=0,vjust=0), check_overlap = TRUE) +
  geom_text(aes(y = find_ent_val("2016/11/11"), x=str_to_date("2016/11/11"),label="Veterans Day",hjust=0,vjust=1.0), check_overlap = TRUE) +
  geom_text(aes(y = find_ent_val("2016/11/24"), x=str_to_date("2016/11/24"),label="Thanksgiving Day", hjust=0,vjust=0), check_overlap = TRUE) +
  theme_minimal() +
  theme(legend.title=element_blank())
print(p)

# Line graph with days of the week
# cosine
p <- ggplot(col_sim, aes(x = day, label = weekday)) + 
  xlab('Day') + ylab('Similarity') + 
  geom_line(aes(y = cosine, colour = "cosine")) +
  geom_point(aes(y = cosine, colour = "cosine")) +
  geom_text(aes(y = cosine, label=weekday), size = 3) +
  theme(legend.title=element_blank())
print(p)
# entity
p <- ggplot(col_sim, aes(x = day, label = weekday)) + 
  xlab('Day') + ylab('Similarity') + 
  geom_line(aes(y = entity, colour = "entity")) +
  geom_point(aes(y = entity, colour = "entity")) +
  geom_text(aes(y = entity, label=weekday), size = 3) +
  theme(legend.title=element_blank())
print(p)

# Radarplot for day of the weeks
# Add weekdays to data frame
# for(i in 1:nrow(dailyMementos)){
#   date <- paste("2016", "11", sprintf("%02d", dailyMementos[i, "day"]), sep="-")
#   date <- as.POSIXct(date, format='%Y-%m-%d', tz="GMT")
#   dailyMementos[i, "weekday"] <- weekdays(as.Date(date))
# }
days <- unique(col_sim$weekday)

# average cosine/entity values
# mean(col_sim$cosine[col_sim$weekday=="Sunday"])
# ggradar(dm_radar)
cos_sim_radar <- dcast(bLong, type~weekday, value.var = "value", fun.aggregate = mean)

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

