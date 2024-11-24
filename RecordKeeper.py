import os
from datetime import datetime
from settings import Settings
import csv
from functools import wraps

def persist_result(request, return_query, answers):
    def write_to_csv(filename, headers, row):
        file_exists = os.path.exists(filename)
        mode = 'a' if file_exists else 'w'
        with open(filename, mode, newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(headers)
            writer.writerow(row)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    question = request.search

    # Write BERT result
    bert_headers = ['Timestamp', 'Question', 'Result']
    bert_row = [timestamp, question, return_query['BERT_MODEL']]
    write_to_csv(app_settings.bert_result_file_name, bert_headers, bert_row)

    # Write Gemini result
    gemini_headers = ['Timestamp', 'Question', 'Result']
    gemini_row = [timestamp, question, return_query['GEMINI']]
    write_to_csv(app_settings.gemini_result_file_name, gemini_headers, gemini_row)

    # Write Retrieval result
    retrieval_headers = ['Timestamp', 'Question', 'Result']
    retrieval_row = [timestamp, question, [answers]]
    write_to_csv(app_settings.retrieval_result_file_name, retrieval_headers, retrieval_row)


def Record(file_name):
    file_path = app_settings.records_dir+file_name
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            
            input_data = {"args": args, "kwargs": kwargs}
            output_data = result
            headers = ["input", "output"]

            file_exists = os.path.exists(file_path)
            mode = 'a' if file_exists else 'w'
            with open(file_path, mode, newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(headers)
                writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"),str(input_data), str(output_data)])
            
            return result
        return wrapper
    return decorator


app_settings = Settings()

