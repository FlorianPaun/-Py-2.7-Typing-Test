# author: Florian Paun, 1BK1T

import Tkinter as GUI
import random
import time

# region read configs
language = ""
behaviour = ""


def read_config():  # reads the language and behaviour from the config file
    global language, behaviour
    config = open('config.txt', "r")
    language = config.readline()[:-1]
    if language == "English" or language == "Englisch":
        language = "EN"
    elif language == "German" or language == "Deutsch":
        language = "DE"
    behaviour = str(config.readline())
    behaviour = behaviour
    config.close()


read_config()
# endregion configs

# region translations
translations = {"EN": ("TypeRacer (but it's the retarded version with no racing)",
                       "Settings",
                       "Mistakes: ",
                       "This run",
                       "Last run",
                       "Time: ",
                       "New sentence",
                       "Reset run"),
                "DE": ("TypeRacer, aber die behinderte Version ohne Racing",
                       "Einstellungen",
                       "Fehler: ",
                       "Dieser Satz",
                       "Letzter Satz",
                       "Zeit: ",
                       "Neuer Satz",
                       "Satz resetten")}
# endregion

# region variables that I kinda had to declare now
text = ""
answer = ""
mistakes = 0
answer_length = 0
time_this_run = 0
wpm_this_run = 0.0
cpm_this_run = 0.0
time_old_run = 0
wpm_old_run = 0.0
cpm_old_run = 0.0
# endregion

# region import random text
text_length = 0


def read_random_line(x):  # reads a random line of text from text_file and updates text_length
    global text, text_length, text_file
    n = random.randint(1, 30)
    if x == "EN":
        text_file = open("resources_EN.txt", "r")
    elif x == "DE":
        text_file = open("resources_DE.txt", "r")
    for i in range(n):
        text = text_file.readline()[:-1]
    text_length = len(text) - 1
    text_file.close()
    return text


read_random_line(language)
# endregion

# region Tkinter stuff
window_main = GUI.Tk()
window_main.configure(bg="white")
window_main.title(translations[language][0])
window_main.geometry("1280x720")
window_main.resizable(width=False, height=False)
window_main.focus_force()

text_GUI = GUI.Text(window_main, font="verdana 20", height="1", bd=0, width=str(text_length))
text_GUI.insert(GUI.INSERT, text)
text_GUI.configure(state='disabled')
text_GUI.tag_config("underline", font="verdana 20 underline")
text_GUI.tag_add("underline", "1.0")
text_GUI.place(anchor="nw", x=50, y=300)

answer_GUI = GUI.Label(window_main, text=answer, font="verdana 20", anchor="w", bg="white")
answer_GUI.place(anchor="nw", x=48, y=400)


def open_settings():
    import settings_window


settings_button = GUI.Button(window_main, text=translations[language][1], command=open_settings, width=11)
settings_button.place(anchor="nw", x=1189, y=690)

label_mistakes = GUI.Label(window_main, text=translations[language][2] + str(mistakes), bg="white")
label_mistakes.place(anchor="nw", x=1100, y=100)

label_this_run = GUI.Label(window_main, text=translations[language][3], bg="white")
label_this_run.place(anchor="nw", x=100, y=0)

label_old_run = GUI.Label(window_main, text=translations[language][4], bg="white")
label_old_run.place(anchor="nw", x=0, y=0)

label_wpm_this_run = GUI.Label(window_main, text="WPM: ", bg="white")
label_wpm_this_run.place(anchor="nw", x=100, y=30)

label_wpm_old_run = GUI.Label(window_main, text="WPM: ", bg="white")
label_wpm_old_run.place(anchor="nw", x=0, y=30)

label_cpm_this_run = GUI.Label(window_main, text="CPM: ", bg="white")
label_cpm_this_run.place(anchor="nw", x=100, y=50)

label_cpm_old_run = GUI.Label(window_main, text="CPM: ", bg="white")
label_cpm_old_run.place(anchor="nw", x=0, y=50)

label_time_this_run = GUI.Label(window_main, text=translations[language][5], bg="white")
label_time_this_run.place(anchor="nw", x=100, y=70)

label_time_old_run = GUI.Label(window_main, text=translations[language][5], bg="white")
label_time_old_run.place(anchor="nw", x=0, y=70)
# endregion

# region text marking functions


def mark_mistake(pos):  # marks a character as a mistake and removes the "correct" tag if there is one
    pos = "1." + pos
    if "correct" in text_GUI.tag_names(pos):
        text_GUI.tag_remove("correct", pos)
    text_GUI.tag_add("mistake", pos)
    text_GUI.tag_config("mistake", background="red")


def mark_correct(pos):  # marks a character in answer as correct, but only if it isn't marked as a mistake already
    pos = "1." + pos
    if "mistake" in text_GUI.tag_names(pos):
        text_GUI.tag_remove("mistake", pos)
    text_GUI.tag_add("correct", pos)
    text_GUI.tag_config("correct", background="green")


def underline(pos):  # underlines the next character
    pos = "1." + pos
    text_GUI.tag_add("underline", pos)
    for i in range(text_length):
        if i != int(pos[2:]):
            text_GUI.tag_remove("underline", "1." + str(i))


# endregion

# region time functions
start = 0
seconds = 0


def time_elapsed():  # returns the time elapsed in seconds
    global seconds
    if seconds == 0:
        seconds = int(time.time()) - start
    return seconds


def calculate_times():
    global time_this_run, wpm_this_run, cpm_this_run, start, seconds
    time_elapsed()
    time_this_run = seconds
    wpm_this_run = round(float(answer.count(" ")) / time_this_run * 60, 2)
    cpm_this_run = round(float(text_length) / time_this_run * 60, 2)
    label_time_this_run.configure(text=translations[language][5] + str(time_this_run) + " s")
    label_wpm_this_run.configure(text="WPM: " + str(wpm_this_run))
    label_cpm_this_run.configure(text="CPM: " + str(cpm_this_run))
    start = 0
    seconds = 0


def switch_times():  # switches stats of current run with last run and then clears them
    global time_this_run, wpm_this_run, cpm_this_run, time_old_run, wpm_old_run, cpm_old_run
    if wpm_this_run != 0:
        time_old_run = time_this_run
        wpm_old_run = wpm_this_run
        cpm_old_run = cpm_this_run
        time_this_run = 0
        wpm_this_run = 0
        cpm_this_run = 0
        label_time_old_run.configure(text=translations[language][5] + str(time_old_run) + " s")
        label_wpm_old_run.configure(text="WPM: " + str(wpm_old_run))
        label_cpm_old_run.configure(text="CPM: " + str(cpm_old_run))
        label_time_this_run.configure(text=translations[language][5])
        label_wpm_this_run.configure(text="WPM: ")
        label_cpm_this_run.configure(text="CPM: ")
# endregion

# region reset functions and buttons


def reset(event):  # clears answer, gets new text, switches times
    global answer, mistakes, start, text
    answer = ""
    answer_GUI.configure(text=answer)
    mistakes = 0
    label_mistakes.configure(text=translations[language][2] + str(mistakes))
    start = 0
    text = read_random_line(language)  # read new text
    text_GUI.configure(state='normal')  # enable widget
    text_GUI.delete("1.0", GUI.END)  # remove text from widget
    text_GUI.insert(GUI.INSERT, text)  # add new text
    text_GUI.configure(width=text_length, state='disabled')  # disable widget again
    text_GUI.tag_add("underline", "1.0")
    switch_times()


def reset_run():  # clears answer and reloads text, thus removing all tags
    global answer, answer_length, mistakes, start
    answer = ""
    answer_GUI.configure(text=answer)
    mistakes = 0
    label_mistakes.configure(text=translations[language][2] + str(mistakes))
    start = 0
    text_GUI.configure(state='normal')  # enable widget
    text_GUI.delete("1.0", GUI.END)  # remove text from widget
    text_GUI.insert(GUI.INSERT, text)  # add new text
    text_GUI.configure(state='disabled')  # disable widget again
    text_GUI.tag_add("underline", "1.0")
    switch_times()


button_reset = GUI.Button(window_main, text=translations[language][6], command=lambda: reset(""), width=11)
button_reset.place(anchor="nw", x=1189, y=660)

button_reset_run = GUI.Button(window_main, text=translations[language][7], command=reset_run, width=11)
button_reset_run.place(anchor="nw", x=1189, y=630)
# endregion


def update_answer(event):
    global answer, mistakes, text_length, answer_length, behaviour, start
    answer_length = len(answer) - 1
    if answer != text:
        if start == 0:  # start the timer on the first key press
            start = int(time.time())
        if behaviour == "1":
            # region easy behaviour, stops after a mistake and waits for the correct character
            if answer_length < text_length:  # doesn't add to the answer if it is already as long as the text
                answer = answer + event.char
                answer_GUI.configure(text=answer)
                answer_length = len(answer) - 1  # update answer length
            if answer[answer_length] != text[answer_length]:  # if characters don't match, add 1 mistake and mark it
                mistakes += 1
                label_mistakes.configure(text=translations[language][2] + str(mistakes))
                mark_mistake(str(answer_length))
                answer_GUI.configure(text=answer)
                answer = answer[:-1]  # and remove the character added last
            elif answer[answer_length] == text[answer_length]:  # if the characters match, mark as correct
                mark_correct(str(answer_length))
                underline(str(answer_length + 1))
                if answer_length == text_length:  # if the lengths also match then it's finished and can calculate stats
                    calculate_times()
                    text_GUI.tag_remove("underline", "1." + str(text_length))
            # endregion
        elif behaviour == "2":
            # region realistic behaviour, doesn't stop after a mistake and the user has to remove the wrong text
            if answer_length < text_length:  # doesn't add to the answer if it is already as long as the text
                answer = answer + event.char
                answer_GUI.configure(text=answer)
                answer_length = len(answer) - 1  # update answer length
                underline(str(answer_length + 1))
            if answer[:answer_length + 1] != text[:answer_length + 1]:
                mistakes += 1  # if all characters don't match, add 1 mistake and mark it
                label_mistakes.configure(text=translations[language][2] + str(mistakes))
                mark_mistake(str(answer_length))
                answer_GUI.configure(text=answer)
            elif answer[:answer_length] == text[:answer_length]:
                mark_correct(str(answer_length))
                if answer_length == text_length:
                    calculate_times()
            # endregion

# region key bindings


def backspace(event):  # removes the last character (if there are any) from answer
    global answer, answer_length
    if behaviour == "2":
        if len(answer) > 0 and answer != text:
            answer = answer[:-1]
            answer_GUI.configure(text=answer)
            answer_length = len(answer) - 1
        underline(str(answer_length + 1))


window_main.bind("<Key>", update_answer)
window_main.bind("<BackSpace>", backspace)
window_main.bind("<Control_L><Return>", reset)
# endregion

# region disabled keys


def nothing(event):
    pass


window_main.bind("<Shift_L>", nothing)
window_main.bind("<Shift_R>", nothing)
window_main.bind("<Control_L>", nothing)
window_main.bind("<Control_R>", nothing)
window_main.bind("<Alt_L>", nothing)
window_main.bind("<Alt_R>", nothing)
window_main.bind("<Caps_Lock>", nothing)
window_main.bind("<Cancel>", nothing)
window_main.bind("<Delete>", nothing)
window_main.bind("<Down>", nothing)
window_main.bind("<End>", nothing)
window_main.bind("<Escape>", nothing)
window_main.bind("<Execute>", nothing)
window_main.bind("<F1>", nothing)
window_main.bind("<F2>", nothing)
window_main.bind("<F3>", nothing)
window_main.bind("<F4>", nothing)
window_main.bind("<F5>", nothing)
window_main.bind("<F6>", nothing)
window_main.bind("<F7>", nothing)
window_main.bind("<F8>", nothing)
window_main.bind("<F9>", nothing)
window_main.bind("<F10>", nothing)
window_main.bind("<F11>", nothing)
window_main.bind("<F12>", nothing)
window_main.bind("<Home>", nothing)
window_main.bind("<Insert>", nothing)
window_main.bind("<Left>", nothing)
window_main.bind("<Linefeed>", nothing)
window_main.bind("<Next>", nothing)
window_main.bind("<Num_Lock>", nothing)
window_main.bind("<Pause>", nothing)
window_main.bind("<Print>", nothing)
window_main.bind("<Prior>", nothing)
window_main.bind("<Right>", nothing)
window_main.bind("<Scroll_Lock>", nothing)
window_main.bind("<Tab>", nothing)
window_main.bind("<Up>", nothing)
# endregion

window_main.mainloop()

# TO DO:
# bug: save settings button needs to be clicked twice for some reason
