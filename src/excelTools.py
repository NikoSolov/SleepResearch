import xlsxwriter
import os

class ExcelTable:
  def __init__(self, dirPath, tableName):
    if not (os.path.exists(dirPath)):
        os.makedirs(dirPath)
    self.table = xlsxwriter.Workbook(os.path.join(dirPath, tableName))
    self.pages = []
  def createPage(self, pageName):
     return self.table.add_worksheet(pageName)
  def writeDataToPage(self, pageName: str, data: dict):
      page = self.table.get_worksheet_by_name(pageName)
      # print(page)
      for cell in data:
          if ":" in cell:
              page.merge_range(cell, data[cell])
          else:
              page.write(cell, data[cell])
  def close(self):
      self.table.close()