# Shopee-Code-League-2021

Category: Student

Team: SAMCOINS

## Challenge Details

[Shopee Code League](https://careers.shopee.sg/codeleague/) is a 3-week coding challenge consisting of 3 coding competitions open to all students and professionals across the region.

Over **15,000 people** from across Asia, aged between nine and 51, formed teams of 2 to 4 to take part in this year's challenge.

## Competitions

### 1. Data Analytics: Multi-Channel Contacts

- Duration: 3 hours
- Student Category Position: 136th
- Overall Position: 342nd (Top 36%)

Given a JSON dataset of customer service contacts information, the challenge was to identify how to merge relevant tickets originating from the same customers through different channels. For instance, the same customer may contact Shopee using different phone numbers or email addresses.

#### Remarks

I did not manage to consider sufficient edge cases to achieve the maximum score. For instance, given three records A, B and C, record C may be linked to record A via phone number, but linked to record B via email address. In this case, all three records should belong to the same set. This can be extended to the case where A and B are not singular records, but disjoint sets.

### 2. Data Science: Address Elements Extraction

- Duration: 1 week
- Student Category Position: 25th
- Overall Position: 84th (Top 9%)

Kaggle Notebook: https://www.kaggle.com/thirsty4pee/scl-ner-for-address-elements-extraction-0-61365

This is a Natural Language Processing (NLP) challenge where the aim is to build a model that accurately extracts Point of Interest (POI) Names and Street Names from unformatted Indonesia addresses.

####  Remarks

While I am satisfied with the model's accuracy in extracting relevant information from raw addresses, there remains the issue of incomplete raw addresses. I've tried various methods of correcting such addresses in both pre and post-processing, but these experiments failed to obtain a higher score on the leaderboard.

### 3. Data Structures and Algorithms: Programming Contest

- Duration: 3 hours
- Student Category Position: 49th
- Overall Position: 129th

A series of competitive programming problems.

#### Remarks

This was definitely a challenge for me, especially due to the fact that partial marks were not awarded - all test cases must be passed to obtain any marks at all for each problem. While several problems can be solved recursively, such naive solutions did not secure any points due to the strict time and memory requirements.

I managed to solve Shopee Farm using dynamic programming (DP), but ran out of time implementing a DP solution for Shoffee. I certainly need more practice!
