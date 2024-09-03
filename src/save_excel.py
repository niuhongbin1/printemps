'''
存 xlsx 
'''
import xlwings as xw 


def out(n,es):
    app = xw.App(visible=False)
    wb = app.books.add()
    sh = wb.sheets[0]
    sh.range('A1').value = es 
    sh.autofit()
    wb.save(n)
    wb.close()
    app.kill()


