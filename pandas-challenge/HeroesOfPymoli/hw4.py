 # Dependencies and Setup
import pandas as pd
data = pd.read_csv('purchase_data.csv')

########################################
summary = pd.DataFrame({"Items": [data['Item Name'].nunique()],
	"Price": [round(data['Price'].mean(),2)],
	"Count": [data['Purchase ID'].count()],
	"Revenue":[data['Price'].sum()]
	})
playerCount = data['SN'].nunique()
########################################
genderValues =  data.groupby('Gender')
genderCount = genderValues['SN'].nunique()
genderPercent = round(genderCount/playerCount*100,2)
gender = pd.DataFrame({"Total Count":genderCount,
	"Percentage":genderPercent
	})
########################################
purchasesByGender = genderValues["Purchase ID"].count()
avgPrice = round(genderValues["Price"].mean(),2)
totalAvg = round(genderValues["Price"].sum(),2)
averagePerPersonByGender = round(totalAvg/genderCount,2)
genderPurchases = pd.DataFrame({"Purchase Count":purchasesByGender,
	"Average Purchase Price":avgPrice,
	"Total Purchase Value":totalAvg,
	"Average Total Purchase per Person":averagePerPersonByGender
	})
########################################
ageRanges = ageRanges = [0, 9, 14, 19, 24, 29, 34, 39, 99999]
rangeLabels = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]
data["Age Group"] = pd.cut(data["Age"],ageRanges, labels=rangeLabels)
ageGroup = data.groupby("Age Group")
ageCount = ageGroup["SN"].nunique()
agePrecentage = (ageCount/playerCount) * 100
age_distribution = pd.DataFrame({"Percentage of Players": agePrecentage, 
	"Total Count": ageCount
	})
########################################
purchaseCountByAge = ageGroup['Purchase ID'].count()
avgPricebyAge = round(ageGroup['Price'].mean(),2)
totalAgePurchase = round(ageGroup['Price'].sum(),2)
avgPerPersonByAge = round(totalAgePurchase/ageCount,2)
age_purchases = pd.DataFrame({"Purchase Count": purchaseCountByAge,
                 "Average Purchase Price": avgPricebyAge,
                 "Total Purchase Value":totalAgePurchase,
                 "Average Purchase Total per Person": avgPerPersonByAge
                 })
########################################
spendingGroup = data.groupby('SN')
spendingCount = spendingGroup['Purchase ID'].count()	
avgPriceSpent = round(spendingGroup['Price'].mean(),2)
totalSpending = round(spendingGroup['Price'].sum(),2)
Top_Spenders = pd.DataFrame({"Purchase Count": spendingCount,
             "Average Purchase Price": avgPriceSpent,
             "Total Purchase Value":totalSpending
			 })
########################################
itemsGroup = data.groupby(['Item ID','Item Name'])
itemsCount = itemsGroup['Price'].count()
itemsValue = round(itemsGroup['Price'].sum()/itemsCount,2)
itemPrice = itemsGroup['Price'].sum()
popularItems = pd.DataFrame({"Purchase Count": itemsCount, 
                             "Item Price": itemsValue,
                             "Total Purchase Value":itemPrice
							})

########################################
print("-----------------")
print("Player Count " + str(playerCount))
print("-----------------")
print(summary)
print("-----------------")
print(gender)
print("-----------------")
print(genderPurchases.to_string())
print("-----------------")
print(age_distribution)
print("-----------------")
print(age_purchases.to_string())
print(Top_Spenders.sort_values(by='Total Purchase Value',ascending=False).head(5))
print(popularItems.sort_values(by='Purchase Count',ascending=False).head(5).to_string())
print(popularItems.sort_values(by='Total Purchase Value',ascending=False).head(5).to_string())


