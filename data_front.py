import numpy as np
import pandas as pd
from google.cloud import bigquery
from data_utils_front import download_df_from_bq

TEST_MDA_TEXT ="""
    TEST MDA
 Item 7. Management&#8217;s Discussion and Analysis of Financial Condition and Results of Operations

The following discussion should be read in conjunction with the consolidated financial statements and accompanying notes included in Part II, Item 8 of this Form 10-K. This Item generally discusses 2023 and 2022 items and year-to-year comparisons between 2023 and 2022. Discussions of 2021 items and year-to-year comparisons between 2022 and 2021 are not included, and can be found in &#8220;Management&#8217;s Discussion and Analysis of Financial Condition and Results of Operations&#8221; in Part II, Item 7 of the Company&#8217;s Annual Report on Form 10-K for the fiscal year ended September 24, 2022.

Fiscal Period

The Company&#8217;s fiscal year is the 52- or 53-week period that ends on the last Saturday of September. An additional week is included in the first fiscal quarter every five or six years to realign the Company&#8217;s fiscal quarters with calendar quarters, which occurred in the first quarter of 2023. The Company&#8217;s fiscal year 2023 spanned 53 weeks, whereas fiscal years 2022 and 2021 spanned 52 weeks each.

Fiscal Year Highlights

The Company&#8217;s total net sales were $383.3 billion and net income was $97.0 billion during 2023.

The Company&#8217;s total net sales decreased 3% or $11.0 billion during 2023 compared to 2022. The weakness in foreign currencies relative to the U.S. dollar accounted for more than the entire year-over-year decrease in total net sales, which consisted primarily of lower net sales of Mac and iPhone, partially offset by higher net sales of Services.

The Company announces new product, service and software offerings at various times during the year. Significant announcements during fiscal year 2023 included the following:

First Quarter 2023:

&#8226; iPad and iPad Pro;

&#8226; Next-generation Apple TV 4K; and

&#8226; MLS Season Pass, a Major League Soccer subscription streaming service.

Second Quarter 2023:

&#8226; MacBook Pro 14&#8221;, MacBook Pro 16&#8221; and Mac mini; and

&#8226; Second-generation HomePod.

Third Quarter 2023:

&#8226; MacBook Air 15&#8221;, Mac Studio and Mac Pro;

&#8226; Apple Vision Pro&#8482;, the Company&#8217;s first spatial computer featuring its new visionOS&#8482;, expected to be available in early calendar year 2024; and

&#8226; iOS 17, macOS Sonoma, iPadOS 17, tvOS 17 and watchOS 10, updates to the Company&#8217;s operating systems.

Fourth Quarter 2023:

&#8226; iPhone 15, iPhone 15 Plus, iPhone 15 Pro and iPhone 15 Pro Max; and

&#8226; Apple Watch Series 9 and Apple Watch Ultra 2.

In May 2023, the Company announced a new share repurchase program of up to $90 billion and raised its quarterly dividend from $0.23 to $0.24 per share beginning in May 2023. During 2023, the Company repurchased $76.6 billion of its common stock and paid dividends and dividend equivalents of $15.0 billion.

Macroeconomic Conditions

Macroeconomic conditions, including inflation, changes in interest rates, and currency fluctuations, have directly and indirectly impacted, and could in the future materially impact, the Company&#8217;s results of operations and financial condition.

Apple Inc. | 2023 Form 10-K | 20

Segment Operating Performance

The following table shows net sales by reportable segment for 2023, 2022 and 2021 (dollars in millions):

##TABLE_START 2023 Change 2022 Change 2021 Net sales by reportable segment: Americas $ 162,560 (4) % $ 169,658 11 % $ 153,306 Europe 94,294 (1) % 95,118 7 % 89,307 Greater China 72,559 (2) % 74,200 9 % 68,366 Japan 24,257 (7) % 25,977 (9) % 28,482 Rest of Asia Pacific 29,615 1 % 29,375 11 % 26,356 Total net sales $ 383,285 (3) % $ 394,328 8 % $ 365,817 ##TABLE_END

Americas

Americas net sales decreased 4% or $7.1 billion during 2023 compared to 2022 due to lower net sales of iPhone and Mac, partially offset by higher net sales of Services.

Europe

Europe net sales decreased 1% or $824 million during 2023 compared to 2022. The weakness in foreign currencies relative to the U.S. dollar accounted for more than the entire year-over-year decrease in Europe net sales, which consisted primarily of lower net sales of Mac and Wearables, Home and Accessories, partially offset by higher net sales of iPhone and Services.

Greater China

Greater China net sales decreased 2% or $1.6 billion during 2023 compared to 2022. The weakness in the renminbi relative to the U.S. dollar accounted for more than the entire year-over-year decrease in Greater China net sales, which consisted primarily of lower net sales of Mac and iPhone.

Japan

Japan net sales decreased 7% or $1.7 billion during 2023 compared to 2022. The weakness in the yen relative to the U.S. dollar accounted for more than the entire year-over-year decrease in Japan net sales, which consisted primarily of lower net sales of iPhone, Wearables, Home and Accessories and Mac.

Rest of Asia Pacific

Rest of Asia Pacific net sales increased 1% or $240 million during 2023 compared to 2022. The weakness in foreign currencies relative to the U.S. dollar had a significantly unfavorable year-over-year impact on Rest of Asia Pacific net sales. The net sales increase consisted of higher net sales of iPhone and Services, partially offset by lower net sales of Mac and iPad.

Apple Inc. | 2023 Form 10-K | 21

Products and Services Performance

The following table shows net sales by category for 2023, 2022 and 2021 (dollars in millions):

##TABLE_START 2023 Change 2022 Change 2021 Net sales by category: iPhone (1)

$ 200,583 (2) % $ 205,489 7 % $ 191,973 Mac (1)

29,357 (27) % 40,177 14 % 35,190 iPad (1)

28,300 (3) % 29,292 (8) % 31,862 Wearables, Home and Accessories (1)

39,845 (3) % 41,241 7 % 38,367 Services (2)

85,200 9 % 78,129 14 % 68,425 Total net sales $ 383,285 (3) % $ 394,328 8 % $ 365,817 ##TABLE_END

(1) Products net sales include amortization of the deferred value of unspecified software upgrade rights, which are bundled in the sales price of the respective product.

(2) Services net sales include amortization of the deferred value of services bundled in the sales price of certain products.

iPhone

iPhone net sales decreased 2% or $4.9 billion during 2023 compared to 2022 due to lower net sales of non-Pro iPhone models, partially offset by higher net sales of Pro iPhone models.

Mac

Mac net sales decreased 27% or $10.8 billion during 2023 compared to 2022 due primarily to lower net sales of laptops.

iPad

iPad net sales decreased 3% or $1.0 billion during 2023 compared to 2022 due primarily to lower net sales of iPad mini and iPad Air, partially offset by the combined net sales of iPad 9th and 10th generation.

Wearables, Home and Accessories

Wearables, Home and Accessories net sales decreased 3% or $1.4 billion during 2023 compared to 2022 due primarily to lower net sales of Wearables and Accessories.

Services

Services net sales increased 9% or $7.1 billion during 2023 compared to 2022 due to higher net sales across all lines of business.

Apple Inc. | 2023 Form 10-K | 22

Gross Margin

Products and Services gross margin and gross margin percentage for 2023, 2022 and 2021 were as follows (dollars in millions):

##TABLE_START 2023 2022 2021 Gross margin: Products $ 108,803 $ 114,728 $ 105,126 Services 60,345 56,054 47,710 Total gross margin $ 169,148 $ 170,782 $ 152,836 ##TABLE_END

##TABLE_START Gross margin percentage: Products 36.5 % 36.3 % 35.3 % Services 70.8 % 71.7 % 69.7 % Total gross margin percentage 44.1 % 43.3 % 41.8 % ##TABLE_END

Products Gross Margin

Products gross margin decreased during 2023 compared to 2022 due to the weakness in foreign currencies relative to the U.S. dollar and lower Products volume, partially offset by cost savings and a different Products mix.

Products gross margin percentage increased during 2023 compared to 2022 due to cost savings and a different Products mix, partially offset by the weakness in foreign currencies relative to the U.S. dollar and decreased leverage.

Services Gross Margin

Services gross margin increased during 2023 compared to 2022 due primarily to higher Services net sales, partially offset by the weakness in foreign currencies relative to the U.S. dollar and higher Services costs.

Services gross margin percentage decreased during 2023 compared to 2022 due to higher Services costs and the weakness in foreign currencies relative to the U.S. dollar, partially offset by a different Services mix.

The Company&#8217;s future gross margins can be impacted by a variety of factors, as discussed in Part I, Item 1A of this Form 10-K under the heading &#8220;Risk Factors.&#8221; As a result, the Company believes, in general, gross margins will be subject to volatility and downward pressure.

Operating Expenses

Operating expenses for 2023, 2022 and 2021 were as follows (dollars in millions):

##TABLE_START 2023 Change 2022 Change 2021 Research and development $ 29,915 14 % $ 26,251 20 % $ 21,914 Percentage of total net sales 8 % 7 % 6 % Selling, general and administrative $ 24,932 (1) % $ 25,094 14 % $ 21,973 Percentage of total net sales 7 % 6 % 6 % Total operating expenses $ 54,847 7 % $ 51,345 17 % $ 43,887 Percentage of total net sales 14 % 13 % 12 % ##TABLE_END

Research and Development

The year-over-year growth in R&#38;D expense in 2023 was driven primarily by increases in headcount-related expenses.

Selling, General and Administrative

Selling, general and administrative expense was relatively flat in 2023 compared to 2022.

Apple Inc. | 2023 Form 10-K | 23

Provision for Income Taxes

Provision for income taxes, effective tax rate and statutory federal income tax rate for 2023, 2022 and 2021 were as follows (dollars in millions):

##TABLE_START 2023 2022 2021 Provision for income taxes $ 16,741 $ 19,300 $ 14,527 Effective tax rate 14.7 % 16.2 % 13.3 % Statutory federal income tax rate 21 % 21 % 21 % ##TABLE_END

The Company&#8217;s effective tax rate for 2023 and 2022 was lower than the statutory federal income tax rate due primarily to a lower effective tax rate on foreign earnings, the impact of the U.S. federal R&#38;D credit, and tax benefits from share-based compensation, partially offset by state income taxes.

The Company&#8217;s effective tax rate for 2023 was lower compared to 2022 due primarily to a lower effective tax rate on foreign earnings and the impact of U.S. foreign tax credit regulations issued by the U.S. Department of the Treasury in 2022, partially offset by lower tax benefits from share-based compensation.

Liquidity and Capital Resources

The Company believes its balances of cash, cash equivalents and unrestricted marketable securities, which totaled $148.3 billion as of September 30, 2023, along with cash generated by ongoing operations and continued access to debt markets, will be sufficient to satisfy its cash requirements and capital return program over the next 12 months and beyond.

The Company&#8217;s material cash requirements include the following contractual obligations:

Debt

As of September 30, 2023, the Company had outstanding fixed-rate notes with varying maturities for an aggregate principal amount of $106.6 billion (collectively the &#8220;Notes&#8221;), with $9.9 billion payable within 12 months. Future interest payments associated with the Notes total $41.1 billion, with $2.9 billion payable within 12 months.

The Company also issues unsecured short-term promissory notes pursuant to a commercial paper program. As of September 30, 2023, the Company had $6.0 billion of commercial paper outstanding, all of which was payable within 12 months.

"""

def convert_quarter_format(q):
        # e.g., 'Q4-24' -> 2023_Q3
        quarter, year_suffix = q.split('-')
        year_prefix = '20' + year_suffix
        return f"{year_prefix}_{quarter}"

def ticker_sentiment(ticker):
    query_ticker = f"""
        SELECT quarter_year, ticker, sector, net_sentiment FROM `sentiment-lewagon.sentiment_db.net_sentiment`
        WHERE
            quarter_year != 'Q4-24'
                AND
            ticker = '{ticker.upper()}'
        """
    # print("running query:", query_ticker)
    ticker_df = download_df_from_bq("net_sentiment", custom_query=query_ticker)

    # Apply the function to the column
    ticker_df['quarter_year'] = ticker_df['quarter_year'].apply(convert_quarter_format)

    return ticker_df.sort_values(by='quarter_year', ascending=True)

def sector_sentiment(sector):
    query_sector = f"""
        SELECT quarter_year, sector, avg(net_sentiment) as net_sentiment
        FROM `sentiment-lewagon.sentiment_db.net_sentiment`
        WHERE quarter_year != 'Q4-24'
        AND sector = '{sector}'
        GROUP BY quarter_year, sector
        """
    sector_df = download_df_from_bq("net_sentiment", custom_query=query_sector)

    # Apply the function to the column
    sector_df['quarter_year'] = sector_df['quarter_year'].apply(convert_quarter_format)

    return sector_df.sort_values(by='quarter_year', ascending=True)
