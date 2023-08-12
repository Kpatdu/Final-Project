from PyQt6.QtWidgets import *
from gui import *
import csv
import os.path


class Logic(QMainWindow, Ui_MainWindow):
    """
    A class representing details for a person subject
    """
    def __init__(self):
        """
        Method to set default values and parameters of Logic Objects
        """
        super().__init__()
        self.setupUi(self)

        self.__num = 0
        self.label_students.setText(f"Student {self.__num + 1}")
        self.__score = []
        self.__score_error = None
        self.textBrowser.setText("Please select the number of courses")

        self.__student_dict = {}

        self.comboBox.addItems(["0", "1", "2", "3", "4",
                                "5", "6", "7", "8", "9"])
        self.comboBox.setCurrentIndex(0)
        self.__comboBoxNum = 0
        self.__lineList = [self.lineEdit_1, self.lineEdit_2, self.lineEdit_3, self.lineEdit_4,
                           self.lineEdit_5, self.lineEdit_6, self.lineEdit_7, self.lineEdit_8,
                           self.lineEdit_9]

        self.comboBox_Button.clicked.connect(lambda: self.num_scores())
        self.pushButton_save.clicked.connect(lambda: self.submit())
        self.pushButton_clear.clicked.connect(lambda: self.clear())
        self.pushButton_clear_all.clicked.connect(lambda: self.clear_all())
        self.pushButton_next.clicked.connect(lambda: self.next())
        self.pushButton_back.clicked.connect(lambda: self.back())
        self.pushButton_back.setEnabled(False)

    def num_scores(self):
        """
        Function that determines the number of "score-lines" that are present. This function will clear and add
        lines based on the variable "comboBoxNum".
        :return: Sets the current number of lines available based on the amount chosen by "self.__comboBox"
        """
        self.__score.clear()
        line_list = self.__lineList
        self.__comboBoxNum = int(self.comboBox.currentText())
        x = 0
        y = 8
        while x < self.__comboBoxNum:
            line_list[x].setEnabled(True)
            x += 1
        while y >= self.__comboBoxNum:
            line_list[y].setEnabled(False)
            line_list[y].clear()
            y -= 1
        if self.__comboBoxNum != 0:
            self.textBrowser.setText("Please Enter Values: (Integers and Floats between 0 to 100 are accepted)\n"
                                     "Anything above or below will be converted to the min or max.")
        else:
            self.textBrowser.setText("Please select the number of courses.")

    def submit(self):
        """
        Function will allow the user to submit their recorded results to the data (with the assumption that
        the information is accurate).
        :return: Will return an error if the function receives an Error, otherwise, continue as normal
        """
        check_score = self.check_score()
        if check_score is False:
            if self.__score_error is ValueError:
                self.textBrowser.setText("Values in the scores are incorrect. Integers and Floats between 0 to 100 "
                                         "are only accepted.\n" "Anything above or below will be "
                                         "converted to the min or max. e.g. 10, 10.4, 50, 20.6")
            elif self.__score_error is TypeError:
                self.textBrowser.setText("No Courses have been selected. Please pick an option in the drop-down.")
        else:
            self.student_scores()
            self.createCSV()

    def check_score(self):
        """
        Functions checks to see if the information put in the lineEdit's are floats. If the information inputted
        does not qualify with the limitations set, the function will return an error.
        :return: Returns "True" if the function performs as normal. Returns "False" on an error.
        """
        tf = False
        lineList = self.__lineList
        self.__score.clear()
        if self.__comboBoxNum != 0:
            try:
                num = self.__comboBoxNum
                x = 0
                while x < num:
                    if 0 <= float(lineList[x].text().strip()) <= 100:
                        self.__score.append(float(lineList[x].text().strip()))
                    elif float(lineList[x].text()) < 0:
                        self.__score.append(0)
                    elif float(lineList[x].text()) > 100:
                        self.__score.append(100)
                    x += 1
                tf = True
                self.__score_error = None
            except ValueError:
                self.__score_error = ValueError
            except TypeError:
                self.__score_error = TypeError
            finally:
                return tf
        else:
            self.__score_error = TypeError
            return tf

    def student_scores(self):
        """
        Function calculates the num, course list, max_num and average for the current student.
        :return: Creates an instance in the "self.__student_dict" of the current student with
        data
        """
        num = self.__comboBoxNum
        course_list = self.__score.copy()
        max_num = max(self.__score)
        average = sum(self.__score) / len(self.__score)
        gpa_list = []
        x = 0
        while x < len(self.__score):
            if self.__score[x] >= 90:
                gpa_list.append(4.00)
            elif self.__score[x] >= 80:
                gpa_list.append(3.00)
            elif self.__score[x] >= 70:
                gpa_list.append(2.00)
            elif self.__score[x] >= 60:
                gpa_list.append(1.00)
            elif self.__score[x] >= 50:
                gpa_list.append(0.00)
            else:
                gpa_list.append(-0.50)
            x += 1
        gpa = sum(gpa_list) / len(self.__score)
        self.__student_dict[self.__num] = {"num": num, "max_num": max_num, "average": average,
                                           "gpa": gpa, "courseScore": course_list}
        self.textBrowser.setText(f"Student {self.__num + 1} has taken {self.__student_dict[self.__num]['num']}"
                                 f" courses with a max grade of {self.__student_dict[self.__num]['max_num']}%"
                                 f", an average of {self.__student_dict[self.__num]['average']}% "
                                 f"and a GPA of {self.__student_dict[self.__num]['gpa']}")

    def createCSV(self):
        """
        Function creates a CSV file
        :return: Writes and updates the CSV file with the data from "self.__student_dict"
        """
        with open(f"outputCSV.csv", "w", newline="") as csvFile:
            content = csv.writer(csvFile)
            content.writerow(["Student", "Courses", "Max_Grade", "Average", "GPA"])
            x = 0
            if self.__student_dict[x]['num'] != 0:
                while x <= self.__num:
                    content.writerow([f"Student_{x + 1}", self.__student_dict[x]['num'],
                                      self.__student_dict[x]['max_num'],
                                      self.__student_dict[x]['average'],
                                      self.__student_dict[x]['gpa']])
                    x += 1

    def next(self):
        """
        Function that returns the user to the next student. If data for that student already existed, the
        data will be displayed, otherwise, nothing will display.
        :return: Brings the user to the next student
        """
        if self.__num not in self.__student_dict.keys():
            self.__student_dict[self.__num] = {"num": 0, "max_num": "N/A", "average": "N/A",
                                               "gpa": "N/A", "courseScore": 0}
        self.__num += 1
        self.label_students.setText(f"Student {self.__num + 1}")
        if self.__num not in self.__student_dict.keys():
            self.comboBox.setCurrentIndex(0)
            self.num_scores()
        else:
            x = 0
            self.__comboBoxNum = self.__student_dict[self.__num]['num']
            self.comboBox.setCurrentIndex(self.__comboBoxNum)
            self.num_scores()
            while x < self.__student_dict[self.__num]['num']:
                self.__lineList[x].clear()
                self.__lineList[x].insert(str(self.__student_dict[self.__num]['courseScore'][x]))
                x += 1
            self.textBrowser.setText(f"Student {self.__num + 1} has taken {self.__student_dict[self.__num]['num']}"
                                     f" courses with a max grade of {self.__student_dict[self.__num]['max_num']}%"
                                     f", an average of {self.__student_dict[self.__num]['average']}% "
                                     f"and a GPA of {self.__student_dict[self.__num]['gpa']}")
        self.pushButton_back.setEnabled(True)

    def back(self):
        """
        Function that returns the user back to a previous student. If data for that student already existed, the
        data will be displayed, otherwise, nothing will display.
        :return: Brings the user back to a previous student
        """
        if self.__num > 1:
            self.pushButton_back.setEnabled(True)
            self.__num -= 1
        elif self.__num == 1:
            self.pushButton_back.setEnabled(False)
            self.__num = 0

        self.label_students.setText(f"Student {self.__num + 1}")
        self.__comboBoxNum = self.__student_dict[self.__num]['num']
        if self.__num in self.__student_dict.keys() and self.__comboBoxNum != 0:
            x = 0
            self.__comboBoxNum = self.__student_dict[self.__num]['num']
            self.comboBox.setCurrentIndex(self.__comboBoxNum)
            self.num_scores()
            while x < self.__student_dict[self.__num]['num']:
                self.__lineList[x].clear()
                self.__lineList[x].insert(str(self.__student_dict[self.__num]['courseScore'][x]))
                x += 1
            self.textBrowser.setText(f"Student {self.__num + 1} has taken {self.__student_dict[self.__num]['num']}"
                                     f" courses with a max grade of {self.__student_dict[self.__num]['max_num']}%"
                                     f", an average of {self.__student_dict[self.__num]['average']}% "
                                     f"and a GPA of {self.__student_dict[self.__num]['gpa']}")
        else:
            self.clear()

    def clear(self):
        """
        Function that clears all data and resets the comboBox down to 0 for the current student.
        :return: The function resets the current student to a default value
        """
        self.comboBox.setCurrentIndex(0)
        self.num_scores()

        if self.__num in self.__student_dict:
            self.__student_dict[self.__num] = {"num": 0, "max_num": "N/A", "average": "N/A",
                                               "gpa": "N/A", "courseScore": 0}
            self.createCSV()

    def clear_all(self):
        """
        Function that clears all data and resets the comboBox down to 0 for the whole program.
        :return: The function resets the program back to its default value
        """
        self.comboBox.setCurrentIndex(0)
        self.num_scores()
        self.__num = 0
        self.label_students.setText(f"Student {self.__num + 1}")
        self.__score_error = None
        self.__student_dict.clear()
        self.pushButton_back.setEnabled(False)
        fileName = os.path.isfile("outputCSV.csv")
        if fileName is True:
            f = open("outputCSV.csv", "w+")
            content = csv.writer(f)
            content.writerow(["Student", "Courses", "Max_Grade", "Average", "GPA"])
            f.close()
