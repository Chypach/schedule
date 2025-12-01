import openpyxl
from TTime import TodayYear




def NomOfWeek(n = 0):
    wb = openpyxl.load_workbook('weeks.xlsx')
    sheet = wb.active
    cell = sheet[f'A{int(TodayYear())+n}']
    # print(cell.value)
    if int(cell.value) == 1:
        return "odd_week"
    elif int(cell.value) == 2:
        return "even_week"

