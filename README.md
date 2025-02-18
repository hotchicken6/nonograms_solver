# 数织解密器

***

<div style="text-align: center;">
    <a href="#数织解密器">中文</a> |
    <a href="#Nonograms_Solver">English</a><br>
</div>

***
## 0. 功能(必须看)

- [X] 简单题目能解决
- 算法模型任有些特殊情况***未能***解决
- 每个难题(20×20)及其以上有可能解***不***出来
- ***不***支持长方形数织谜题
- ***代码未经优化***

## 1. 介绍

### 1.1 Local

通过手动输入行族和列族的信息和大小 **(仅支持正方形大小)**，解出数织的解。

### 1.2 Online

通过操控已打开的浏览器，打开一个数织游戏小网站[数织](https://cn.puzzle-nonograms.com)获取的行族和列族的信息和大小 **(
仅支持正方形大小)**
，解出数织的解，并填入。

#### tips：需要一定的爬虫知识

## 2. 算法介绍

## 2.1 步骤1：全概率

设有以下行

| 1 | 2 | 3 |   |   |   |   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

将1，2，3所在方块的可能性全部计算出来，则有

| 1 | 1 | 1 2 | 2 | 2 | 2 3 | 3 | 3 | 3 | 3 |
|---|---|-----|---|---|-----|---|---|---|---|

上图则为方块所在的全概率

## 2.2 步骤2：左右极

将2.1所计算的全概率图进行再次计算，根据方块的长度计算每个数字的右数最左边和左数最右边的块，得出该数字所必然填空的地方

设有如下全概率图

| 1 | 1 | 1 2 | 2 | 2 | 2 3 | 3 | 3 | 3 | 3 |
|---|---|-----|---|---|-----|---|---|---|---|

有(数字)(左极限)(右极限)  
1 3 1  
2 5 4  
3 8 8

如果右极小于等于左极限，则从右极限到左极限的坐标都是此数字的必然填空点，即有

| 1 | 2 | 3 |   |   |   |   |   |   |   | ■ |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

## 2.3 步骤3：聚合

设有如下全概率图(上)和答案图(下)

| 1 | 2 | 3 | 1 | 1 | 1 2 | 2 | 2 | 2 3 | 3 | 3 | 3 | 3 |
|---|---|---|---|---|-----|---|---|-----|---|---|---|---|
| 1 | 2 | 3 |   |   |     |   |   |     | ■ |   | ■ |   |

两个已经确定的方块和***唯一***的全概率坐标对应，则此时可以将这两个方块进行聚合连接，则有

| 1 | 2 | 3 | 1 | 1 | 1 2 | 2 | 2 | 2 3 | 3 | 3 | 3 | 3 |
|---|---|---|---|---|-----|---|---|-----|---|---|---|---|
| 1 | 2 | 3 |   |   |     |   |   |     | ■ | ■ | ■ |   |

## 2.4 步骤4：找X点

此时有找出的点位来，将其X进行标出，并且在全概率图进行删除

设有如下全概率图(上)和答案图(下)

| 1 | 2 | 3 | 1 | 1 | 1 2 | 2 | 2 | 2 3 | 3 | 3 | 3 | 3 |
|---|---|---|---|---|-----|---|---|-----|---|---|---|---|
| 1 | 2 | 3 |   |   |     | ■ | ■ |     |   | ■ | ■ |   |

则坐标2已经找出，删除除本身外所有的2，且3有2个，删除其达不到的全概率图，即有

| 1 | 2 | 3 | 1 | 1 | 1 | 2 | 2 |   | 3 | 3 | 3 | 3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 2 | 3 |   |   |   | ■ | ■ |   |   | ■ | ■ |   |

然后将全概率图为空的删除，和已经标X点的删除，有

| 1 | 2 | 3 | 1 | 1 |   | 2 | 2 |   | 3 | 3 | 3 | 3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 2 | 3 |   |   | X | ■ | ■ | X |   | ■ | ■ |   |

## 2.5 步骤N：重复步骤1-4，直到图解完

**篇幅有限，许多特殊情况未能讲解**

| 1 | 2 | 3 | 1 |   |   | 2 | 2 |   |   | 3 | 3 | 3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 2 | 3 | ■ | X | X | ■ | ■ | X | X | ■ | ■ | ■ |

# 3.例

以数织游戏小网站(https://cn.puzzle-nonograms.com),题号: 347917为例  
**篇幅有限，全概率图不写出来**

0

|   |   | 2 |   |   | 1 | 1 |
|---|---|---|---|---|---|---|
|   |   | 1 | 4 | 2 | 1 | 1 |
|   | 4 |   |   |   |   |   |
|   | 3 |   |   |   |   |   |
| 1 | 2 |   |   |   |   |   |
|   | 2 |   |   |   |   |   |
|   | 1 |   |   |   |   |   |

1 左右极

|   |   | 2 |   |   | 1 | 1 |
|---|---|---|---|---|---|---|
|   |   | 1 | 4 | 2 | 1 | 1 |
|   | 4 |   | ■ | ■ | ■ |   |
|   | 3 | ■ | ■ | ■ |   |   |
| 1 | 2 |   | ■ |   | ■ |   |
|   | 2 |   | ■ |   |   |   |
|   | 1 |   |   |   |   |   |

2 聚合

|   |   | 2 |   |   | 1 | 1 |
|---|---|---|---|---|---|---|
|   |   | 1 | 4 | 2 | 1 | 1 |
|   | 4 |   | ■ | ■ | ■ |   |
|   | 3 | ■ | ■ | ■ |   |   |
| 1 | 2 |   | ■ |   | ■ |   |
|   | 2 |   | ■ |   |   |   |
|   | 1 |   |   |   |   |   |

3 找X

|   |   | 2 |   |   | 1 | 1 |
|---|---|---|---|---|---|---|
|   |   | 1 | 4 | 2 | 1 | 1 |
|   | 4 |   | ■ | ■ | ■ |   |
|   | 3 | ■ | ■ | ■ | X | X |
| 1 | 2 | X | ■ | X | ■ |   |
|   | 2 |   | ■ | X | X | X |
|   | 1 |   | X | X | X |   |

4 再一次左右极

|   |   | 2 |   |   | 1 | 1 |
|---|---|---|---|---|---|---|
|   |   | 1 | 4 | 2 | 1 | 1 |
|   | 4 | ■ | ■ | ■ | ■ |   |
|   | 3 | ■ | ■ | ■ | X | X |
| 1 | 2 | X | ■ | X | ■ | ■ |
|   | 2 | ■ | ■ | X | X | X |
|   | 1 |   | X | X | X |   |

5 聚合

|   |   | 2 |   |   | 1 | 1 |
|---|---|---|---|---|---|---|
|   |   | 1 | 4 | 2 | 1 | 1 |
|   | 4 | ■ | ■ | ■ | ■ |   |
|   | 3 | ■ | ■ | ■ | X | X |
| 1 | 2 | X | ■ | X | ■ | ■ |
|   | 2 | ■ | ■ | X | X | X |
|   | 1 |   | X | X | X |   |

6 找X

|   |   | 2 |   |   | 1 | 1 |
|---|---|---|---|---|---|---|
|   |   | 1 | 4 | 2 | 1 | 1 |
|   | 4 | ■ | ■ | ■ | ■ | X |
|   | 3 | ■ | ■ | ■ | X | X |
| 1 | 2 | X | ■ | X | ■ | ■ |
|   | 2 | ■ | ■ | X | X | X |
|   | 1 | X | X | X | X |   |

7 再一次左右极

|   |   | 2 |   |   | 1 | 1 |
|---|---|---|---|---|---|---|
|   |   | 1 | 4 | 2 | 1 | 1 |
|   | 4 | ■ | ■ | ■ | ■ | X |
|   | 3 | ■ | ■ | ■ | X | X |
| 1 | 2 | X | ■ | X | ■ | ■ |
|   | 2 | ■ | ■ | X | X | X |
|   | 1 | X | X | X | X | ■ |

完成

# Nonograms_Solver

***

<div style="text-align: center;">
    <a href="#数织解密器">中文</a> |
    <a href="#Nonograms_Solver">English</a><br>
</div>

***
## 0. Features (Must Read)

- [X] Simple problems can be solved
- Some special cases in the algorithm model ***cannot*** be solved
- For each difficult problem (20×20) or larger, a solution ***might not*** be found
- ***Does not*** support rectangular nonogram puzzles
- ***Code is unoptimized***

## 1. Introduction

### 1.1 Local

Manually input the row family and column family information and size **(only supports square size)**, and solve the
solution of the nonogram.

### 1.2 Online

By controlling an opening browser, open a nonogram game website (https://www.puzzle-nonograms.com), retrieve the row and
column family information and size **(only supports square size)**, solve the nonogram puzzle, and fill in the solution.

#### tips:Requires some knowledge of web scraping

## 2. Algorithm Introduction

## 2.1 Step 1: Total Probability

Let there be the following rows

| 1 | 2 | 3 |   |   |   |   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

By calculating all the possibilities of the blocks where 1, 2, and 3 are located, we can get

| 1 | 1 | 1 2 | 2 | 2 | 2 3 | 3 | 3 | 3 | 3 |
|---|---|-----|---|---|-----|---|---|---|---|

The above diagram shows the total probability of the blocks' locations.

## 2.2 Step 2: Left and Right Extremes

Recalculate the total probability chart obtained in Step 2.1, and calculate the leftmost and rightmost blocks for each
number based on the block length, and get the points that must be filled for that number.

Let the following be the total probability chart:

| 1 | 1 | 1 2 | 2 | 2 | 2 3 | 3 | 3 | 3 | 3 |
|---|---|-----|---|---|-----|---|---|---|---|

There are (number) (left limit) (right limit)  
1 3 1  
2 5 4  
3 8 8

If the right limit is less than or equal to the left limit, the coordinates from the right limit to the left limit are
the inevitable filling points for this number.

## 2.3 Step 3: Aggregation

Let there be the following total probability chart (top) and answer chart (bottom):

| 1 | 2 | 3 | 1 | 1 | 1 2 | 2 | 2 | 2 3 | 3 | 3 | 3 | 3 |
|---|---|---|---|---|-----|---|---|-----|---|---|---|---|
| 1 | 2 | 3 |   |   |     |   |   |     | ■ |   | ■ |   |

If two blocks are already determined and correspond to **unique** total probability coordinates, then these two blocks
can be aggregated and connected, as shown below:

| 1 | 2 | 3 | 1 | 1 | 1 2 | 2 | 2 | 2 3 | 3 | 3 | 3 | 3 |
|---|---|---|---|---|-----|---|---|-----|---|---|---|---|
| 1 | 2 | 3 |   |   |     |   |   |     | ■ | ■ | ■ |   |

## 2.4 Step 4: Find X Points

At this point, mark the X points found and delete them from the total probability chart.

Let the following be the total probability chart (top) and answer chart (bottom):

| 1 | 2 | 3 | 1 | 1 | 1 2 | 2 | 2 | 2 3 | 3 | 3 | 3 | 3 |
|---|---|---|---|---|-----|---|---|-----|---|---|---|---|
| 1 | 2 | 3 |   |   |     | ■ | ■ |     |   | ■ | ■ |   |

Then, coordinate 2 has been found, so delete all other 2s, and since there are two 3s, delete those that cannot reach
the total probability chart, as shown below:

| 1 | 2 | 3 | 1 | 1 | 1 | 2 | 2 |   | 3 | 3 | 3 | 3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 2 | 3 |   |   |   | ■ | ■ |   |   | ■ | ■ |   |

Then delete the empty total probability chart and those with marked X points, resulting in:

| 1 | 2 | 3 | 1 | 1 |   | 2 | 2 |   | 3 | 3 | 3 | 3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 2 | 3 |   |   | X | ■ | ■ | X |   | ■ | ■ |   |

## 2.5 Step N: Repeat Steps 1-4 until the chart is solved

**Due to space limitations, many special cases are not explained.**

| 1 | 2 | 3 | 1 |   |   | 2 | 2 |   |   | 3 | 3 | 3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 2 | 3 | ■ | X | X | ■ | ■ | X | X | ■ | ■ | ■ |

# 3. Example

Using the nonogram game website (https://www.puzzle-nonograms.com), question number: 347917 as an example.  
**Due to space limitations, the total probability chart is not shown.**

0

|   |   | 2 |   |   | 1 | 1 |
|---|---|---|---|---|---|---|
|   |   | 1 | 4 | 2 | 1 | 1 |
|   | 4 |   |   |   |   |   |
|   | 3 |   |   |   |   |   |
| 1 | 2 |   |   |   |   |   |
|   | 2 |   |   |   |   |   |
|   | 1 |   |   |   |   |   |

1 Left and Right Extremes

|   |   | 2 |   |   | 1 | 1 |
|---|---|---|---|---|---|---|
|   |   | 1 | 4 | 2 | 1 | 1 |
|   | 4 |   | ■ | ■ | ■ |   |
|   | 3 | ■ | ■ | ■ |   |   |
| 1 | 2 |   | ■ |   | ■ |   |
|   | 2 |   | ■ |   |   |   |
|   | 1 |   |   |   |   |   |

2 Aggregation

|   |   | 2 |   |   | 1 | 1 |
|---|---|---|---|---|---|---|
|   |   | 1 | 4 | 2 | 1 | 1 |
|   | 4 |   | ■ | ■ | ■ |   |
|   | 3 | ■ | ■ | ■ |   |   |
| 1 | 2 |   | ■ |   | ■ |   |
|   | 2 |   | ■ |   |   |   |
|   | 1 |   |   |   |   |   |

3 Find X

|   |   | 2 |   |   | 1 | 1 |
|---|---|---|---|---|---|---|
|   |   | 1 | 4 | 2 | 1 | 1 |
|   | 4 |   | ■ | ■ | ■ |   |
|   | 3 | ■ | ■ | ■ | X | X |
| 1 | 2 | X | ■ | X | ■ |   |
|   | 2 |   | ■ | X | X | X |
|   | 1 |   | X | X | X |   |

4 Left and Right Extremes Again

|   |   | 2 |   |   | 1 | 1 |
|---|---|---|---|---|---|---|
|   |   | 1 | 4 | 2 | 1 | 1 |
|   | 4 | ■ | ■ | ■ | ■ |   |
|   | 3 | ■ | ■ | ■ | X | X |
| 1 | 2 | X | ■ | X | ■ | ■ |
|   | 2 | ■ | ■ | X | X | X |
|   | 1 |   | X | X | X |   |

5 Aggregation

|   |   | 2 |   |   | 1 | 1 |
|---|---|---|---|---|---|---|
|   |   | 1 | 4 | 2 | 1 | 1 |
|   | 4 | ■ | ■ | ■ | ■ |   |
|   | 3 | ■ | ■ | ■ | X | X |
| 1 | 2 | X | ■ | X | ■ | ■ |
|   | 2 | ■ | ■ | X | X | X |
|   | 1 |   | X | X | X |   |

6 Find X

|   |   | 2 |   |   | 1 | 1 |
|---|---|---|---|---|---|---|
|   |   | 1 | 4 | 2 | 1 | 1 |
|   | 4 | ■ | ■ | ■ | ■ | X |
|   | 3 | ■ | ■ | ■ | X | X |
| 1 | 2 | X | ■ | X | ■ | ■ |
|   | 2 | ■ | ■ | X | X | X |
|   | 1 | X | X | X | X |   |

7 Left and Right Extremes Again

|   |   | 2 |   |   | 1 | 1 |
|---|---|---|---|---|---|---|
|   |   | 1 | 4 | 2 | 1 | 1 |
|   | 4 | ■ | ■ | ■ | ■ | X |
|   | 3 | ■ | ■ | ■ | X | X |
| 1 | 2 | X | ■ | X | ■ | ■ |
|   | 2 | ■ | ■ | X | X | X |
|   | 1 | X | X | X | X | ■ |

Finish