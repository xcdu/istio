
import re
#remove /u/username and url
'''
# open your csv and read as a text string
with open('text-wash3.csv', 'r') as f:
    my_csv_text = f.read()

find_str = '/u/'
replace_str = 'user@'

# substitute
new_csv_str = re.sub(find_str, replace_str, my_csv_text)

# open new file and save
new_csv_path = 'text-wash4.csv' # or whatever path and name you want
with open(new_csv_path, 'w') as f:
    f.write(new_csv_str)
'''
with open('text-wash4.csv', 'r') as f:
    my_csv_text = f.read()

#find_str = r'http\S+'
replace_str = '_URL_'

# substitute
new_csv_str = re.sub(r'http\S+', replace_str, my_csv_text)

# open new file and save
new_csv_path = 'text-wash5.csv'  # or whatever path and name you want
with open(new_csv_path, 'w') as f:
    f.write(new_csv_str)