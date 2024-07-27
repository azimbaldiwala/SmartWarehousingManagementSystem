from numpy import searchsorted
import openpyxl


def generateBill(bill_id, products: list, rates: list, quanity: list, bill_total_value):

    billStruct = openpyxl.load_workbook('Bill_structure.xlsx')
    sheet = billStruct['Sheet']

    bill_id_ = sheet[f'A2']
    bill_id_.value = "Bill ID: " + bill_id
  
    
    row = 6
    for i in range(len(products)):
        
        product_name = sheet[f'A{row}']
        product_name.value = str(products[i][0])

        product_rate = sheet[f'B{row}']
        product_rate.value = str(rates[i][0])

        product_quantity = sheet[f'C{row}']
        product_quantity.value = str(quanity[i])

        total = int(rates[i][0]) * int(quanity[i])

        product_total = sheet[f'D{row}']
        product_total.value = str(total)

        row += 1

    # Grand Total:

    row += 4

    grand_total_title = sheet[f'C{row}'] 
    grand_total_title.value = "Grand Total[INR]:"

    grand_total_value = sheet[f'D{row}']
    grand_total_value.value = str(bill_total_value)


    save_path = f"Bills/{bill_id}.xlsx"
    
    billStruct.save(save_path)
    billStruct.close()


#generateBill(100, ["Service"], ["1"], ["10000"], 10000)
