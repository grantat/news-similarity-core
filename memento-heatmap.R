library(ggplot2)

format_data <- function(dt){
  # format uri removing www
  dt$uri <- gsub("(www.)?", "", dt$uri)
  # swap from GMT to EST time
  dt$datetime <- as.POSIXct(dt$datetime, format='%Y-%m-%dT%H:%M:%S', tz="GMT")
  dt$datetime <- format(dt, tz="America/New_York")$datetime
  dt$datetime <- strptime(dt$datetime, format = '%Y-%m-%d %H:%M:%S')
  # Getting the day and hour of each memento pushed
  dt$weekday <- weekdays(as.Date(dt$datetime))
  dt$hour <- dt$datetime$hour
  dt
}

avg_times <- function(dailyMementos){
  # find average for each day
  temp <- data.frame(hour=double(), avg=double())
  for(i in unique(dailyMementos$Hour)){
    s <- subset(dailyMementos, Hour == i)
    m <- sum(s$Freq)
    avg <- m / length(unique(dailyMementos$uri))
    # print(paste("Hour",i, "avg =",floor(avg)))
    temp[nrow(temp) + 1,] = list(i, floor(avg))
  }
  print(temp[which.max(temp$avg),])
  # print(max(temp$V2))
}

make_plots <- function(dt, plot_title){
  dt <- as.data.frame(dt)
  dailyMementos <- as.data.frame(table(dt$uri, dt$hour))
  names(dailyMementos) <- c('uri', 'Hour', 'Freq')
  dailyMementos$Hour <- as.numeric(as.character(dailyMementos$Hour))
  dailyMementos$uri <- factor(dailyMementos$uri, ordered = TRUE, 
                              levels = unique(dt$uri))
  # Plotting the number of crimes each day (line graph)
  # linechart <- ggplot(dailyMementos, aes(x = Hour, y = Freq)) + geom_line(aes(group = uri, color = uri)) + xlab('Hour') + ylab('Number of Mementos') + ggtitle('Hourly count of Mementos created - November 2016')
  # print(linechart)
  # auto generate graph
  hmap <- ggplot(dailyMementos, aes(x = Hour, y = uri)) + geom_tile(aes(fill = Freq)) + scale_fill_gradient(name = 'Mementos created', low = 'white', high = 'red') + theme(axis.title.y = element_blank(), plot.title = element_text(hjust = 0.5)) + ggtitle(plot_title)
  print(hmap)

  dailyMementos
}

path = "./data/mementos-per-month/"
file.names <- dir(path, pattern =".csv")
pdf(paste("./docs/imgs/heatmaps/mementos-per-hour", ".pdf",sep = ""))
for(i in 1:length(file.names)){
  plot_title <- gsub('.{4}$', '', file.names[i])
  dt <- read.csv(paste(path, file.names[i], sep = ""), header = TRUE)
  print(plot_title)
  # data tables allow in place modification
  dt <- format_data(dt)
  dailyMementos <- make_plots(dt, plot_title)
  avg_times(dailyMementos)
  # break
}
dev.off()
