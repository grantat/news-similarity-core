library(ggplot2)

format_data <- function(dt){
  # format uri removing www
  dt$uri <- gsub("(www.)?", "", dt$uri)
  dt <- dt[!(dt$uri == "wsj.com"),]
  # freq <- ave(rep(1, times=nrow(dt)), dt$uri, FUN=sum)
  # dt[order(freq, dt$uri, decreasing = TRUE), ]
    # swap from GMT to EST time
  dt$datetime <- as.POSIXct(dt$datetime, format='%Y-%m-%dT%H:%M:%S', tz="GMT")
  dt$datetime <- format(dt, tz="America/New_York")$datetime
  dt$datetime <- strptime(dt$datetime, format = '%Y-%m-%d %H:%M:%S')
  # Getting the day and hour of each memento pushed
  dt$weekday <- weekdays(as.Date(dt$datetime))
  dt$month <- months(as.Date(dt$datetime))
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
  print(temp[which.min(temp$avg),])
  # print(max(temp$V2))
}

# count_mementos_per_uri <- function(dt){
#   # find average for each day
#   temp <- data.frame(hour=double(), avg=double())
#   for(i in unique(dt$)){
#     s <- subset(dailyMementos, Hour == i)
#     m <- sum(s$Freq)
#     avg <- m / length(unique(dailyMementos$uri))
#     # print(paste("Hour",i, "avg =",floor(avg)))
#     temp[nrow(temp) + 1,] = list(i, floor(avg))
#   }
#   print(temp[which.max(temp$avg),])
#   # print(max(temp$V2))
# }

make_plots <- function(dt, plot_title){
  dt <- as.data.frame(dt)
  dailyMementos <- as.data.frame(table(dt$uri, dt$hour))
  names(dailyMementos) <- c('uri', 'Hour', 'Freq')
  dailyMementos$Hour <- as.numeric(as.character(dailyMementos$Hour))
  dailyMementos$uri <- factor(dailyMementos$uri,  
                              levels = unique(dt$uri))
  # Plotting the number of crimes each day (line graph)
  # linechart <- ggplot(dailyMementos, aes(x = Hour, y = Freq)) + geom_line(aes(group = uri, color = uri)) + xlab('Hour') + ylab('Number of Mementos') + theme(plot.title = element_text(hjust = 0.5)) + ggtitle(plot_title)
  # print(linechart)
  # auto generate graph
  hmap <- ggplot(dailyMementos, aes(x = Hour, y = uri)) + geom_tile(aes(fill = Freq)) +
    scale_fill_gradient(name = 'Mementos created', low = 'white', high = 'red') + 
    theme(axis.title.y = element_blank(), plot.title = element_text(hjust = 0.5)) + 
    # scale_x_discrete(labels = c("0" = "12AM", "5" = "5AM", "10" = "10AM", "15" = "3PM", "20" = "8PM")) +
    scale_x_continuous(breaks=c(0,5,10,15,20), labels=c("12AM", "5AM", "10AM", "3PM", "8PM")) +
    ggtitle(plot_title)
  print(hmap)

  dailyMementos
}

path = "./data/mementos-per-month/"
file.names <- dir(path, pattern =".csv")
# pdf(paste("./docs/imgs/mementos/mementos-per-hour-line-graph", ".pdf",sep = ""))
for(i in 1:length(file.names)){
  plot_title <- gsub('.{4}$', '', file.names[i])
  cat(paste(plot_title, "\n"))
  dt <- read.csv(paste(path, file.names[i], sep = ""), header = TRUE)
  print(plot_title)
  # data tables allow in place modification
  dt <- format_data(dt)
  dailyMementos <- make_plots(dt, plot_title)
  avg_times(dailyMementos)
  break
}
# dev.off()

# 
# Stats per months
# 
temp <- read.csv("./data/mementos-per-month/3months.csv")
temp <- format_data(temp)
temp <- subset(temp, month == "November" | month == "December" | month == "January")
dailyMementos <- make_plots(temp, "")
avg_times(dailyMementos)
# 
# for(i in unique(temp$uri)){
#   cat(paste("URI",i,"&",sum(temp$uri == i),"\n"))
# }
