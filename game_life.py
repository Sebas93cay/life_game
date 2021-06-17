#!/usr/bin/python3

from traceback import print_tb
import PySimpleGUI as sg
import time
from PySimpleGUI.PySimpleGUI import Multiline


def InitMat():
    return [[0 for i in range(30)] for j in range(30)]


def printMat(TextArea, Mat):
    text = ""
    for row in Mat:
        for i in row:
            if i == 0:
                text += "_"
            else:
                text += "#"
        text += '\n'
    TextArea.update(text)


def cellsBorn(mat, cells):
    for cell in cells:
        mat[cell[0]][cell[1]] = 1


def nextStep(Mat0, Mat1):
    for i, row in enumerate(Mat0):
        # print("i = {}".format(i))
        # print(row)
        for j, cell in enumerate(row):
            # print("LA GRAN i = {}".format(i))
            # print("EL GRAN j = {}".format(j))
            # print("CELLL IS "+str(cell))
            count = 0
            if cell == 0:
                for r_i in range(i-1, i + 2):
                    for c_i in range(j-1, j+2):
                        # print("r_i = {}".format(r_i))
                        # print("c_i = {}".format(c_i))
                        if c_i == 30:
                            c_i = 0
                        if r_i == 30:
                            r_i = 0
                        if c_i == -1:
                            c_i = 29
                        if r_i == -1:
                            r_i = 29
                        # print("end")
                        # print("r_i = {}".format(r_i))
                        # print("c_i = {}".format(c_i))
                        count += Mat0[r_i][c_i]
                if count == 3:
                    Mat1[i][j] = 1
                else:
                    Mat1[i][j] = 0
            else:
                for r_i in range(i-1, i + 2):
                    for c_i in range(j-1, j+2):
                        if c_i == 30:
                            c_i = 0
                        if r_i == 30:
                            r_i = 0
                        if c_i == -1:
                            c_i = 29
                        if r_i == -1:
                            r_i = 29
                        count += Mat0[r_i][c_i]
                count -= 1
                if count != 2 and count != 3:
                    Mat1[i][j] = 0
                else:
                    Mat1[i][j] = 1


layout = [[sg.Text("GAME OF LIFE")],
          [sg.Text('alives: '), sg.Input(
              '(10,10),(10,11),(11,11),(11,12),(12,11)', size=(20, 1), key='-INPUT-')],
          [sg.Button("GO")],
          [sg.Multiline(key='-ML-'+sg.WRITE_ONLY_KEY,
                        size=(30, 30), font=("Helvetica", 12))],
          [sg.Button("CLOSE"), sg.Text(key='-ITER-', size=(16, 1))]
          ]

# Create the window
window = sg.Window("GAME OF LIFE", layout, margins=(10, 10), finalize=True)

Mata = InitMat()
Mate = InitMat()

direction = 1

go = False
i = 0
while True:
    event, values = window.read(timeout=100)
    # End program if user closes window or
    # presses the OK button
    if event == "CLOSE" or event == sg.WIN_CLOSED:
        break

    if event == "GO":
        try:
            alives = eval('['+values['-INPUT-']+']')
            print(alives)
            if any([type(i) != tuple for i in alives]):
                raise Exception("ups")
            cellsBorn(Mata, alives)
            go = True
            printMat(window['-ML-'+sg.WRITE_ONLY_KEY], Mata)
        except Exception as e:
            print(e)
            sg.popup('ALIVE CELLS HAS TO BE TUPLES SEPARATED BY COMMAS')

    time.sleep(0.1)
    if go:
        if direction == 1:
            nextStep(Mata, Mate)
            printMat(window['-ML-'+sg.WRITE_ONLY_KEY], Mate)
            direction = 0

        else:
            nextStep(Mate, Mata)
            printMat(window['-ML-'+sg.WRITE_ONLY_KEY], Mata)
            direction = 1

        window['-ITER-'].update("iterations: {}".format(i))
        i += 1

window.close()
