import os
import openai
import re

openai.api_key = os.getenv("OPENAI_API_KEY")


# Function to find the next available file number in the directory
def get_next_file_number(dir_path, level, short_topic):
    # Create a regex pattern to match filenames and extract numbers
    pattern = re.compile(rf"{level}_{short_topic.replace(' ', '_')}_p(\d+)_(\d+).txt")
    max_num = -1

    # List all files in the directory and find the highest number
    for filename in os.listdir(dir_path):
        match = pattern.match(filename)
        if match:
            num = int(match.group(2))  # The second group contains the number
            max_num = max(max_num, num)

    return max_num + 1  # Return the next available number

# levels = ["A2","B1","B2","C1","C2"]
levels = ["C2"]
topics = ["a sports topic or sport", "politics and government", "a technology", "a social issue", "an arts and culture", "a business", "a pop culture", "a random topic"]
short_topics = ["Sports", "Politics and government", "Technology", "Social issues", "Arts and culture", "Business", "Pop culture", "Random topic"]
languages = ["French", "Spanish"]
# languages = ["Italian", "French", "Spanish"]
short_languages = ["fr", "es"]
# short_languages = ["it", "fr", "es"]
prompts = ["Write a {level} level {language} text in a expository style about {topic} of your choice. Always include a title at the start.",
           "Write a {level} level {language} text in a descriptive style about {topic} of your choice. Always include a title at the start.",
           "Write a {level} level {language} narrative about {topic} of your choice. Always include a title at the start.",
           "Write a {level} level {language} argumentative piece on {topic} of your choice. Always include a title at the start.",
           "Write a {level} level {language} analytical text about {topic} of your choice. Always include a title at the start.",
           "Write a {level} level {language} text in a style of your choice about {topic} of your choice. Always include a title at the start."]

n=0
i=0
for level in levels:
  for language,short_language in zip(languages,short_languages):
    for topic, short_topic in zip(topics,short_topics):
      for prompt in prompts:
        formatted_prompt = prompt.format(level=level, language=language, topic=topic) # formatting text to fill in placeholders

        # Generate sample text with OpenAI API 
        completion = openai.ChatCompletion.create(
          model="gpt-4",
          messages=[
            {"role": "system","content": formatted_prompt}, 
          ]
        )
        GPT_text = completion.choices[0]['message']['content']

        # Define directory file path and ensure it exists
        dir_path = os.path.join(f"Content/{short_language}/{level}")
        os.makedirs(dir_path, exist_ok=True)  # Ensure the directory exists

        # Get the next available file number for the new filename
        file_num = get_next_file_number(dir_path, level, short_topic)
        filename = f"{level}_{short_topic.replace(' ', '_')}_p{n}_{file_num}.txt"
        filepath = os.path.join(dir_path, filename)

        # Write the generated text to a .txt file
        with open(filepath, 'w') as file:
          file.write(GPT_text)

        # recalculates the n to give the right prompt number
        n = (n + 1) % 6
        i += 1
        print(i)


