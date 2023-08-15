# Final-Project-Financial-Analysis
Final project for the Lighthouse Labs Data Science Bootcamp. Business information is collected via API, organized into a database, and analyzed using algorithms.

## Project Goal

The initial aim of this project was to determine whether or not an algorithm could classify a company as belonging to the tech industry based solely on financial statements. This soon broadened in scope to include every major industry recognized by the SEC, with around ~ 350 classes by the end.

## Project Overview
![Project_Overview](https://raw.githubusercontent.com/BNDT4Sen/Final-Project-Financial-Analysis/master/Functions/Project_Overview.drawio.png)

## Data Collection

The Russel 3000 was chosen as a comprehensive list of companies to use as a basis for the data set. This list represents the 3000 largest companies in the United States. After locating the most recent official PDF file of the list (Data\Russel 3000.pdf), I used a Python module called Tabula to read Pandas DataFrames from it (API-Requests\Russel_3000_PDF_Reading.py). At that point I had a list of the names of 3000 companies and their respective ticker symbols. I then needed to find an API that I could query to collect financial statements.

Polygon.io was the API chosen for this purpose, as it uniquely provided historical financial statements. For some companies this data stretched back nearly 15 years. After poring over the API documentation and familiarizing myself with the endpoints, I wrote a python file to iterate over the Russel 3000 DataFrame and return the requested data (API-Requests\API_Requests.py).

A Json file was collected for each company (Data\Raw Request Data), although they were not equal in length. Although I had requested filings from the years 2008 to 2022, the API provided many of the individual company requests with just a few sets of financial statements each. This would make it impossible to organize the data by year in any meaningful way.

These Json files were then parsed and spliced into 6 Pandas Dataframes (API-Requests\Raw_to_Pandas.py). One for each type of financial statement provided, as well as a DataFrame for company information and another for filing information. The name of the industry that each individual company belongs to was discovered after collecting the Standard Industrial Classification list from the SEC (Data\Standard_Industrial_Classifications.csv). The next step of the process was to begin exploring and cleaning the DataFrames.

## Exploration and Cleaning

The Pandas DataFrames were initially explored in several Jupyter Notebooks, but this process was later condensed into the one remaining in the repository currently. (Exploratory-Data-Analysis\DataFrame_Exploration.ipynb). Both the exploration and cleaning processes were closely tied, and once I had a general feel for the data, I got my hands dirty.

Duplicate entries were checked and removed from the DataFrames (Exploratory-Data-Analysis\DataFrame_Cleaning.ipynb). Null values in Financial statements can often be interpreted as 0, and this remained the case across the vast majority of the columns. Certain columns with very few null values, particularly for items which would generally only be null in case of error, did have their values trimmed.

Once all of the duplicate and null values had been properly dealt with, the cleaned data was exported to be used in Feature Engineering (Data\Cleaned_Pandas_DataFrames).

## Feature Engineering

There were nearly 100 columns across all of the financial statement DataFrames, and this would be untenable for a large scale analysis. I decided to utilize feature engineering to reduce dimensionality. Focusing on highly important yet simple Financial Ratios, collected the necessary columns from the cleaned DataFrames and outputted a dataset that machine learning models would be trained and tested on (Functions\Feature_Engineering.ipynb).

#### The following features were created:

- Current Ratio; provides an important glimpse into how financially secure a company is in the short term, relating current assets to current liabilities.
- Operating Cash Flow Ratio; similar to the current ratio, but focuses moreso on cash and cash equivalents of the period rather than any and all current assets.
- Debt to Equity Ratio; Provides insight into how leveraged a company is. Obtained by dividing total liabilities by total equity, a higher Debt to Equity ratio can be seen as riskier, whilst lower is typically more conservative.
- Interest Coverage Ratio; Another take on the leverage of a company, this covers solely the interest payments that a company makes. This ratio would favour a company signing a single larger loan with lower rates over smaller, shorter term loans. Economic periods with the very low interest rates that we have seen in the past will make this metric particularly interesting going forward as rates continue to rise.
- Operating Margin Ratio; Identifies the proportion of revenue that is retained by the company after costs of revenue are taken into account. A higher ratio is seen as very favourable across any industry.
- Return on Assets; Identifies how well a company utilizes its assets to generate a profit. Found by dividing net income by total assets of the company.
- Return on Equity; Similar to Return on Assets, but takes the liabilities of a company into account as well. This punishes heavily leveraged companies in a way the previous ratio did not.
- Making Interest Payments; Not a financial ratio by any means, this metric is a binary yes or no regarding whether or not a company has recorded making interest payments in the period.

## Pipeline Construction 

Considering how wildly the values of the data could vary from company to company, scaling of some sort was a necessity. I tried out a few separate scalers, landing on Quantile Transformer. This scaler was especially effective at punishing outliers and bringing the fringes of the data closer to the center. Without this, top companies with tens or hundreds of billions in revenue would easily outweigh the smaller, but much more numerous companies of the Russel 3000.

Although the 8 features I had engineered would not bring about a problem strictly regarding dimensionality, their effectiveness was still up in the air. Principal Component Analysis would allow me to easily identify which features had a strong relationship with the data and which did not (Predictive-Models\Principal_Component_Analysis.ipynb).

#### Principal Component Analysis Results

- Current Ratio: 42.5%
- Operating Cash Flow: 19.1%
- Debt to Equity: 13.4%
- Interest Coverage: 10%
- Operating Margin: 7.9%
- Return on Assets: 4.1%
- Return on Equity: 1.8%
- Makes Interest Payments: 1.2%

Now that I had the features I needed to determine which model to use. I first tried SVM classification, whose results did not impress. Even classifying on a limited scope of just 10, accuracy and f1 scores were very poor regardless of parameters. Naive Bayes performed in a similar manner, although I maintained that file for the sake of comparison (Predictive-Models\Naive_Bayes.ipynb). There were some other classification models tested as well, but none came close to Random Forest.

Random Forest scored at least twice as highly as any other algorithm in classifying companies based on the limited testing scope of 10 classes. It was immediately clear that this was going to be the best choice for the machine learning pipeline.

Constructing the pipeline itself took very little time in comparison to the collection, cleaning, and parsing of the data. Already having tested several models, scalers, and dimensionality reduction techniques, I had an idea of what the end result would look like. Still, there were parameters that needed tuning. Grid Search Cross-Validation was used for this purpose. My initial Grid Search was far too ambitious, using several tens of gigabytes of memory, far more than I had available. I narrowed down to just a few important parameters and split the Grid Search into three rounds. The end result was a noticeable improvement over the vanilla Random Forest, although the scores remained a bit unimpressive (Predictive-Models\Model_Pipeline.ipynb).

## Results & Conclusion

The primary metric chosen for testing was the F1 score, a harmonic mean of both precision and recall. Considering the extremely unbalanced distribution of classes, using this metric over a typical accuracy score was necessary. The F1 score falls on a scale of 0 to 1, with 1 being a perfect score. Obviously, the below scores are nowhere near perfect.

#### Dummy Classifier:
- Precision Score: 0.0163 
- Recall Score: 0.0164 
- F1 Score: 0.0163

#### Vanilla Random Forest:
- Precision Score: 0.2160
- Recall Score: 0.2146 
- F1 Score: 0.2058

#### Pipeline Output:
- Precision Score: 0.2439 
- Recall Score: 0.2445 
- F1 Score: 0.2362

Despite being initially disappointed by the poor scores, when taking into account the number of classes (345) that the Random Forest had to work with, I felt satisfied. There is no doubt plenty of improvement to be made, but as a first iteration it does a fair job. The marked 15% improvement that the Pipeline had on the F1 Score was also nice to see. 

Considering the success of the Random Forest, I am eager to give neural networks a try. I suspect they will perform even better at classifying the large number of industries. That being said, a larger improvement would likely be had with further data cleaning and additional engineered features.

