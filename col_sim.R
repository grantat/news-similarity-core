library(ggplot2)
library(reshape2)

col_sim <- read.csv("data/col_sim_summary.csv", header = TRUE)
col_sim <- col_sim[order(col_sim$day),]
col_sim$date <- as.POSIXct(col_sim$date, format='%Y-%m-%d', tz="GMT")
col_sim$weekday <- weekdays(as.Date(col_sim$date))

# scatterplot
p <- ggplot(col_sim, aes(day)) + 
  xlab('Day') + ylab('Cosine/Entity Value') + 
  geom_point(aes(y = cosine, colour = "cosine")) + 
  geom_point(aes(y = entity, colour = "entity"))
print(p)

# grouped bar chart
# counts <- table(col_sim$cosine, col_sim$entity)
bLong <- melt(data          = col_sim,
              id.vars       = c("day"),
              measure.vars  = c("cosine","entity"),
              variable.name = "type",
              value.name    = "value")
p <- ggplot(bLong, aes(x = day, y = value, fill=factor(type))) + 
  xlab('Day') + ylab('Value') + 
  geom_bar(stat="identity",position="dodge") +
  facet_grid(type ~ .) +
  theme(legend.title=element_blank())
print(p)

# Line graph
p <- ggplot(col_sim, aes(x = day, label = weekday)) + 
  xlab('Day') + ylab('Value') + 
  geom_line(aes(y = cosine, colour = "cosine")) +
  geom_point(aes(y = cosine, colour = "cosine")) +
  # geom_text(aes(y = cosine, label=weekday), size = 3)
  geom_line(aes(y = entity, colour = "entity")) +
  geom_point(aes(y = entity, colour = "entity")) +
  # geom_text(aes(y = entity, label=weekday), size = 3)
  theme(legend.title=element_blank())
print(p)
