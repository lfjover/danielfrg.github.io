---
layout: post
title: Creating a blog in 2012
---
[Permalink](http://ctrl68.wordpress.com/2013/01/18/copper-bi-tools-for-python-preprocessing/ "Permalink to BI tools for Python – Preprocessing « CTRL 68")

# BI tools for Python – Preprocessing « CTRL 68

This is a follow up of my [previous post][1] where I talk about replacing the very basics of SAS (Enterprise Miner) with Python (using pandas %2B scikit-learn). The example on that post was way to easy. I just start my Advance Business Intelligence class and we are going to use SAS again, I am going to take this opportunity and develop some tools to do the **same** of my BI class with python.

Dataset: I am going to use the same dataset as in my class; is about donations, is not huge but is not small (28 columns and 9686 row) - [csv file][2].

After hours of thinking I decide to call this module [copper][3] (inspired by dog of [The Fox and the Hound][4] aka the saddest movie ever) the code is available on [github][3].

The first class of the semester was to remember how to explore and pre-process the data. SAS does a very good job understanding the data, for example: has no problem with the money columns (starts with the dollar symbol: ‘$’) or categorical/string columns. Scikit-learn has problems with this type of variables; only can use numbers.

To solve this problem I develop a simple class called Dataset which is just a wrapper around a few pandas DataFrames to add metadata: role and type of each column. And transforms the data depending of the metadata.

For now the Roles can be:

*   ID: Identifier of the row, no use in machine learning
*   Input: Input to the machine learning models
*   Target: Target to the machine learning models
*   Rejected: Do not use this for the machine learning

Types can be:

*   Numeric: usually int or float; so does not apply any transformation
*   Money: Remove the dollar symbols (‘$’) and convert to number
*   Category: usually strings; transform the categories into different columns for scikit-learn

When the metadata is correct can select different parts (based on the role) of the dataset and export them if needed

*   inputs, target: Useful transformations for scikit-learn – more about this in other posts
*   frame: Complete frame: Useful transformations for exploring the data

## Example

Importing the data


    copper.config.data_dir = './'
    ds = copper.load('donors.csv')
    print(ds)


Output:

    Role      Type
    TARGET_B            Target    Number
    ID                      ID    Number
    TARGET_D          Rejected     Money
    GiftCnt36            Input    Number
    GiftCntAll           Input    Number
    GiftCntCard36        Input    Number
    GiftCntCardAll       Input    Number
    GiftAvgLast          Input     Money
    GiftAvg36            Input     Money
    GiftAvgAll           Input     Money
    GiftAvgCard36        Input     Money
    GiftTimeLast         Input    Number
    GiftTimeFirst        Input    Number
    PromCnt12            Input    Number
    PromCnt36            Input    Number
    PromCntAll           Input    Number
    PromCntCard12        Input    Number
    PromCntCard36        Input    Number
    PromCntCardAll       Input    Number
    StatusCat96NK        Input  Category
    StatusCatStarAll     Input    Number
    DemCluster           Input    Number
    DemAge               Input    Number
    DemGender            Input  Category
    DemHomeOwner         Input  Category
    DemMedHomeValue      Input     Money
    DemPctVeterans       Input    Number
    DemMedIncome         Input     Money

As you can see the class automatically detects which columns are Numerical/Money/Category and sets the type. Also detects (based on the name of the column) the roles ID/Input/Target; for example the second target is rejected because only one is set to be the target.

Note that the role and type can be changed, for example:


    ds.role['DemMedIncome'] = 'Rejected'
    print(ds)


Produces:

    ...
    DemPctVeterans       Input    Number
    DemMedIncome      Rejected     Money

We can export parts of it:


    ds.export(name='frame', format='csv', w='frame')
    ds.export(name='inputs', format='csv', w='inputs')
    ds.export(name='target', format='csv', w='target')


or just see them in the terminal/ipython notebook:


    print(ds.frame)
    print(ds.inputs)
    print(ds.targets)


## Comparing

This is a comparison of the some columns marked as ‘Money’.


    original = ds._oframe[['GiftAvgLast', 'GiftAvg36', 'GiftAvgAll', 'GiftAvgCard36']][0:10]
    new = ds.frame[['GiftAvgLast', 'GiftAvg36', 'GiftAvgAll', 'GiftAvgCard36']][0:10]
    print(original)
    print(new)


Before:

    GiftAvgLast GiftAvg36 GiftAvgAll GiftAvgCard36
    0      $17.00    $13.50      $9.25        $17.00
    1      $20.00    $20.00     $15.88           NaN
    2       $6.00     $5.17      $3.73         $5.00
    3      $10.00     $8.67      $8.50         $8.67
    4      $20.00    $20.00     $20.00        $20.00
    5      $11.00    $10.33      $8.27         $8.00
    6      $15.00    $20.00     $13.00        $20.00
    7      $15.00    $15.00     $11.50           NaN
    8      $35.00    $35.00     $28.33           NaN
    9       $6.00    $20.00     $11.60        $20.00

After:

    GiftAvgLast  GiftAvg36  GiftAvgAll  GiftAvgCard36
    0           17      13.50        9.25          17.00
    1           20      20.00       15.88            NaN
    2            6       5.17        3.73           5.00
    3           10       8.67        8.50           8.67
    4           20      20.00       20.00          20.00
    5           11      10.33        8.27           8.00
    6           15      20.00       13.00          20.00
    7           15      15.00       11.50            NaN
    8           35      35.00       28.33            NaN
    9            6      20.00       11.60          20.00

This is a comparison of the columns marked as ‘Category’:


    original = ds._oframe[['DemGender']][0:10]
    new = ds.inputs[['DemGender [F]', 'DemGender [M]', 'DemGender [U]']][0:10]
    print(original)
    print(new)


Before:

    DemGender
    0         F
    1         F
    2         M
    3         M
    4         M
    5         M
    6         M
    7         U
    8         F
    9         U

After:

    DemGender [F]  DemGender [M]  DemGender [U]
    0              1              0              0
    1              1              0              0
    2              0              1              0
    3              0              1              0
    4              0              1              0
    5              0              1              0
    6              0              1              0
    7              0              0              1
    8              1              0              0
    9              0              0              1

On this case we need to use `ds.inputs` instead of `ds.frame` because for the second one the categorical variables are not transformed, for the inputs are transformed because scikit-learn requires it.

## Thats it!

for now ![:)][5]

TODO:

*   Make graphics exploration easier – histograms mainly
*   Make a wrapper around scikit-learn to easily select models

Code is on [github][6] – I hope to update significantly the package every week with the updates from each class.

### Like this:

Be the first to like this.

 [1]: http://ctrl68.wordpress.com/2013/01/02/will-it-python-replace-sas-enterprise-miner-basic/ "Will it Python? Replace SAS Enterprise Miner (basic)"
 [2]: https://raw.github.com/dfrodriguez143/copper/master/examples/donors/donors.csv "Donors Dataset"
 [3]: https://github.com/dfrodriguez143/copper "Python Copper"
 [4]: http://en.wikipedia.org/wiki/The_Fox_and_the_Hound
 [5]: http://s0.wp.com/wp-includes/images/smilies/icon_smile.gif?m=1129645325g
 [6]: https://github.com/dfrodriguez143/copper "Copper Github"
