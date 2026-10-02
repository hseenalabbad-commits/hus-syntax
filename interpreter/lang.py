import sys
import MyTokens

if len(sys.argv) < 2:
    print("Error: No input file provided!", file=sys.stderr)
    sys.exit(1)

file_path = sys.argv[1]
tkns = MyTokens.Tokens.KEYWORDS

# قاموس لتخزين المتغيرات
variables = {}

try:
    with open(file_path, 'r', encoding='utf-8') as code:
        print("\n")
        
        for line_num, line in enumerate(code, 1):
            clean_line = line.strip()
            
            # تجاهل السطور الفارغة والتعليقات
            if not clean_line or clean_line.startswith('#'):
                continue
            
            parts = clean_line.split()
            cmd = parts[0]
            
            # 1. أمر الطباعة: print
            if cmd in tkns and cmd == tkns["print"]:
                if len(parts) < 2:
                    raise ValueError(f"What Are You Want To Print? \"LINE: {line_num}\"")
                
                # نجمع باقي السطر كنص كامل بعد كلمة print ونشيل علامات التنصيص الزائدة
                full_text = " ".join(parts[1:]).strip('"\'')
                
                # نبحث عن أي متغير داخل النص محصور بين أقواس مثل {name} ونبدله بقيمته
                for var_key, var_val in variables.items():
                    placeholder = f"{{{var_key}}}"
                    if placeholder in full_text:
                        full_text = full_text.replace(placeholder, str(var_val))
                
                # لو اليوزر كتب اسم متغير لوحده بدون نص (مثل print name)
                if full_text in variables:
                    print(variables[full_text], "\n")
                else:
                    print(full_text, "\n")
            
            # 2. تعريف المتغيرات باستخدام set (مثال: set name = hseen)
            elif cmd in tkns and cmd == tkns["set"]:
                if len(parts) < 4:
                    raise ValueError(f"Syntax Error in set at \"LINE: {line_num}\"")
                
                var_name = parts[1]
                var_value = " ".join(parts[3:]).strip('"\'') 
                
                # لو اليوزر خزن قيمة متغير في متغير تاني
                if var_value in variables:
                    var_value = variables[var_value]
                
                # تحويل الأرقام إلى int حقيقي
                elif var_value.isdigit():
                    var_value = int(var_value)
                
                variables[var_name] = var_value
            
            else:
                print(f"Hus Error at line {line_num}: Unknown command -> {cmd}", file=sys.stderr)
                
except FileNotFoundError:
    print(f"Error: File '{file_path}' not found!", file=sys.stderr)