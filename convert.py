import pandas as pd
import json
import re
import sys

def convert_excel_to_json(input_file, output_file):
    try:
        df = pd.read_excel(input_file)
    except Exception as e:
        print(f"Error reading file {input_file}: {e}")
        return

    if 'Query' not in df.columns or 'Response' not in df.columns:
        print("Error: The Excel file must contain 'Query' and 'Response' columns.")
        return

    result = []
    current_id = 1

    for index, row in df.iterrows():
        query = str(row['Query']) if pd.notna(row['Query']) else ''
        response = str(row['Response']) if pd.notna(row['Response']) else ''

        # 跳过缺少内容的列
        if not query.strip() or not response.strip() or query.lower() == 'nan' or response.lower() == 'nan':
            continue

        # 处理 user_query
        user_query = query.strip()
        
        # 处理 plan_list，通过正则表达式按 "数字. " 切分
        items = re.split(r'(?=\b\d+\.\s+)', response.strip())
        plan_list = []
        for item in items:
            item = item.strip()
            if item:
                plan_list.append({"plan_list": item})
                
        if not plan_list:
            plan_list.append({"plan_list": response.strip()})
             
        result.append({
            "id": current_id,
            "user_query": user_query,
            "plan_list": plan_list
        })
        current_id += 1

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    print(f"转换完成，结果已保存至 {output_file}")

if __name__ == "__main__":
    input_file = r"D:\Download\高阶数据处理样本_0620.xlsx"
    output_file = "output.json"
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    convert_excel_to_json(input_file, output_file)
