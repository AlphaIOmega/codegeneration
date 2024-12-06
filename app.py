from flask import Flask, jsonify
import openpyxl
import os

app = Flask(__name__)

# Path to the Excel file

EXCEL_FILE = "codes.xlsx"


@app.route('/generate-code', methods=['GET'])
def generate_code():
    if not os.path.exists(EXCEL_FILE):
        return (jsonify({'success': False,
                'message': 'Excel file not found.'}), 404)

    try:

        # Load the Excel workbook

        wb = openpyxl.load_workbook(EXCEL_FILE)
        sheet = wb.active

        # Find the first unused code in column A

        for row in sheet.iter_rows(min_row=1, max_col=1):
            cell = row[0]
            if cell.value and not cell.font.strike:  # Unused code (not strikethrough)
                code = cell.value

                # Mark the code as used by applying a strikethrough

                cell.font = openpyxl.styles.Font(strike=True)
                wb.save(EXCEL_FILE)
                return jsonify({'success': True, 'code': code})

        return jsonify({'success': False,
                       'message': 'No unused codes available.'})
    except Exception, e:

        return (jsonify({'success': False, 'message': str(e)}), 500)

if __name__ == '__main__':
    app.run(debug=True)
