from datasets import load_dataset

dataset = load_dataset("swaption2009/20k-en-zh-translation-pinyin-hsk",split=['train'])


for i in range(10):
    if dataset[0]['text'][i] == 'hsk: 1':
        print(dataset[0]['text'][i+1])

# def group_and_filter(data, desired_hsk_level):
#     # Initialize a list to hold grouped examples
#     examples = []
#     current_example = {}
    
#     # Iterate through each row in the dataset
#     for row in data:
#         text = row['row']['text']
#         if text.startswith('english:'):
#             # Start of a new example
#             if current_example:  # If there's an ongoing example, append it first
#                 examples.append(current_example)
#             current_example = {'english': text[len('english:'):].strip()}
#         elif text.startswith('hsk:'):
#             current_example['hsk'] = int(text[len('hsk:'):].strip())
#         elif text.startswith('mandarin:'):
#             current_example['mandarin'] = text[len('mandarin:'):].strip()
#         elif text.startswith('pinyin:'):
#             current_example['pinyin'] = text[len('pinyin:'):].strip()
#             # Assuming pinyin is the last part of an example, append it here
#             examples.append(current_example)
#             current_example = {}  # Reset for the next example
    
#     # Filter examples by the desired HSK level
#     filtered_examples = [ex for ex in examples if ex.get('hsk') == desired_hsk_level]
    
#     return filtered_examples

# # Example usage
# desired_hsk_level = 1
# filtered_data = group_and_filter(data, desired_hsk_level)

# # Print Mandarin text of each filtered example
# for example in filtered_data:
#     print(example['mandarin'])
