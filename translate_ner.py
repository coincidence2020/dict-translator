import json
import time
import os
from googletrans import Translator
from concurrent.futures import ThreadPoolExecutor

translator = Translator()
MAX_RETRIES = 5
TRANSLATION_DELAY = 0.5
LANGUAGES = ['zh-cn', 'de', 'ru']  # Target languages for translation

def translate_text(text, dest_lang):
    """Translate individual text to target language with retry mechanism."""
    for attempt in range(MAX_RETRIES):
        try:
            translated = translator.translate(text, src='en', dest=dest_lang).text
            print(f"Original: {text} -> Translated: {translated}")
            return translated
        except Exception as e:
            print(f"Translation error: {str(e)}, retrying ({attempt + 1}/{MAX_RETRIES})")
            time.sleep(TRANSLATION_DELAY * (attempt + 1))
    return text

def translate_entry(entry, dest_lang):
    """Translate the specific fields (text, PER, ORG, LOC) in the JSON entry."""
    # Translate 'text' field
    if 'text' in entry:
        entry['text'] = translate_text(entry['text'], dest_lang)

    # Translate entities within PER, ORG, LOC fields
    for tag in ['PER', 'ORG', 'LOC']:
        if tag in entry:
            # Translate each entity within the tag and replace with translated content
            entry[tag] = [translate_text(item, dest_lang) for item in entry[tag]]

    return entry

def process_file(input_path, output_dir):
    """Process the input JSONL file and output the translated files."""
    for lang in LANGUAGES:
        output_path = os.path.join(
            output_dir,
            f"{os.path.splitext(os.path.basename(input_path))[0]}_{lang}.jsonl"
        )

        with open(input_path, 'r', encoding='utf-8') as f_in, \
                open(output_path, 'w', encoding='utf-8') as f_out:

            # Using ThreadPoolExecutor for parallel processing of each line
            with ThreadPoolExecutor() as executor:
                futures = []
                for line in f_in:
                    entry = json.loads(line.strip())
                    futures.append(executor.submit(translate_entry, entry, lang))

                # Write the translated result into the output file
                for future in futures:
                    translated_entry = future.result()
                    f_out.write(json.dumps(translated_entry, ensure_ascii=False) + '\n')


if __name__ == "__main__":
    input_file = r'E:\onedrive\桌面\uner-20231114-092426\en_ewt-ud-train.jsonl'
    output_dir = r'E:\onedrive\桌面\uner-20231114-092426'

    print(f"Processing {input_file}...")

    start_time = time.time()
    process_file(input_file, output_dir)

    print(f"Completed in {time.time() - start_time:.2f}s")
    print(f"Translations saved to {output_dir}")
