# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# Study data files
mouse_metadata_path = "Mouse_metadata.csv"
study_results_path = "Study_results.csv"

mouse_metadata = pd.read_csv(mouse_metadata_path)
study_results = pd.read_csv(study_results_path)



mergedDf = pd.merge(mouse_metadata, study_results, on="Mouse ID")
print('===============================================')

print(mergedDf.head(5).to_string())
miceCount=len(mergedDf['Mouse ID'].unique())
print('===============================================')

print("there are " + str(miceCount) + " mice")

duplicatesDf=mergedDf.loc[mergedDf.duplicated(subset=["Mouse ID", "Timepoint"]), "Mouse ID"].unique()


cleanDf = mergedDf[mergedDf["Mouse ID"].isin(duplicatesDf) == False]

print('===============================================')

print(cleanDf.head(5).to_string())

nonDuplicateCount = len(cleanDf["Mouse ID"].unique())

summaryDf = pd.DataFrame({
		   "Mean": cleanDf.groupby("Drug Regimen").mean()["Tumor Volume (mm3)"],
	       "Median": cleanDf.groupby("Drug Regimen").median()["Tumor Volume (mm3)"], 
	       "Variance": cleanDf.groupby("Drug Regimen").std()["Tumor Volume (mm3)"],
	       "Standard Dev.": cleanDf.groupby("Drug Regimen").var()["Tumor Volume (mm3)"],
	       "SEM": cleanDf.groupby("Drug Regimen").sem()["Tumor Volume (mm3)"]
	})
print('===============================================')

print(summaryDf.head(5))

#pretty nifty way to do all of the above by using the aggregate method
aggregatedSummary = cleanDf.groupby("Drug Regimen").agg({"Tumor Volume (mm3)":["mean","median","var","std","sem"]})
print('===============================================')
print(aggregatedSummary.head(5))

print('===============================================')

miceBargraph = cleanDf.groupby("Drug Regimen").count()["Mouse ID"]
miceBargraph.plot(kind ='bar')
plt.title("Treatments over the course of the study")
plt.show()
plt.bar(miceBargraph.index, miceBargraph.values, align="center")
plt.title("Treatments over the course of the study alternate example")

plt.show()
print('===============================================')


############

gender = cleanDf['Sex'].value_counts()
gender.plot(kind="pie", autopct='%1.1f%%')
plt.title('Male v. Female Population')
plt.show()

plt.pie(gender,labels = ['Males','Females'],autopct='%1.1f%%')
plt.title('Male v. Female Population')
plt.show()


tumors = cleanDf.groupby('Mouse ID').max()["Timepoint"].reset_index()

mergeDf = pd.merge(tumors[["Mouse ID","Timepoint"]],cleanDf,on=["Mouse ID","Timepoint"])
print(mergeDf.head(5))

print('===============================================')

drugs = ["Capomulin", "Ramicane", "Infubinol", "Ceftamin"]
tumorList = []
for drug in drugs:
	volume =  mergeDf.loc[mergeDf["Drug Regimen"]==drug]["Tumor Volume (mm3)"]
	tumorList.append(volume)
	quartiles = volume.quantile([.25,.5,.75])
	lower = quartiles[.25]
	upper = quartiles[.75]
	IQR = upper - lower
	lowOutliers = lower - (1.5*IQR)
	upperOultiers = upper -(1.5*IQR)
	print(drug + "has a IQR of " + str(IQR) + " and outliers above " 
		+ str(upperOultiers) + " and below " + str(lowOutliers) )
	print('===============================================')


fig1 = plt.subplots() 
plt.boxplot(tumorList)
plt.title("Tumor of volume compared to drug")
plt.ylabel('Tumor Volume')
plt.xlabel(drugs)
plt.show()

capomulinDf = cleanDf[cleanDf['Drug Regimen'] =='Capomulin']
y_axis = capomulinDf["Tumor Volume (mm3)"]
x_axis = capomulinDf["Timepoint"]
plt.xlabel("Timepoint")
plt.ylabel("Avg. Tumor Volume for Capomulin Treatments")
plt.plot(x_axis, y_axis)
plt.show()

mouseWeight = capomulinDf.groupby(['Mouse ID'])['Weight (g)'].mean()
tumorSize = capomulinDf.groupby(['Mouse ID'])['Tumor Volume (mm3)'].mean()
plt.scatter(mouseWeight,tumorSize)
plt.xlabel('Timepoints')
plt.ylabel('Mean Tumor size in capomulin trials')
plt.show()


capWeight = capomulinDf['Weight (g)']
capTumorVolume = capomulinDf["Tumor Volume (mm3)"]

capCorrelation = capWeight.corr(capTumorVolume)
print("The correlaiton is " + str(capCorrelation))

sns.regplot(x="Weight (g)", y="Tumor Volume (mm3)", data=capomulinDf)
plt.show()
