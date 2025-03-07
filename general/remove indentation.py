input_file_path = '../file/filter_file/filter_with_srt.py'
output_file_path = input_file_path.split('.')[0]+'1.'+input_file_path.split('.')[1]
with open(input_file_path, 'r') as input_file:
    content = input_file.read()

# Convert tabs to four spaces
content = content.expandtabs(4)

# Save the modified content to the output file
with open(output_file_path, 'w') as output_file:
    output_file.write(content)

print('----finished!!----')