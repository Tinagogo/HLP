# Executive Report

## Problem and Data

The problem is to predict future default events based on static and dynamic data for client demographics and their historical records.

## Conclusions

1. Resampling (or other techniques) are necessary to address the imbalanced classification problem.
2. Dynamic features based on historical records are useful in predicting future default events.
3. The data quality and reliability is not perfect. More and better data might further improve the modeling performances or enable more advanced models.

# Data Engineering

## Data preprocessing

1. How to fix missing value, outliers, skewness, and misleading information?
2. Business insight from data exploration analysis

Details: [Features.ipynb](Features.ipynb)

## Labels

1. How to define 'good' or 'bad' clients according to the credit history?
2. Is there temporal dependency between default events? Yes.
3. Is the credit history a good feature for the credit risk prediction? Yes.

Details: [Labels.ipynb](Labels.ipynb)

# Model development 

1. How to solve the imbalance problem?
One solution is to resample the smaller class with replacement.
2. How to evaluate classification models performance in differenet settings?
3. How to develop dynamic features to improve the performance?

- Details: [Static Models](Static_Models.ipynb)
- Details: [Dynamic Models](Dynamic_Models.ipynb)

# Data Descriptions

File name: summary_application.csv

	Feature
	Description
	Comments

	ID
	Client number
	

	CODE_GENDER
	Gender
	

	FLAG_OWN_CAR
	Is there a car
	

	FLAG_OWN_REALTY
	Is there a property
	

	CNT_CHILDREN
	Number of children
	

	AMT_INCOME_TOTAL
	Annual income
	

	NAME_INCOME_TYPE
	Income category
	

	NAME_EDUCATION_TYPE
	Education level
	

	NAME_FAMILY_STATUS
	Marital status
	

	NAME_HOUSING_TYPE
	Way of living
	

	DAYS_BIRTH
	Birthday
	Count backwards from current day (0), -1 means yesterday

	DAYS_EMPLOYED
	Start date of employment
	Count backwards from current day(0). If positive, it means the person currently unemployed.

	FLAG_MOBIL
	Is there a mobile phone
	

	FLAG_WORK_PHONE
	Is there a work phone
	

	FLAG_PHONE
	Is there a phone
	

	FLAG_EMAIL
	Is there an email
	

	OCCUPATION_TYPE
	Occupation
	

	CNT_FAM_MEMBERS
	Family size



File name: summary_credit_history. csv

	Feature 
	Description
	Comments

	ID
	Client number
	

	MONTHS_BALANCE
	Record month
	The month of the extracted data is the starting point, backwards, 0 is the current month, -1 is the previous month, and so on

	STATUS
	Status
	0: 1-29 days past due 1: 30-59 days past due 2: 60-89 days overdue 3: 90-119 days overdue 4: 120-149 days overdue 5: Overdue or bad debts, write-offs for more than 150 days C: paid off that month X: No loan for the month

