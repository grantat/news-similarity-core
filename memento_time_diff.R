library(tidyverse)
library(ggplot2)

dt <- read.csv("data/parsed_links/headline-counts.csv", header = TRUE)
# remove wsj
dt <- dt[dt$uri != "www.wsj.com", ]
# format uri removing www
dt$uri <- gsub("(www.)?", "", dt$uri)

dailyMementos <- as.data.frame(dt)
dailyMementos$headline_count <- as.numeric(dailyMementos$headline_count)
dailyMementos$day <- as.POSIXct(dailyMementos$day, format='%Y-%m-%d', tz="GMT")
dailyMementos$uri <- factor(dailyMementos$uri, ordered = TRUE, 
                            levels = unique(dt$uri))
dailyMementos <- subset(dailyMementos, months(day) == "November" | months(day) == "December" | months(day) == "January")
## Add a column indicating what days to highlight
# dailyMementos <- dailyMementos %>% mutate( ToHighlight = ifelse( months(day) == "November", "yes", "no" ) )
# Plotting the number of headlines each day (line graph)
p <- ggplot(dailyMementos, aes(x = as.Date(day), y = headline_count)) + 
  # geom_point(aes(group = uri, color = uri)) + 
  geom_bar(stat = "identity") +
  xlab('Day') + ylab('Number of stories') + 
  # ggtitle('Total count of stories found') +
  # scale_fill_manual( values = c( "yes"="black", "no"="black" ), guide = FALSE ) +
  scale_y_continuous(breaks=c(0,5,10)) +
  theme(plot.title = element_text(hjust = 0.5))
p <- p + facet_wrap(~uri, ncol = 2)
# auto generate graph
print(p)

# Add weekdays to data frame
# for(i in 1:nrow(dailyMementos)){
#   date <- paste("2016", "11", sprintf("%02d", dailyMementos[i, "day"]), sep="-")
#   date <- as.POSIXct(date, format='%Y-%m-%d', tz="GMT")
#   dailyMementos[i, "weekday"] <- weekdays(as.Date(date))
# }

times <- read.csv("data/mementos/memento-times.csv", header = TRUE)
# remove wsj
times <- times[times$uri != "www.wsj.com", ]
# format uri removing www
times$uri <- gsub("(www.)?", "", times$uri)
times$actual_datetime <- as.POSIXct(times$actual_datetime, format='%a, %d %b %Y %H:%M:%S GMT', tz="GMT")
times$request_datetime <- as.POSIXct(times$request_datetime, format='%Y-%m-%dT%H:%M:%S', tz="GMT")
times <- subset(times, months(request_datetime) == "November" | months(request_datetime) == "December" | months(request_datetime) == "January")

# time difference in minutes to one significant figure
times$diff <- difftime(times$actual_datetime, times$request_datetime, units = "min")
# convert day to factor
dailyTimes <- as.data.frame(times)
# dailyTimes$day <- as.numeric(as.character(dailyTimes$day))
dailyTimes$diff <- as.numeric(dailyTimes$diff)
dailyTimes$uri <- factor(dailyTimes$uri, ordered = TRUE, 
                            levels = unique(times$uri))

# Plotting the number of headlines each day (bar graph)
time_plot <- ggplot(dailyTimes, aes(x = actual_datetime, y = diff)) + 
  geom_point() + 
  # scale_y_continuous(trans='log10') +
  xlab('Day') + ylab('Time Difference (Minutes)') + 
  ggtitle('Memento Request vs. Actual timestamps - 1AM GMT') +
  geom_text(aes(label=ifelse(diff>250 | diff < -250,as.character(uri),'')),hjust=-0.05,vjust=0) +
  theme(plot.title = element_text(hjust = 0.5))
  # scale_x_continuous(breaks = round(seq(min(dailyTimes$day), max(dailyTimes$day), by = 1),1)) 
# auto generate graph
print(time_plot)

# Boxplot for time differences in memento request time and actual memento time
bplot <- ggplot(dailyTimes, aes(x = uri, y = diff)) + 
  geom_boxplot() + 
  xlab('URI') + ylab('Time Difference (Minutes)') + 
  theme(axis.text.x = element_text(angle = 60, hjust = 1))
print(bplot)
