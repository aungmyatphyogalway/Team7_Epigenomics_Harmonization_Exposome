install.packages("haven")
install.packages("dplyr")
library(haven)
library(dplyr)

#load xpt files
demograph <- read_xpt("~/Downloads/P_DEMO.xpt.txt")
diet_interview <- read_xpt("~/Downloads/P_DR1IFF.xpt.txt")
physical_activity<- read_xpt("~/Downloads/P_PAQ.xpt.txt")

##Extract
## gender and age
demograph <- demograph[, c(1, 4, 5)]
diet<- diet_interview[, c(1,7,13,16, 20:84)]
rm(diet_interview)
physical_activity<- physical_activity[, c(1,2,11)]

#remove missing data
table(demograph$RIAGENDR, useNA = "always")
table(demograph$RIDAGEYR, useNA = "always")

table(physical_activity$PAQ605, useNA = "always")
physical_activity$PAQ605[physical_activity$PAQ605 %in% c(7,9)] <- NA
physical_activity <- physical_activity %>%
  filter(!is.na(physical_activity$PAQ605))

table(diet$DR1FS, useNA = "always")
diet$DR1FS[diet$DR1FS == 99] <- NA
diet <- diet %>%
  filter(!is.na(diet$DR1FS))

table(diet$DR1FS, useNA = "always")
diet$DR1FS[diet$DR1FS == 99] <- NA
diet <- diet %>%
  filter(!is.na(diet$DR1FS))

table(diet$DR1IKCAL, useNA = "always")
diet <- diet %>%
  filter(!is.na(diet$DR1IKCAL))

table(diet$DR1IPROT, useNA = "always")
diet <- diet %>%
  filter(!is.na(diet$DR1IPROT))

testing <- inner_join(demograph, physical_activity, by = "SEQN")
testing2<- inner_join(testing, diet, by= "SEQN")
table(testing2$PAQ650, useNA = "always")

test_data<- testing2
table(test_data$DR1ISELE, useNA = "always")

#change to category data
lvl.001<- c(1,2)
lbl.001<- c("Male", "Female")
test_data$RIAGENDR<- ordered(test_data$RIAGENDR, levels=lvl.001, labels=lbl.001)
test_data <- test_data %>%
  rename(sex = RIAGENDR)
#vigorous work activity
lvl.002<- c(1,2)
lbl.002<- c("Yes", "No")
test_data$PAQ605<- ordered(test_data$PAQ605, levels=lvl.002, labels=lbl.002)
test_data <- test_data %>%
  rename(vigorous_work_activity= PAQ605)
test_data$PAQ650<- ordered(test_data$PAQ650, levels=lvl.002, labels=lbl.002)
test_data <- test_data %>%
  rename(vigorous_recreational_activity= PAQ650)

test_data$DRABF<- ordered(test_data$DRABF, levels=lvl.002, labels=lbl.002)
test_data <- test_data %>%
  rename(breast_fed_infant= DRABF)

lvl.003<- c(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,90)
lbl.003<- c("no combination food", "beverage", "cereal", "bread", "salad", "sandwich", "soup", "frozen meals",
            "ice cream", "dried beans and vetgetable","fruit", "tortilla","meat", "lunchables", "chips", "other")
test_data$DR1CCMTX<- ordered(test_data$DR1CCMTX, levels=lvl.003, labels=lbl.003)
test_data <- test_data %>%
  rename(combination_food_type= DR1CCMTX)

lvl.004<- c(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,24,25,26,27,28,91)
lbl.004<- c("grocery", "restaurant with waiter", "fast food", "bar", "restaurant", "cafeteria not k12 school",
            "cafeteria k12", "child care center", "child home care", "food pantry", "meals on wheels",
            "community food program", "community program", "vending machine", "snack tray", "gift", "mall order purchase",
            "residential dining", "grown by someone", "fish caught", "sport facility", "vending truck", "fundraiser",
            "store convience", "store", "other")
test_data$DR1FS<- ordered(test_data$DR1FS, levels=lvl.004, labels=lbl.004)
test_data <- test_data %>%
  rename(source_of_food= DR1FS)

write.csv(test_data, file = "exposome_data.csv", row.names = FALSE)
