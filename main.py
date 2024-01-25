import os
import ollama

# Path to your Obsidian vault
dir_path = "/Users/raf/Library/Mobile Documents/iCloud~md~obsidian/Documents/sol/Diary/"
files = [f for f in os.listdir(dir_path) if f.endswith(".md")]
sorted_files = sorted(files, reverse=True)[:7]


def summarise_single_note(note_content):
    response = ollama.chat(
        model="llama2",
        messages=[
            {
                "role": "user",
                "content": f"""
        
        Summarise the node below under 100 words.
        Use markdown bullet points.
        Every bullet point is one sentence.
        
        Note:
        {note_content}
        """.strip(),
            },
        ],
    )

    return response["message"]["content"]


def list_beautiful_things(note_content):
    response = ollama.chat(
        model="llama2",
        messages=[
            {
                "role": "user",
                "content": f"""
The note below contains a list of "Beautiful Things". 

== EXAMPLE_START ==
Beautiful things:

- Luna's amazing focaccia
- playing with the dog before dinner

== EXAMPLE_END ==

Extract the beautiful things from the note below. Do not introduce any new information. Do not include any text besides the list of beautiful things. Do not include the "Today:" list. 

        Note:
        {note_content}
        """.strip(),
            },
        ],
    )

    return response["message"]["content"]


file_contents = []
for file in sorted_files:
    with open(os.path.join(dir_path, file), "r") as f:
        file_contents.append(f.read())


print(f"Loaded {len(file_contents)} files")
print("🏁 Summarising...")

current_dir = os.path.dirname(os.path.realpath(__file__))
summaries_file_path = os.path.join(current_dir, "summaries.md")

if os.path.exists(summaries_file_path):
    os.remove(summaries_file_path)

for content in file_contents:
    note = summarise_single_note(content)
    with open(summaries_file_path, "w") as result_file:
        result_file.write(f"{note}\n\n------\n\n")

beautiful_things_path = os.path.join(current_dir, "beautiful_things.md")
if os.path.exists(beautiful_things_path):
    os.remove(beautiful_things_path)

for content in file_contents:
    note = list_beautiful_things(content)
    with open(beautiful_things_path, "w") as result_file:
        result_file.write(f"{note}\n\n------\n\n")

print("\n\n👍 Done!")
