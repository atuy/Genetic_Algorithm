from tkinter import *
from Genetic_Function import *
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import tkinter.messagebox
from matplotlib import pyplot as plt
from matplotlib import animation
import tkinter as tk


class RegrMagic(object):
    input_pw=""
    min_len = 2
    max_len = 30
    x_lab = []  # x축 값
    y_lab = []  # y축 값

    # 메인 부분 위는 다 함수 정의
    n_generation = 100000
    population = 100
    best_sample = 20
    lucky_few = 20
    n_child = 5
    chance_of_mutation = 10
    endNum=100

    """Mock for function Regr_magic()
    """
    pop = generate_population(size=population, min_len=min_len, max_len=max_len)

    def __init__(self,input_pw,menu):
        self.input_pw=input_pw
        self.g=0
        self.menu=menu


    def __call__(self):

        while(self.g<=self.n_generation):
            pop_sorted, pred_len = compute_performace(population=self.pop, password=self.input_pw)
            pop_avg = 0
            pop_sum = 0
            for i in range(len(pop_sorted)):
                pop_sum += pop_sorted[i][1]
            pop_avg = pop_sum / len(pop_sorted)

            if int(pop_sorted[0][1]) >= 99:
                self.x_lab.append(self.g + 1)  # 최종 x값 저장
                n = pop_sorted[0][1]
                self.y_lab.append(round(n, 2))  # 최종 y 값 100 저장 반올림 2자리 까지 출력
                print('===== %s번째 비밀번호 탐색 =====' % (self.g + 1))
                print(pop_sorted[0], pop_avg, sep="   ")  # 출력할 때 pop_avg sep 지우기
                print('\n비밀번호를 찾았습니다!! :  %s' % (pop_sorted[0][0]))
                print(self.x_lab, self.y_lab, sep="   ")
                self.endNum+=1

                self.menu.tt1.configure(text="찾은 비밀번호 :  " + str(pop_sorted[0][0]))
                return self.g+1, self.endNum

            survivors = select_survivors(population_sorted=pop_sorted, best_sample=self.best_sample, lucky_few=self.lucky_few,
                                         password_len=pred_len)

            children = create_children(parents=survivors, n_child=self.n_child)

            new_generation = mutate_population(population=children, chance_of_mutation=10)

            self.pop = new_generation

            self.x_lab.append(self.g + 1)  # x축 저장
            self.y_lab.append(round(pop_avg, 2))  # y축 저장 반올림 2자리 까지 출력
            print('===== %s번째 비밀번호 탐색 =====' % (self.g + 1))
            print(pop_sorted[0], pop_avg, sep="   ")  # 출력할 때 pop_avg sep 지우기
            self.menu.tt1.configure(text="찾은 비밀번호 :"+str(pop_sorted[0][0]))
            self.g+=1

            return self.g+1, round(pop_avg, 2)

class App:

    x=[]
    y=[]
    t = plt
    regr_magic = RegrMagic


    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("200x100")
        self.tt = Label(self.window, text="비밀 번호를 입력하세요:")
        self.e1 = Entry(self.window,show="*")

        self.tt.pack()
        self.e1.pack()
        self.resultButton = Button(self.window, text="시작", command=self.startGenetic)
        self.resultButton.pack()

        self.fig = self.t.figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig,self.window)

        self.window.mainloop()

    def animate(self, args):
        self.x.append(args[0])
        self.y.append(args[1])

        if (args[1] == 101):
            #return plt.plot(self.x, self.y, color='g')
            self.anim.event_source.stop()
            self.resultButton.configure(state='normal')


        return plt.plot(self.x, self.y, color='g')

    def frames(self):
        while True:
            yield self.regr_magic()

    def startGenetic(self):
        if (len(self.e1.get()) > 1):
            self.chartWindow=tk.Toplevel(self.window)
            self.x.clear()
            self.y.clear()

            self.canvas=None

            self.tt1 = Label(self.chartWindow, text="찾은 비밀번호 :", font=("맑은 고딕", 20))
            self.tt1.pack()

            self.fig = self.t.figure(figsize=(5, 4), dpi=100)
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.chartWindow)
            self.canvas.get_tk_widget().pack()

            self.ax1 = self.fig.add_subplot(1, 1, 1)

            self.ax1.set_title("Genetic_Algorithm")
            self.ax1.set_xlabel('Generation', fontsize=10)
            self.ax1.set_ylabel('Score', fontsize='medium')
            self.regr_magic = RegrMagic(self.e1.get(), self)

            self.anim = animation.FuncAnimation(self.fig, self.animate, frames=self.frames, interval=1, blit=False)
            self.resultButton.configure(state='disabled')
        else:
            tkinter.messagebox.showinfo("메세지 상자","두글자 이상을 입력하여주세요.")
App()