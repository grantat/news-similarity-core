library(ggplot2)

dt <- read.csv("data/headline-counts.csv", header = TRUE)
# remove wsj
dt <- dt[dt$uri != "www.wsj.com", ]

dailyMementos <- as.data.frame(dt)
dailyMementos$headline_count <- as.numeric(dailyMementos$headline_count)
dailyMementos$day <- as.numeric(as.character(dailyMementos$day))
dailyMementos$uri <- factor(dailyMementos$uri, ordered = TRUE, 
                            levels = unique(dt$uri))
# Plotting the number of headlines each day (line graph)
p <- ggplot(dailyMementos, aes(x = day, y = headline_count)) + 
  # geom_point(aes(group = uri, color = uri)) + 
  geom_bar(stat = "identity") +
  xlab('Day') + ylab('Number of stories') + 
  ggtitle('Total count of stories found - 1AM GMT - November 2016 ') +
  theme(plot.title = element_text(hjust = 0.5))
# p <- p + facet_wrap(~uri, ncol = 2)
# auto generate graph
print(p)

times <- read.csv("data/memento-times.csv", header = TRUE)
# remove wsj
times <- times[times$uri != "www.wsj.com", ]
times$actual_datetime <- as.POSIXct(times$actual_datetime, format='%a, %d %b %Y %H:%M:%S GMT', tz="GMT")
times$request_datetime <- as.POSIXct(times$request_datetime, format='%Y-%m-%dT%H:%M:%S', tz="GMT")

# time difference in minutes to one significant figure
times$diff <- difftime(times$actual_datetime, times$request_datetime, units = "min")
# convert day to factor
dailyTimes <- as.data.frame(times)
dailyTimes$day <- as.numeric(as.character(dailyTimes$day))
dailyTimes$diff <- as.numeric(dailyTimes$diff)
dailyTimes$uri <- factor(dailyTimes$uri, ordered = TRUE, 
                            levels = unique(times$uri))

# Plotting the number of headlines each day (line graph)
time_plot <- ggplot(dailyTimes, aes(x = day, y = diff)) + 
  geom_point() + 
  scale_y_continuous(trans='log10') +
  xlab('Day') + ylab('Time Difference (Minutes)') + 
  ggtitle('Request vs. Actual timestamps - 1AM GMT - November 2016 ') + 
  geom_text(aes(label=ifelse(diff>100 | diff < -100,as.character(uri),'')),hjust=-0.05,vjust=0,) 
  # scale_x_continuous(breaks = round(seq(min(dailyTimes$day), max(dailyTimes$day), by = 1),1)) 
# auto generate graph
print(time_plot)
