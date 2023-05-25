import numpy as np


all_s_num = 76
all_h_num = 7
h_p = all_h_num/all_s_num

s_base = 30
h_base = 6
p = 0.056

epoch_cost = 20


def get_s_with_content(content, s_n_cnt_list):
    """
    成功获取s后的操作
    :param content:
    :param s_n_cnt_list:
    :return:
    """
    # 更新获得s的累积列表
    s_n_cnt_list = update_s(s_n_cnt_list)
    # 判断是否累积获得目标h
    if s_n_cnt_list[1][1] >= h_base:
        # 更新获得h的累积列表
        s_n_cnt_list = update_h(s_n_cnt_list)
        current_s = np.random.randint(0, all_h_num)
        content[current_s] += 1
    else:
        current_s = np.random.randint(0, all_s_num)
        content[current_s] += 1
        if current_s < all_h_num:
            # 更新获得h的累积列表
            s_n_cnt_list = update_h(s_n_cnt_list)
    return content, s_n_cnt_list


def update_s(s_n_cnt_list):
    """
    获得s目标后的更新
    :param s_n_cnt_list:
    :return:
    """
    s_n_cnt_list[0][0] += 1
    s_n_cnt_list[1][1] += 1
    s_n_cnt_list[0][1] = 0
    return s_n_cnt_list


def update_h(s_n_cnt_list):
    """
    获得h目标后的更新
    :param s_n_cnt_list:
    :return:
    """
    s_n_cnt_list[1][0] += 1
    s_n_cnt_list[1][1] = 0
    return s_n_cnt_list


def update_common(s_n_cnt_list):
    """
    未获得目标s的普通更新
    :param s_n_cnt_list:
    :return:
    """
    s_n_cnt_list[0][1] += 1
    return s_n_cnt_list


def take_content(content, s_n_cnt_list, vis=False):
    # 初始化目标s和目标h的累积列表
    # s_n_cnt_list = [
    #     [0, 0],
    #     [0, 0],
    # ]
    # 初始化content
    # content = np.zeros(all_s_num)

    # 初始化目标content
    target_content = np.ones(all_s_num) * 5
    untarget_mark = True  # 未达成目标标志
    take_num = 0  # 循环次数
    while untarget_mark:
        take_num += 1
        current_p_s = np.random.rand()
        # 概率获得目标s
        if current_p_s <= p:
            content, s_n_cnt_list = get_s_with_content(content, s_n_cnt_list)
        else:
            # 普通更新
            s_n_cnt_list = update_common(s_n_cnt_list)
            if s_n_cnt_list[0][1] >= s_base:
                content, s_n_cnt_list = get_s_with_content(content, s_n_cnt_list)

        if vis:
            print('*' * 30)
            print('epoch:', take_num + 1, 'cost:', (take_num + 1) * epoch_cost)
            print('s_cnt:', s_n_cnt_list[0][0] - s_n_cnt_list[1][0], 'h_cnt:', s_n_cnt_list[1][0])
            print('h:', content[:all_h_num])
            # print('*' * 30)
        if check_target(content, target_content):
            break
    return content, s_n_cnt_list, take_num


def check_target(content, target_content):
    """
    检测目标是否达成
    :param content:
    :param target_content:
    :return:
    """
    # sub = content - target_content
    sub = content[:all_h_num] - target_content[:all_h_num]
    return np.all(sub >= 0)
  
  
if __name__ == '__main__':
  for i in range(1000):
    cnt = []
    s_n_cnt_list = [
        [0, 0],
        [0, 0],
    ]
    content = np.zeros(all_s_num)
    content, s_n_cnt_list, take_num = take_content(content, s_n_cnt_list, vis=False)
    cnt.append(take_num)
    print('*' * 30)
    print('epoch:', take_num + 1, 'cost:', (take_num + 1) * epoch_cost)
    print('s_cnt:', s_n_cnt_list[0][0] - s_n_cnt_list[1][0], 'h_cnt:', s_n_cnt_list[1][0])
    print('h:', content[:all_h_num])
    print('base_s:', take_num//s_base - take_num//s_base//h_base, 'base_h:', take_num//s_base//h_base)
  print('*' * 30)
  print('mean:')
  print('epoch:', np.mean(cnt), 'cost:', np.mean(cnt) * 20)
