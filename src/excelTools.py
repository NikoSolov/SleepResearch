import xlsxwriter

def writeDataToPage(page, data: dict):
    for cell in data:
        if ":" in cell:
            page.merge_range(cell, data[cell])
        else:
            page.write(cell, data[cell])
