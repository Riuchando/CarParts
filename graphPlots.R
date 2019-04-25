rm(list = ls())

library("ggplot2")
library("reshape")
library("stringi")
library("dplyr")

setwd("/Users/stephenkinser/CarParts")
# not sure how to check length of the rows until after the fact
tires <- read.csv("tireInfo.csv", header = F, col.names = paste0("V", seq_len(12)))

# changing $345 -> 345
tires$Price = as.numeric(sub("$", "", as.character(tires$V2), fixed = TRUE))
tires$V2 = NULL

tires$Name = as.character(tires$V1)
tires$V1 = NULL

tires$company = gsub(x = tires$Name, pattern = "[a-zA-z]*[0-9]+(.|,|/|-|T)*", replace = "")

meanprice <- tapply(tires$Price, tires$company, mean)
ggplot(aes(x = Name, y = Price), data = tires) + geom_point() + facet_wrap(~company)
ggsave(filename = "tires.png")
# ggplot(aes(x=company , y= meanprice), data= tires)+geom_bar()
co <- factor(levels(as.factor(tires$company)), levels = levels(as.factor(tires$company)))
qplot(co, meanprice, geom = "bar", stat = "identity", fill = I("grey50"))
ggsave(filename = "meanPrice.png")
qplot(Name, Price, data = tires, geom = "bar", stat = "identity", fill = I("grey50")) + facet_wrap(~company)
ggsave("whatIwanted.png")

meltedDataSet = melt(tires, id = c("Price", "Name", "company"))
meltedDataSet$value = as.character(meltedDataSet$value)
# meltedDataSet[as.character(meltedDataSet$value)=="","value"]=NA
meltedDataSet = meltedDataSet[!(meltedDataSet$value == ""),]
meltedDataSet$value
grep("Max Load", meltedDataSet$value)

tireWeightAV = meltedDataSet[grep("Tire Weight", meltedDataSet$value), "value"]
tireWeightBucket = meltedDataSet[grep("Tire Weight", meltedDataSet$value), "Name"]
tires[tires$Name %in% tireWeightBucket, "TireWeight"] = gsub("Tire Weight:", "", tireWeightAV)
qplot(TireWeight, Price, data = !is.na(tires), geom = "bar", stat = "identity", fill = I("grey50")) + facet_wrap(~company)


grep("Rim Range", meltedDataSet$value)
grep("Terrain", meltedDataSet$value)
grep("Tread Wear Warranty", meltedDataSet$value)
grep("Speed Rating", meltedDataSet$value)
grep("Load Range", meltedDataSet$value)
grep("Overall Diameter", meltedDataSet$value)
grep("Tread Depth", meltedDataSet$value)
grep("Approved Rim", meltedDataSet$value)
grep("Outlined White Letter", meltedDataSet$value)
grep("Black Side Wall", meltedDataSet$value)
tireSizeAV = meltedDataSet[grep("[0-9][0-9]x[0-9][0-9]", meltedDataSet$value), "value"]
tireSize = meltedDataSet[grep("[0-9][0-9]x[0-9][0-9]", meltedDataSet$value), "Name"]

# first gsub gets rid of values ending in 0
# second gsub get rid of spaces
# third gsub is getting rid of values ending with -numbernumber OR Rnumbernumber
# last gsub gets rid of Tire Size
tires[tires$Name %in% tireSize, "TireSize"] = gsub("0$", "",
                                                gsub(" ", "",
                                                     gsub("-[0-9][0-9]|R[0-9][0-9]", "",
                                                          gsub("Tire Size:", "", tireSizeAV))))



# order= !is.na(as.numeric(stri_extract_first_regex(str=tires$TireSize, pattern="[0-9][0-9]")))
qplot(x = TireSize, y = Price, data = subset(tires, !is.na(TireSize)),
      geom = "point", stat = "unique", fill = I("grey50")) +
      facet_wrap(~company)

ggsave("accordingTotireSize.png")

group_by(tires, TireSize)
# qplot(TireSize, Price, data=  sort(subset(tires,!is.na(TireSize))[,"TireSize"]), 
#      geom="bar",stat= "identity",fill= I("grey50"))+ 
#       facet_wrap( ~company)

qplot(TireSize, Price, data = group_by(subset(tires, !is.na(TireSize)), TireSize),
            geom = "bar", stat = "identity", fill = I("grey50")) +
             facet_wrap(~company)
max(subset(tires, !is.na(TireSize))["TireSize", "Name"])
