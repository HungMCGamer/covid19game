import random
import sys
import tkinter as Tk
from tkinter import Button, Frame, Label, LabelFrame, messagebox, PhotoImage, Tk, W, Entry
import xlrd
import time, os
from random import seed
from random import randint
from random import shuffle

seed(1)

class Bq:
    total_questions = 0
    your_score = 0
    qcount = 1
    answer = ''
    wrong = ''
    choy = ''
    quest_frame = None
    ans_choices_frame = None
    your_rating = 0
    pc = 0
    player_name = ''
    level_round_current = 0
    index_question = 0
    tmp_count = 0
    #following vars  will eventually come from a config file.
    window_title = 'Trờ chơi Phòng chống dịch Covid-19'

# Set up main window.
root = Tk()
root.title(Bq.window_title)

# Frame for logo display.
logo_frame = LabelFrame(root)
logo_frame.grid(row=0, column=0)

# Load in and display logo image.
logo_lbl = Label(logo_frame)
PHOTO = PhotoImage(file=f'covid-logo.png')
logo_lbl.config(image=PHOTO)
logo_lbl.grid(row=0, column=0, padx=2, pady=2)
logo_lbl.photo = PHOTO

# Frame for question counter.
qcount_frame = Frame(root)
qcount_frame.grid()

# Frame for printing questions.
Bq.quest_frame = Frame(root)
Bq.quest_frame.grid(row=2, column=0, padx=5, pady=8)

# Frame for printing the 4 poss answer choices in.
Bq.ans_choices_frame = Frame(root)
Bq.ans_choices_frame.grid(row=3, column=0, padx=5, pady=8)

# Frame for the answer buttons.
btns_frame = LabelFrame(root)
btns_frame.grid(padx=5, pady=8)

# Frame for score counter.
score_frame = Frame(root, pady=20)
score_frame.grid()

# Give the location of the file
Loc_of_QA = ("QnA.xls")
# To open Workbook
wb = xlrd.open_workbook(Loc_of_QA)
sheet = wb.sheet_by_index(0)
sheet.cell_value(2, 0)
ques_list=[]
ans_list=[]
index_list=[]
difficult_level=[]
for i in range(sheet.nrows):
    index_list.append(i)
    ques_list.append(sheet.cell_value(i, 2))
    difficult_level.append(sheet.cell_value(i, 1))
    if sheet.cell_value(i, 7) == "A":
        ans_list.append(sheet.cell_value(i, 3))
        ans_list.append(sheet.cell_value(i, 4))
        ans_list.append(sheet.cell_value(i, 5))
        ans_list.append(sheet.cell_value(i, 6))
    elif sheet.cell_value(i, 7) == "B":
        ans_list.append(sheet.cell_value(i, 4))
        ans_list.append(sheet.cell_value(i, 3))
        ans_list.append(sheet.cell_value(i, 5))
        ans_list.append(sheet.cell_value(i, 6))
    elif sheet.cell_value(i, 7) == "C":
        ans_list.append(sheet.cell_value(i, 5))
        ans_list.append(sheet.cell_value(i, 3))
        ans_list.append(sheet.cell_value(i, 4))
        ans_list.append(sheet.cell_value(i, 6))
    elif sheet.cell_value(i, 7) == "D":
        ans_list.append(sheet.cell_value(i, 6))
        ans_list.append(sheet.cell_value(i, 3))
        ans_list.append(sheet.cell_value(i, 4))
        ans_list.append(sheet.cell_value(i, 5))
    else:
        ans_list.append(sheet.cell_value(i, 6))
        ans_list.append(sheet.cell_value(i, 3))
        ans_list.append(sheet.cell_value(i, 4))
        ans_list.append(sheet.cell_value(i, 5))
# For row 0 and column 0

shuffle(index_list)
#print(difficult_level)
#print(ques_list[0])
#print(index_list)


# Load questions into a list called quest_list.
#with open('questions.txt', 'r') as f:
    # splitlines removes the newline esc char.
#    ques_list = f.read().splitlines()
#    print(ques_list)

# Find out how many questions were loaded in.
Bq.total_questions = (len(ques_list))

# Load multiple choice answers into ans_list.
#with open('answers.txt', 'r') as f:
#    ans_list = f.read().splitlines()

def get_rating():
    """Get percentage of questions answered correctly
        and link it to a game over message."""
    Bq.your_rating = 0
    per_cent = 100 * float(Bq.your_score)/20
    temp = round(per_cent, 3)
    Bq.pc = str(temp)+'%'

    if per_cent < 26:
        Bq.your_rating = 'Kêt quả không được tốt, ' + str(Bq.player_name)+ ' đã nghiêm túc thực hiện chưa?'
        return
    if per_cent < 51:
        Bq.your_rating = 'Kêt quả tạm chấp nhận được, ' + str(Bq.player_name)+ ' hãy cố gắng trong lần chơi tới nhé!'
        return
    if per_cent < 76:
        Bq.your_rating = 'Hi, kết quả tốt đó. Nhưng ' + str(Bq.player_name)+ 'cũng cần cải thiện thêm.'
        return
    if per_cent < 101:
        Bq.your_rating = 'Kêt quả quá tuyệt vời, ' + str(Bq.player_name)+ ' thực sự hiểu quá rõ về covid-19!'
        return

def check_end_game():
    """Check if game over, if so get rating and end game."""
    get_rating()

    if Bq.index_question == (20):
        messagebox.showinfo(Bq.window_title, 'Trờ chơi kết thúc\n\n Kêt quả của ' + str(Bq.player_name)+ ' là '
                            +str(Bq.your_score)+ ' trên tổng số  '
                            +str(20)+'\n\n'
                            +str(Bq.your_rating))
        root.destroy()
        sys.exit()

def update_score():
    """Update the players score label."""
    score_label = Label(score_frame,
                        bg='plum', font=('Arial', 14, 'bold'),
                        text='Điểm hiện tại của ' + str(Bq.player_name)+ ' là: ' + str(Bq.your_score))

    score_label.grid(row=0, column=0)


def correctly_answered():
    """Pop up msgbox if answered correctly."""
    messagebox.showinfo(Bq.window_title,
                        str(Bq.answer)+' chính xác !\n\n'
                        'Xin chúc mừng ' + str(Bq.player_name)+ ', bạn đã có thêm điểm.')

    Bq.tmp_count += 1 # Next question.
    check_end_game()
    display_quest_count()
    display_question()
    display_answer_choices()

def wrong_answer():
    """Pop up box if answered incorrectly."""
    messagebox.showinfo(Bq.window_title,
                        str(Bq.wrong)+'  không chính xác !\n\n'
                        '' + str(Bq.player_name)+ ' không được nhận thêm điểm nào.')

    Bq.tmp_count += 1
    check_end_game()
    display_quest_count()
    display_question()
    display_answer_choices()

def display_quest_count():
    """Show question number."""

    qcount_label = Label(qcount_frame, bg='skyblue', fg='white',
                         font=('Arial', 14, 'bold'),
                         text='Vòng ' + str(Bq.level_round_current + 1) +'/4: ' + 'câu hỏi số ' + str(Bq.index_question + 1)+'/20 ')
                        
    qcount_label.grid(row=1, column=0)


def display_question():
    """Display question."""
    Bq.quest_frame.destroy()
    Bq.quest_frame = Frame(root)
    Bq.quest_frame.grid(row=2, column=0, padx=5, pady=8)
    Bq.index_question = Bq.index_question + 1
    if (Bq.index_question == 6):
       Bq.level_round_current = 1
       Bq.tmp_count = 1
    if (Bq.index_question == 11):
       Bq.level_round_current = 2
       Bq.tmp_count = 1
    if (Bq.index_question == 16):
       Bq.level_round_current = 3
       Bq.tmp_count = 1

    if Bq.level_round_current == 0:
      while (difficult_level[index_list[Bq.tmp_count]] != 'M1'):
#            print(Bq.qcount)
#            print(index_list[Bq.qcount])
#            print (difficult_level[index_list[Bq.qcount]])
            Bq.tmp_count = Bq.tmp_count + 1
    
    if Bq.level_round_current == 1:
      while (difficult_level[index_list[Bq.tmp_count]] != 'M2'):
#            print(Bq.qcount)
#            print(index_list[Bq.qcount])
#            print (difficult_level[index_list[Bq.qcount]])
            Bq.tmp_count = Bq.tmp_count + 1
    
    if Bq.level_round_current == 2:
      while (difficult_level[index_list[Bq.tmp_count]] != 'M3'):
#            print(Bq.qcount)
#            print(index_list[Bq.qcount])
#            print (difficult_level[index_list[Bq.qcount]])
            Bq.tmp_count = Bq.tmp_count + 1

    if Bq.level_round_current == 3:
      while (difficult_level[index_list[Bq.tmp_count]] != 'M4'):
#            print(Bq.qcount)
#            print(index_list[Bq.qcount])
#            print (difficult_level[index_list[Bq.qcount]])
            Bq.tmp_count = Bq.tmp_count + 1

#    print(Bq.tmp_count)
#    print(index_list[Bq.tmp_count])
#    print (difficult_level[index_list[Bq.tmp_count]])
    Bq.qcount = index_list[Bq.tmp_count]
    quest_ion = (ques_list[Bq.qcount])
    quest_label = Label(Bq.quest_frame, height=3,
                        fg='blue', wraplength=330, justify='left',
                        font=('Arial', 11, 'italic', 'bold'),
                        text='Câu hỏi: ' + quest_ion)

    quest_label.grid(row=0, column=0)

def display_answer_choices():
    """Show the multiple choice answers."""
    correct_answer = Bq.qcount *4

    Bq.ans_choices_frame.destroy()
    Bq.ans_choices_frame = Frame(root)
    Bq.ans_choices_frame.grid(row=3, column=0, padx=5, pady=8)

    # Need to get the four multiple choice answers into a list so
    # the answers can be shuffled randomly.
    temp1 = ans_list[Bq.qcount * 4]
    temp2 = ans_list[Bq.qcount * 4+1]
    temp3 = ans_list[Bq.qcount * 4+2]
    temp4 = ans_list[Bq.qcount * 4+3]

    # Have to join like this, I dont know other way to do it,
    # but doing it this way makes a tuple which cant be shuffled.
    tup = (temp1), (temp2), (temp3), (temp4)

    # So convert tuple to a list, otherwise can't shuffle it.
    Bq.choy = list(tup)

    # Mix up the sequence of answers because in ans_list the correct
    # answer is always first.
    random.shuffle(Bq.choy)

    # Print the answer choices, now they are in a random order.
    ans_0 = Label(Bq.ans_choices_frame, font=('Arial', 10, 'bold'),
                  text='A. ' + Bq.choy[0])
    ans_0.grid(row=0, column=0, sticky=W)
    ans_1 = Label(Bq.ans_choices_frame, font=('Arial', 10, 'bold'),
                  text='B. ' + Bq.choy[1])
    ans_1.grid(row=1, column=0, sticky=W)
    ans_2 = Label(Bq.ans_choices_frame, font=('Arial', 10, 'bold'),
                  text='C. ' + Bq.choy[2])
    ans_2.grid(row=2, column=0, sticky=W)
    ans_3 = Label(Bq.ans_choices_frame, font=('Arial', 10, 'bold'),
                  text='D. ' + Bq.choy[3])
    ans_3.grid(row=3, column=0, sticky=W)

    Bq.answer = ans_list[correct_answer]

def clkd_but_a():
    """Answer button A was clicked."""
    if Bq.answer == Bq.choy[0]:
        Bq.your_score += 1
        update_score()
        correctly_answered()
    else:
        Bq.wrong = Bq.choy[0]
        wrong_answer()

def clkd_but_b():
    """Answer button B was clicked."""
    if Bq.answer == Bq.choy[1]:
        Bq.your_score += 1
        update_score()
        correctly_answered()
    else:
        Bq.wrong = Bq.choy[1]
        wrong_answer()

def clkd_but_c():
    """Answer button C was clicked."""
    if Bq.answer == Bq.choy[2]:
        Bq.your_score += 1
        update_score()
        correctly_answered()
    else:
        Bq.wrong = Bq.choy[2]
        wrong_answer()

def clkd_but_d():
    """Answer button D was clicked."""
    if Bq.answer == Bq.choy[3]:
        Bq.your_score += 1
        update_score()
        correctly_answered()
    else:
        Bq.wrong = Bq.choy[3]
        wrong_answer()

# GUI buttons A B C D.
btn_a = Button(btns_frame, bg='gold',
               font=('Arial', 14, 'bold'), text=' A ',
               command=clkd_but_a)
btn_a.grid(row=5, column=0, pady=15, padx=15)

btn_b = Button(btns_frame, bg='red',
               font=('Arial', 14, 'bold'), text=' B ',
               command=clkd_but_b)
btn_b.grid(row=5, column=1, pady=15, padx=15)

btn_c = Button(btns_frame, bg='springgreen',
               font=('Arial', 14, 'bold'), text=' C ',
               command=clkd_but_c)
btn_c.grid(row=5, column=2, pady=15, padx=15)

btn_d = Button(btns_frame, bg='white',
               font=('Arial', 14, 'bold'), text=' D ',
               command=clkd_but_d)
btn_d.grid(row=5, column=3, pady=15, padx=15)


def Start_the_game(player_name_game):
  Bq.player_name = player_name_game
  messagebox.showinfo(Bq.window_title,'Xin chào '   + str(Bq.player_name)  + ' tới Trờ chơi Phòng chống dịch Covid-19 !')
  NameCheck01 = Bq.player_name
  while True:
    if NameCheck01 == '':
      messagebox.showerror(title='Lỗi', message='Tên đăng nhập không hợp lệ! Vui lòng khởi động lại trò chơi')

    else:
      break
  
  Bq.quest_frame.destroy()
  display_quest_count()
  display_question()
  display_answer_choices()
  update_score()
  btns_frame = LabelFrame(root)
  btns_frame.grid(padx=5, pady=8)
  btn_a = Button(btns_frame, bg='gold',
               font=('Arial', 14, 'bold'), text=' A ',
               command=clkd_but_a)
  btn_a.grid(row=5, column=0, pady=15, padx=15)

  btn_b = Button(btns_frame, bg='red',
               font=('Arial', 14, 'bold'), text=' B ',
               command=clkd_but_b)
  btn_b.grid(row=5, column=1, pady=15, padx=15)

  btn_c = Button(btns_frame, bg='springgreen',
               font=('Arial', 14, 'bold'), text=' C ',
               command=clkd_but_c)
  btn_c.grid(row=5, column=2, pady=15, padx=15)

  btn_d = Button(btns_frame, bg='white',
               font=('Arial', 14, 'bold'), text=' D ',
               command=clkd_but_d)
  btn_d.grid(row=5, column=3, pady=15, padx=15)

# Register name to access the game.
btns_frame.destroy()
Name_Filling = Label(Bq.quest_frame, text = " Xin mời nhập tên!")
print ('Registered as ', Bq.player_name)
NameCheck01 = Bq.player_name
    
Name_Filling.pack()

myEntry = Entry(Bq.quest_frame, width=20)
myEntry.focus()
#myEntry.bind(myEntry.get(), Start_the_game)
myEntry.pack()

enterEntry = Button(Bq.quest_frame, text= "Enter", command= lambda: Start_the_game(myEntry.get()))
enterEntry.pack()

# Start game.
#display_quest_count()
#display_question()
#display_answer_choices()
#update_score()

root.mainloop()
