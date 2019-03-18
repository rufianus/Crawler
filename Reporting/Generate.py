
import pandas
from Google.Cloud import MySQL


class Excel:


    def __init__(self, table_names):

        if isinstance(table_names, list):
            self.main_table_name = table_names[0]
            self.join_table_names = table_names.pop(0)
            repeats = ""
            proceed = True
            for char in self.main_table_name:
                if proceed is True:
                    repeats.append(char)
                    for join_table_name in self.join_table_names:
                        if repeats not in join_table_name:
                            repeats = repeats[:-1]
                            proceed = False
                            break
                elif proceed is False:
                    break
            self.file_name = [self.main_table_name]
            for join_table_name in self.join_table_names:
                self.file_name.extend(["_join_", join_table_name])
            self.file_name.append(".xlsx")
            self.file_name = ''.join(self.file_name)

    def IndexToColumn(self, index):

        column_reference = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        temp = (index + 1) // 26
        if temp != 0:
            excel_column_index = ''.join([str(column_reference[temp - 1]), column_reference[index - (temp * 26)]])
            return excel_column_index

    def QueryFromTable(self, column_lists, condition):

        MySQL = MySQL()
        query_data_frame = pandas.read_sql(''.join(MySQL.Command), MySQL.Connection)
        column_count = len(query_data_frame.columns)
        row_count = len(query_data_frame.index)
        if row_count == 0: print("No record in query:\n\n", MySQL.Command)
        elif row_count > 0:
            max_lengths = []
            column_names_list = query_data_frame.columns.values.tolist()
            column_index = 0
            for column_name in column_names_list:
                column_index += 1
                values_in_column = query_data_frame[column_name].tolist()
                max_length = 0
                for value in values_in_column:
                    length = len(str(value))*1.02
                    if length > max_length: max_length = length
                max_lengths.append([column_index, max_length])
            writer = pandas.ExcelWriter(self.file_name, engine='xlsxwriter')
            query_data_frame.to_excel(writer, 'Sheet1', index=False)
            workbook = writer.book
            worksheet = writer.sheets['Sheet1']
            last_excel_column = self.IndexToColumn(column_count - 1)
            cell_format = workbook.add_format()
            worksheet.freeze_panes(1, 3)
            worksheet.autofilter("A1:" + str(last_excel_column) + str(row_count - 1))
            for max_length_list in max_lengths:
                column_index = max_length_list[0]
                max_length = max_length_list[1]
                excel_column_index = self.IndexToColumn(column_index - 1)
                excel_column_index += (":" + excel_column_index)
                worksheet.set_column(excel_column_index, max_length, cell_format)
            writer.save()
            print(self.file_name + " saved.")


MySQL = MySQL(database_name="Delphi")
Excel = Excel(["DelphiCrawler_google_people"])
