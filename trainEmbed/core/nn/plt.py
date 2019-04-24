
import time

def show(rs_list):
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(12, 5))
    plt.ion()  # 开启交互绘图
    ax = fig.add_subplot(122)
    ax.plot(rs_list, 'b-')

    plt.pause(0.01)  # 显示出来
    time.sleep(5)  # 继续跑业务逻辑

    # 刷新图像
    ax.clear()
    ax.plot(rs_list, 'r.')

    while True:
        plt.pause(0.5)
