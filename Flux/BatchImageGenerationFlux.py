import os
import torch
from diffusers import FluxPipeline
import re
import shutil
from datetime import datetime
import zipfile

def get_gpu_info():
    """Get GPU memory information"""
    if torch.cuda.is_available():
        total = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        used = torch.cuda.memory_allocated(0) / (1024**3)
        free = total - used
        return {
            'total': f"{total:.2f} GB",
            'used': f"{used:.2f} GB",
            'free': f"{free:.2f} GB"
        }
    return "GPU not available"

def print_gpu_status(stage):
    """Print GPU status with stage label"""
    gpu_info = get_gpu_info()
    if isinstance(gpu_info, dict):
        print(f"\nGPU Status - {stage}:")
        print(f"Total Memory: {gpu_info['total']}")
        print(f"Used Memory: {gpu_info['used']}")
        print(f"Free Memory: {gpu_info['free']}")
    else:
        print(gpu_info)

def setup_model():
    """Setup and return the Flux model"""
    # Set custom cache directory
    os.environ['HF_HOME'] = '/WAVE/scratch2/oignat_lab/ParthBhaleraoWork/huggingface'
    os.environ['TRANSFORMERS_CACHE'] = '/WAVE/scratch2/oignat_lab/ParthBhaleraoWork/huggingface/transformers'
    os.environ['DIFFUSERS_CACHE'] = '/WAVE/scratch2/oignat_lab/ParthBhaleraoWork/huggingface/diffusers'
    
    model_id = "Freepik/flux.1-lite-8B-alpha"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    pipe = FluxPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float16,
        cache_dir=os.environ['HF_HOME'],
        local_files_only=True
    ).to(device)
    
    pipe.enable_attention_slicing(1)
    return pipe, device

def parse_prompts(file_path):
    """Parse prompts from text file"""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Split by numbered prompts and clean them
    prompts_dict = {}
    # Using regex to find numbered prompts
    pattern = r'(\d+):\s*((?:(?!\n\d+:).)*)'
    matches = re.finditer(pattern, content, re.DOTALL)
    
    for match in matches:
        number = match.group(1)
        prompt = match.group(2).strip()
        prompts_dict[number] = prompt
    
    return prompts_dict

def generate_images(pipe, prompts_dict, output_dir, device):
    """Generate images for each prompt"""
    for number, prompt in prompts_dict.items():
        print(f"\nGenerating image for prompt {number}...")
        
        with torch.inference_mode():
            image = pipe(
                prompt=prompt,
                generator=torch.Generator(device="cpu").manual_seed(11),
                num_inference_steps=30,
                guidance_scale=4,
                height=768,
                width=768,
            ).images[0]
        
        # Save the image
        image_path = os.path.join(output_dir, f"{number}.png")
        image.save(image_path)
        print(f"Saved image {number}.png")

def create_zip(folder_path):
    """Create a zip file of the output folder"""
    zip_path = f"{folder_path}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)
    return zip_path

def main():
    # Get input file path
    input_file = "MultiLingual-SingleAgent_Prompts.txt"
    if not os.path.exists(input_file):
        print("Error: Input file not found!")
        return

    # Create output directory based on input filename
    output_dir = os.path.splitext(os.path.basename(input_file))[0]
    os.makedirs(output_dir, exist_ok=True)

    # Initial GPU status
    print_gpu_status("Before Model Loading")

    # Load model
    pipe, device = setup_model()
    
    # GPU status after model loading
    print_gpu_status("After Model Loading")

    # Parse prompts
    prompts = parse_prompts(input_file)
    
    # Copy input file to output directory
    shutil.copy2(input_file, os.path.join(output_dir, os.path.basename(input_file)))

    # Generate images
    generate_images(pipe, prompts, output_dir, device)

    # Create zip file
    zip_path = create_zip(output_dir)

    print("\nProcess completed successfully!")
    print(f"Output folder: {os.path.abspath(output_dir)}")
    print(f"Zip file created: {os.path.abspath(zip_path)}")

if __name__ == "__main__":
    main()