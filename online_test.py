from copy import deepcopy

from selenium.webdriver import Keys, ActionChains


def print_map(smap):
    for i in range(len(smap)):
        if i % 5 == 0 and i != 0:
            print()
        print(end=" ")
        for j in range(len(smap[i])):
            if j % 5 == 0 and j != 0:
                print(end=" ")
            if smap[i][j] == 1:
                print(end="■")
            elif smap[i][j] == 0:
                print(end="×")
            else:
                print(end="□")
        print()


def print_lim_map(smap):
    for i in range(len(smap)):
        print(smap[i])


from seleniumwire import webdriver  # 替代原始的 webdriver
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.36'
}
# 连接已打开的 Edge 浏览器

options = webdriver.EdgeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.36")
options.debugger_address = "127.0.0.1:9222"  # 连接到之前启动的 Edge 端口

# 创建 WebDriver（不会打开新窗口，而是接管已打开的 Edge）
driver = webdriver.Edge(options=options)

# 获取当前页面的 HTML
html = driver.page_source
print(html)

task_top_div = driver.find_element("id","taskTop")
col = [list(map(int,_.text.split("\n"))) for _ in task_top_div.find_elements("class name","task-group")]

task_left_div = driver.find_element("id","taskLeft")
row = [list(map(int,_.text.split("\n"))) for _ in task_left_div.find_elements("class name","task-group")]

map_div = driver.find_element("class name","nonograms-cell-back")
row_divs = map_div.find_elements("class name","row")
cell_divs = [_.find_elements("class name","cell") for _ in row_divs]

print(col)
print(row)

n = len(col)


amap = []
p_row_map = []
p_col_map = []
temp_p_map = []
temp = []
for i in range(n):
    temp.append(-1)
for i in range(n):
    amap.append(deepcopy(temp))

temp = [].copy()
for i in range(n):
    temp.append(deepcopy([]))
for i in range(n):
    p_row_map.append(deepcopy(temp))
    p_col_map.append(deepcopy(temp))
    temp_p_map.append(deepcopy(temp))


def cal_pmap(num_list, is_row):
    global p_row_map,p_col_map
    for index_numList in range(n):
        nums = num_list[index_numList]
        cum_num_list = [0]
        for i in range(len(nums)):
            cum_num_list.append(cum_num_list[i] + nums[i] + 1)
        for num_index in range(len(nums)):
            left = cum_num_list[num_index] - cum_num_list[0]
            right = cum_num_list[-1] - cum_num_list[num_index + 1]
            for _ in range(left, n - right):
                if is_row:
                    p_row_map[index_numList][_].append(num_index)
                else:
                    p_col_map[_][index_numList].append(num_index)


def cal_fill(num_list, is_row):
    global amap
    for numList_index in range(len(num_list)):
        nums = num_list[numList_index]
        for num_index in range(len(nums)):
            num = nums[num_index]
            left = -1
            right = -1
            flag = False
            for i in range(n):
                if is_row:
                    if num_index in p_row_map[numList_index][i]:
                        if not flag:
                            flag = True
                            right = i
                        left = i
                else:
                    if num_index in p_col_map[i][numList_index]:
                        if not flag:
                            flag = True
                            right = i
                        left = i
            right = right + num
            left = left - num + 1
            for i in range(left, right):
                if is_row:
                    amap[numList_index][i] = 1
                else:
                    amap[i][numList_index] = 1


def merge_map(num_list, is_row):
    global p_row_map,p_col_map,amap
    for numList_index in range(len(num_list)):
        nums = num_list[numList_index]
        for num_index in range(len(nums)):
            num = nums[num_index]
            flag = False
            left = -1
            right = -1
            for i in range(n):
                if is_row:
                    pval = p_row_map[numList_index][i]
                    aval = amap[numList_index][i]
                else:
                    pval = p_col_map[i][numList_index]
                    aval = amap[i][numList_index]
                if aval == 1 and len(pval) == 1 and num_index in pval:
                    if not flag:
                        flag = True
                        left = i
                    right = i
            if flag:
                for i in range(left+1, right):
                    if is_row:
                        amap[numList_index][i] = 1
                    else:
                        amap[i][numList_index] = 1
                pad = num - right + left - 1
                for i in range(n):
                    if pad == 0 and (i == left-1 or i == right+1):
                        if is_row:
                            p_row_map[numList_index][i].clear()
                        else:
                            p_col_map[i][numList_index].clear()
                    if i not in range(left-pad, right+pad+1):
                        if is_row:
                            if num_index in p_row_map[numList_index][i]:
                                p_row_map[numList_index][i].remove(num_index)
                        else:
                            if num_index in p_col_map[i][numList_index]:
                                p_col_map[i][numList_index].remove(num_index)


def find_row_col_x():
    global p_row_map,p_col_map,amap
    for i in range(n):
        for j in range(n):
            if len(p_row_map[i][j]) == 0:
                amap[i][j] = 0
                p_col_map[i][j].clear()
            if len(p_col_map[i][j]) == 0:
                amap[i][j] = 0
                p_row_map[i][j].clear()


def find_x(num_list, is_row):
    global p_row_map,p_col_map,amap
    for numList_index in range(len(num_list)):
        nums = num_list[numList_index]
        for num_index in range(len(nums)):
            num = nums[num_index]
            left = -1
            right = -1
            flag = False

            if is_row:
                for i in range(n):
                    if num_index in p_row_map[numList_index][i]:
                        if not flag:
                            flag = True
                            left = i
                        right = i
                    else:
                        if right+1-left<num and flag:
                            for j in range(left, right+1):
                                if num_index in p_row_map[numList_index][j]:
                                    p_row_map[numList_index][j].remove(num_index)
                        flag = False
                        left = -1
                        right = -1
                if flag:
                    if right + 1 - left < num and flag:
                        for j in range(left, right + 1):
                            if num_index in p_row_map[numList_index][j]:
                                p_row_map[numList_index][j].remove(num_index)

            else:
                for i in range(n):
                    if num_index in p_col_map[i][numList_index]:
                        if not flag:
                            flag = True
                            left = i
                        right = i
                    else:
                        if right+1-left<num and flag:
                            for j in range(left, right+1):
                                if num_index in p_col_map[j][numList_index]:
                                    p_col_map[j][numList_index].remove(num_index)
                        flag = False
                        left = -1
                        right = -1
                if flag:
                    if right + 1 - left < num and flag:
                        for j in range(left, right + 1):
                            if num_index in p_col_map[j][numList_index]:
                                p_col_map[j][numList_index].remove(num_index)


def cnt_map():
    cnt = 0
    for i in range(n):
        for j in range(n):
            if amap[i][j] != -1:
                cnt+=1
    return cnt


def cal_lim(index,is_row):
    ans = []
    temp = 0
    if is_row:
        if amap[index][0] != 0:
            flag = 1
        else:
            flag = 0
        for i in range(n):
            if amap[index][i] != 0:
                if flag == 1:
                    temp += 1
                else:
                    flag = 1
                    ans.append(temp)
                    temp = 1
            else:
                if flag == 0:
                    temp -= 1
                else:
                    flag = 0
                    ans.append(temp)
                    temp = -1
    else:
        if amap[0][index] != 0:
            flag = 1
        else:
            flag = 0
        for i in range(n):
            if amap[i][index] != 0:
                if flag == 1:
                    temp += 1
                else:
                    flag = 1
                    ans.append(temp)
                    temp = 1
            else:
                if flag == 0:
                    temp -= 1
                else:
                    flag = 0
                    ans.append(temp)
                    temp = -1
    ans.append(temp)
    return ans


def new_cal_pmap(numList,is_row):
    tpmap = deepcopy(temp_p_map)
    for numList_index in range(len(numList)):
        nums = numList[numList_index]
        tag = cal_lim(numList_index, is_row)
        index_tag = 0
        index_point = 0
        left_num = []
        right_num = []
        for num_index in range(len(nums)):
            num = nums[num_index]
            flag = True
            while flag:
                if tag[index_tag] < 0:
                    index_point -= tag[index_tag]
                    index_tag += 1
                else:
                    if num <= tag[index_tag]:
                        left_num.append(index_point)
                        index_point += num
                        if num == tag[index_tag]:
                            index_tag += 1
                        else:
                            tag[index_tag] -= num + 1
                            index_point += 1
                        flag = False
                    else:
                        index_point += tag[index_tag]
                        index_tag += 1
        tag = cal_lim(numList_index, is_row)
        index_tag = len(tag) - 1
        index_point = n - 1
        for num_index in reversed(range(len(nums))):
            num = nums[num_index]
            flag = True
            while flag:
                if tag[index_tag] < 0:
                    index_point += tag[index_tag]
                    index_tag -= 1
                else:
                    if num <= tag[index_tag]:
                        right_num.append(index_point)
                        flag = False
                        index_point -= num
                        if num == tag[index_tag]:
                            index_tag -= 1
                        else:
                            tag[index_tag] -= num + 1
                            index_point -= 1
                    else:
                        index_point -= tag[index_tag]
                        index_tag -= 1
        right_num.reverse()
        for i in range(len(left_num)):
            left = left_num[i]
            right = right_num[i]
            for j in range(left, right + 1):
                if is_row:
                    tpmap[numList_index][j].append(i)
                else:
                    tpmap[j][numList_index].append(i)

    for i in range(n):
        for j in range(n):
            if is_row:
                for num in p_row_map[i][j]:
                    if num not in tpmap[i][j]:
                        p_row_map[i][j].remove(num)
            else:
                for num in p_col_map[i][j]:
                    if num not in tpmap[i][j]:
                        p_col_map[i][j].remove(num)




cal_pmap(row, True)
cal_pmap(col, False)
# epochs = 3
# for epoch in range(epochs):
#     cal_fill(row,True)
#     cal_fill(col,False)
#     merge_map(row,True)
#     merge_map(col,False)
#     find_row_col_x()
#     find_row_col_x()
#     find_x(row,True)
#     find_x(col,False)
#     # find_row_col_x()
#     # find_row_col_x()
all_cnt = n*n
cnt = cnt_map()
c = 0
old_cnt = -1
flag = True
while cnt < all_cnt:
    cal_fill(row,True)
    cal_fill(col,False)
    merge_map(row,True)
    merge_map(col,False)
    find_row_col_x()
    find_row_col_x()
    find_x(row,True)
    find_x(col,False)
    new_cal_pmap(row,True)
    new_cal_pmap(col,False)
    cnt = cnt_map()
    if cnt == old_cnt:
        flag=False
        break
    old_cnt = cnt
    c+=1
    print("第{}次迭代".format(c),end="")
    print("进度:{%.2f}%%"%(cnt*100/all_cnt))

print_map(amap)

for i in range(n):
    for j in range(n):
        if amap[i][j] == 1:
            cell_divs[i][j].click()
        elif amap[i][j] == 0 and not flag:
            ActionChains(driver).context_click(cell_divs[i][j]).perform()

# driver.close()