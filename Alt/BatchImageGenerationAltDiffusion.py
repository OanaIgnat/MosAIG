# import os
# import importlib.util
# import time

# def print_parameter_guidelines():
#     print("\n" + "="*80)
#     print("ALTDIFFUSION-M18 IMAGE GENERATOR".center(80))
#     print("="*80 + "\n")

#     print("PARAMETER GUIDELINES:")
#     print("-"*50)
#     print("\n1. Image Dimensions:")
#     print("   • Width and Height must be multiples of 8")
#     print("   • Recommended range: 512-1024")
#     print("   • Larger sizes require more GPU memory")
    
#     print("\n2. Seed Value:")
#     print("   • Any integer value")
#     print("   • Same seed = reproducible results")
#     print("   • Different seeds = unique variations")
#     print("   • Seed value doesn't affect quality, only randomization pattern")
    
#     print("\n3. Guidance Scale:")
#     print("   • Recommended range: 5.0-15.0")
#     print("   • Higher values = stronger adherence to prompt")
#     print("   • Lower values = more creative freedom")
#     print("   • Default: 7.5")
    
#     print("\n4. Inference Steps:")
#     print("   • Range: 20-150")
#     print("   • More steps = better quality but slower generation")
#     print("   • Default: 50")

#     print("\nSUPPORTED LANGUAGES:")
#     print("-"*50)
#     print("English, Chinese, Japanese, Thai, Korean, Hindi, Ukrainian, Arabic,")
#     print("Turkish, Vietnamese, Polish, Dutch, Portuguese, Italian, Spanish,")
#     print("German, French, and Russian")
    
#     print("\nPROMPT GUIDELINES:")
#     print("-"*50)
#     print("• Maximum length: 77 tokens")
#     print("• Exceeding tokens will be truncated")
#     print("• Be specific and yet descriptive")
#     print("• Use commas to separate different aspects")
    
#     print("\nCOMMANDS:")
#     print("-"*50)
#     print("• Type 'exit' or 'quit' at any prompt to end the program")
#     print("• Type 'guidelines' to see these guidelines again")
    
#     print("\n" + "="*80 + "\n")

# def get_validated_input(prompt_text, input_type, valid_range=None, multiple_of=None):
#     while True:
#         value = input(prompt_text).strip().lower()
        
#         # Check for exit commands
#         if value in ['exit', 'quit']:
#             return 'exit'
            
#         # Check for guidelines request
#         if value == 'guidelines':
#             print_parameter_guidelines()
#             continue
            
#         try:
#             value = input_type(value)
#             if valid_range and (value < valid_range[0] or value > valid_range[1]):
#                 print(f"Value must be between {valid_range[0]} and {valid_range[1]}")
#                 continue
#             if multiple_of and value % multiple_of != 0:
#                 print(f"Value must be a multiple of {multiple_of}")
#                 continue
#             return value
#         except ValueError:
#             print(f"Please enter a valid {input_type.__name__} value")

# def generate_images():
#     # Create output directory
#     output_dir = "m18-generated_output"
#     os.makedirs(output_dir, exist_ok=True)
    
#     # First load the model
#     print("\nLoading the model (this will take a few minutes)...")
#     try:
#         main2 = importlib.import_module("main-2")
#         main2.load_model()
#         print("\nModel loaded successfully!")
#     except Exception as e:
#         print(f"\nError loading model: {e}")
#         return

#     # Import main3 for generation
#     main3 = importlib.import_module("main-3")
    
#     print_parameter_guidelines()

#     # Main generation loop
#     while True:
#         print("\n" + "="*40)
#         print("NEW IMAGE GENERATION".center(40))
#         print("="*40)
        
#         # Get parameters
#         width = get_validated_input("\nEnter width (multiple of 8): ", int, [128, 1024], 8)
#         if width == 'exit': break
        
#         height = get_validated_input("Enter height (multiple of 8): ", int, [128, 1024], 8)
#         if height == 'exit': break
        
#         seed = get_validated_input("Enter seed (integer): ", int)
#         if seed == 'exit': break
        
#         guidance_scale = get_validated_input("Enter guidance scale (5.0-15.0): ", float, [5.0, 15.0])
#         if guidance_scale == 'exit': break
        
#         num_inference_steps = get_validated_input("Enter number of inference steps (20-150): ", int, [20, 150])
#         if num_inference_steps == 'exit': break
        
#         print("\nEnter your prompt (or 'exit' to quit):")
#         print("(Remember: supports multiple languages, max 77 tokens)")
#         prompt = input("> ").strip()
#         if prompt.lower() in ['exit', 'quit']: break
        
#         print("\nEnter filename to save the image (without extension):")
#         filename = input("> ").strip()
#         if filename.lower() in ['exit', 'quit']: break
        
#         # Generate image
#         try:
#             print("\nGenerating image...")
#             output_path = main3.generate_single_image(
#                 prompt=prompt,
#                 seed=seed,
#                 width=width,
#                 height=height,
#                 num_inference_steps=num_inference_steps,
#                 guidance_scale=guidance_scale,
#                 output_dir=output_dir,
#                 filename=filename
#             )
#             print(f"\nSuccess! Image saved to: {output_path}")
            
#             # Ask if user wants to generate another image
#             response = input("\nGenerate another image? (y/n): ").strip().lower()
#             if response != 'y':
#                 break
                
#         except Exception as e:
#             print(f"\nError generating image: {e}")
#             response = input("\nTry another image? (y/n): ").strip().lower()
#             if response != 'y':
#                 break

#     print("\nThank you for using AltDiffusion-M18 Image Generator!")

# if __name__ == "__main__":
#     generate_images()





# import os
# import shutil
# import torch
# import importlib.util
# import re
# from pathlib import Path

# def print_gpu_status(message="Current GPU Status"):
#     print(f"\n=== {message} ===")
#     print(f"GPU: {torch.cuda.get_device_name(0)}")
#     print(f"Total GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**2:.2f} MB")
#     print(f"Allocated GPU Memory: {torch.cuda.memory_allocated() / 1024**2:.2f} MB")
#     print(f"Cached GPU Memory: {torch.cuda.memory_reserved() / 1024**2:.2f} MB")
#     print(f"Free GPU Memory: {(torch.cuda.get_device_properties(0).total_memory - torch.cuda.memory_allocated()) / 1024**2:.2f} MB")
#     print("=" * 50)

# def process_prompt_file(file_path):
#     """
#     Process the input file containing numbered prompts and return a list of prompts.
#     Handles multi-line prompts and removes numbering.
#     """
#     prompts = []
#     current_prompt = []
#     current_number = 1

#     try:
#         with open(file_path, 'r', encoding='utf-8') as file:
#             for line in file:
#                 line = line.strip()
#                 if not line:  # Skip empty lines
#                     continue
                
#                 # Check if line starts with a number followed by colon
#                 match = re.match(r'(\d+):', line)
                
#                 if match:
#                     # If we have collected lines for previous prompt, save it
#                     if current_prompt:
#                         prompts.append(' '.join(current_prompt))
#                         current_prompt = []
                    
#                     # Start new prompt, remove the number prefix
#                     number = int(match.group(1))
#                     if number != current_number:
#                         raise ValueError(f"Expected prompt number {current_number}, but found {number}")
                    
#                     current_number += 1
#                     current_prompt.append(line[match.end():].strip())
#                 else:
#                     # Append to current prompt if there's one being collected
#                     if current_prompt:
#                         current_prompt.append(line)

#         # Don't forget to add the last prompt
#         if current_prompt:
#             prompts.append(' '.join(current_prompt))

#         return prompts

#     except Exception as e:
#         print(f"Error processing prompt file: {e}")
#         return []

# def generate_images():
#     # Print initial GPU status
#     print_gpu_status("Initial GPU Status")

#     # First load the model
#     print("\nLoading the model (this will take a few minutes)...")
#     try:
#         main2 = importlib.import_module("main-2")
#         main2.load_model()
#         print("\nModel loaded successfully!")
#     except Exception as e:
#         print(f"\nError loading model: {e}")
#         return

#     # Print GPU status after loading
#     print_gpu_status("GPU Status After Loading Model")

#     # Import main3 for generation
#     main3 = importlib.import_module("main-3")

#     # Get input file path
#     file_path = input("\nEnter the path to your prompt file (txt): ").strip()
#     if not os.path.exists(file_path):
#         print(f"Error: File {file_path} does not exist!")
#         return

#     # Create output directory based on input file name
#     output_dir = Path(file_path).stem
#     os.makedirs(output_dir, exist_ok=True)

#     # Copy input file to output directory
#     try:
#         shutil.copy2(file_path, output_dir)
#         print(f"\nCreated output directory: {output_dir}")
#         print(f"Copied prompt file to output directory")
#     except Exception as e:
#         print(f"Error copying file: {e}")
#         return

#     # Process prompts
#     prompts = process_prompt_file(file_path)
#     if not prompts:
#         print("No valid prompts found in file!")
#         return

#     # Hardcoded parameters
#     params = {
#         "width": 768,
#         "height": 768,
#         "guidance_scale": 11,
#         "num_inference_steps": 110,
#         "seed": 11000
#     }

#     # Generate images for each prompt
#     print("\nStarting image generation...")
#     for idx, prompt in enumerate(prompts, 1):
#         try:
#             print(f"\nGenerating image {idx}/{len(prompts)}")
#             output_path = main3.generate_single_image(
#                 prompt=prompt,
#                 output_dir=output_dir,
#                 filename=str(idx),
#                 **params
#             )
#             print(f"Saved image: {output_path}")
#         except Exception as e:
#             print(f"Error generating image {idx}: {e}")
#             continue

#     print("\nImage generation completed!")

# if __name__ == "__main__":
#     generate_images()





import os
import shutil
import torch
import importlib.util
import re
from pathlib import Path

def print_gpu_status(message="Current GPU Status"):
    print(f"\n=== {message} ===")
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"Total GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**2:.2f} MB")
    print(f"Allocated GPU Memory: {torch.cuda.memory_allocated() / 1024**2:.2f} MB")
    print(f"Cached GPU Memory: {torch.cuda.memory_reserved() / 1024**2:.2f} MB")
    print(f"Free GPU Memory: {(torch.cuda.get_device_properties(0).total_memory - torch.cuda.memory_allocated()) / 1024**2:.2f} MB")
    print("=" * 50)

def process_prompt_file(file_path, start_number=1):
    """
    Process the input file containing numbered prompts and return a list of prompts.
    Handles multi-line prompts and removes numbering.
    """
    prompts = []
    current_prompt = []
    current_number = 1

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:  # Skip empty lines
                    continue
                
                # Check if line starts with a number followed by colon
                match = re.match(r'(\d+):', line)
                
                if match:
                    # If we have collected lines for previous prompt, save it
                    if current_prompt and current_number >= start_number:
                        prompts.append((current_number, ' '.join(current_prompt)))
                        
                    current_prompt = []
                    
                    # Start new prompt, remove the number prefix
                    number = int(match.group(1))
                    if number != current_number:
                        raise ValueError(f"Expected prompt number {current_number}, but found {number}")
                    
                    current_number += 1
                    if current_number >= start_number:
                        current_prompt.append(line[match.end():].strip())
                else:
                    # Append to current prompt if there's one being collected
                    if current_prompt and current_number >= start_number:
                        current_prompt.append(line)

        # Don't forget to add the last prompt
        if current_prompt and current_number >= start_number:
            prompts.append((current_number - 1, ' '.join(current_prompt)))

        return prompts

    except Exception as e:
        print(f"Error processing prompt file: {e}")
        return []

def generate_images():
    # Print initial GPU status
    print_gpu_status("Initial GPU Status")

    # First load the model
    print("\nLoading the model (this will take a few minutes)...")
    try:
        main2 = importlib.import_module("main-2")
        main2.load_model()
        print("\nModel loaded successfully!")
    except Exception as e:
        print(f"\nError loading model: {e}")
        return

    # Print GPU status after loading
    print_gpu_status("GPU Status After Loading Model")

    # Import main3 for generation
    main3 = importlib.import_module("main-3")

    # Get input file path
    file_path = input("\nEnter the path to your prompt file (txt): ").strip()
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist!")
        return

    # Get starting number from user
    try:
        start_number = int(input("\nEnter starting number (0 for beginning): ").strip())
        if start_number < 0:
            print("Error: Starting number cannot be negative!")
            return
        start_number = 1 if start_number == 0 else start_number
    except ValueError:
        print("Error: Please enter a valid number!")
        return

    # Create output directory based on input file name
    output_dir = Path(file_path).stem
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"\nCreated output directory: {output_dir}")
        
        # Copy input file to output directory only if directory was just created
        try:
            shutil.copy2(file_path, output_dir)
            print(f"Copied prompt file to output directory")
        except Exception as e:
            print(f"Error copying file: {e}")
            return
    else:
        print(f"\nUsing existing output directory: {output_dir}")
        if not os.path.exists(os.path.join(output_dir, Path(file_path).name)):
            try:
                shutil.copy2(file_path, output_dir)
                print(f"Copied prompt file to output directory")
            except Exception as e:
                print(f"Error copying file: {e}")
                return

    # Process prompts
    prompts = process_prompt_file(file_path, start_number)
    if not prompts:
        print("No valid prompts found in file!")
        return

    # Hardcoded parameters
    params = {
        "width": 768,
        "height": 768,
        "guidance_scale": 11,
        "num_inference_steps": 110,
        "seed": 11000
    }

    # Generate images for each prompt
    print("\nStarting image generation...")
    total_prompts = len(prompts)
    for idx, (prompt_number, prompt) in enumerate(prompts, 1):
        try:
            print(f"\nGenerating image {idx}/{total_prompts} (Prompt #{prompt_number})")
            output_path = main3.generate_single_image(
                prompt=prompt,
                output_dir=output_dir,
                filename=str(prompt_number),
                **params
            )
            print(f"Saved image: {output_path}")
        except Exception as e:
            print(f"Error generating image {prompt_number}: {e}")
            continue

    print("\nImage generation completed!")

if __name__ == "__main__":
    generate_images()

