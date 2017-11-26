library(ggplot2)

dt <- read.csv("data/hour-counts.csv", header = TRUE)

# swap from GMT to EST time
dt$datetime <- as.POSIXct(dt$datetime, format='%Y-%m-%dT%H:%M:%S', tz="GMT")
dt$datetime <- format(dt, tz="America/New_York")$datetime
dt$datetime <- strptime(dt$datetime, format = '%Y-%m-%d %H:%M:%S')
# Getting the day and hour of each memento pushed
dt$weekday <- weekdays(as.Date(dt$datetime))
dt$hour <- dt$datetime$hour
# Sorting the weekdays
dailyMementos <- as.data.frame(table(dt$uri, dt$hour))
names(dailyMementos) <- c('uri', 'Hour', 'Freq')
dailyMementos$Hour <- as.numeric(as.character(dailyMementos$Hour))
dailyMementos$uri <- factor(dailyMementos$uri, ordered = TRUE, 
                            levels = unique(dt$uri))
# Plotting the number of crimes each day (line graph)
linechart <- ggplot(dailyMementos, aes(x = Hour, y = Freq)) + geom_line(aes(group = uri, color = uri)) + xlab('Hour') + ylab('Number of Mementos') + ggtitle('Hourly count of Mementos created - November 2016')
# auto generate graph
print(linechart)

hmap <- ggplot(dailyMementos, aes(x = Hour, y = uri)) + geom_tile(aes(fill = Freq)) + scale_fill_gradient(name = 'Mementos created', low = 'white', high = 'red') + theme(axis.title.y = element_blank())
print(hmap)