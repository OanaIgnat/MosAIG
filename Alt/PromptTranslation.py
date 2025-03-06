from googletrans import Translator
import re
import time

def read_prompts(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Split by numbers followed by colon (e.g., "1:", "2:", etc.)
    prompts = re.split(r'\d+:\s*', content)
    # Remove empty strings and strip whitespace
    prompts = [p.strip() for p in prompts if p.strip()]
    return prompts

def translate_text(text, target_lang):
    translator = Translator()
    try:
        translation = translator.translate(text, dest=target_lang)
        return translation.text
    except Exception as e:
        print(f"\nError translating to {target_lang}: {str(e)}")
        return f"Translation Error for {target_lang}"

def process_file(input_filename):
    print("\nStarting translation process...")
    
    # Extract original filename without extension
    base_name = input_filename.rsplit('.', 1)[0]
    output_filename = f"MultiLingual-{input_filename}"
    
    # Get list of prompts
    prompts = read_prompts(input_filename)
    
    # Calculate total operations
    total_prompts = len(prompts)
    total_operations = total_prompts * 4  # 4 translations per prompt
    
    # Target languages
    languages = {
        'hi': 'Hindi',
        'de': 'German',
        'es': 'Spanish',
        'vi': 'Vietnamese'
    }
    
    # Process and write translations
    with open(output_filename, 'w', encoding='utf-8') as outfile:
        counter = 1
        operations_completed = 0
        
        for idx, prompt in enumerate(prompts, 1):
            # Write original English text
            outfile.write(f"{counter}: {prompt}\n")
            counter += 1
            
            # Translate and write for each target language
            for lang_code, lang_name in languages.items():
                # Update progress
                operations_completed += 1
                progress = (operations_completed / total_operations) * 100
                
                # Print progress
                print(f"\rProgress: {progress:.1f}% | Processing prompt {idx}/{total_prompts} | Translating to {lang_name}...", end="")
                
                # Add a small delay to avoid hitting rate limits
                time.sleep(0.5)
                
                translation = translate_text(prompt, lang_code)
                outfile.write(f"{counter}: {translation}\n")
                counter += 1
            
            # Add a blank line between sets
            outfile.write("\n")
    
    print(f"\n\nTranslation completed! Output saved to: {output_filename}")
    print(f"Total prompts processed: {total_prompts}")
    print(f"Total translations made: {total_operations}")

if __name__ == "__main__":
    input_filename = input("Enter the input filename (including extension): ")
    process_file(input_filename)