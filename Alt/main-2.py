import torch
from diffusers import DiffusionPipeline
import os
import pickle
import gc
import time

def print_gpu_status(message="Current GPU Status"):
    print(f"\n=== {message} ===")
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"Total GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**2:.2f} MB")
    print(f"Allocated GPU Memory: {torch.cuda.memory_allocated() / 1024**2:.2f} MB")
    print(f"Cached GPU Memory: {torch.cuda.memory_reserved() / 1024**2:.2f} MB")
    print(f"Free GPU Memory: {(torch.cuda.get_device_properties(0).total_memory - torch.cuda.memory_allocated()) / 1024**2:.2f} MB")
    print("=" * 50)

def clear_gpu_memory():
    print("\nClearing GPU memory...")
    
    # Clear PyTorch GPU memory
    torch.cuda.empty_cache()
    
    # Force garbage collection
    gc.collect()
    
    # Reset the GPU device
    if torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats(0)
        torch.cuda.empty_cache()
    
    # Sleep for a moment to ensure cleanup
    time.sleep(2)
    
    print("GPU memory cleared!")

def load_model():
    # Define paths
    MODEL_PATH = "/WAVE/scratch2/oignat_lab/ParthBhaleraoWork/altdiffusion_model"
    PIPE_PATH = "/WAVE/scratch2/oignat_lab/ParthBhaleraoWork/pipe.pkl"
    
    # Check if CUDA is available
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is not available!")
    
    # Print initial GPU status
    print_gpu_status("Initial GPU Status")
    
    # Clear GPU memory
    clear_gpu_memory()
    
    # Print GPU status after clearing
    print_gpu_status("GPU Status After Clearing Memory")
    
    # Check if model exists
    if not os.path.exists(MODEL_PATH):
        raise RuntimeError(f"Model not found at {MODEL_PATH}. Please run model download first.")
    
    print(f"\nLoading model from {MODEL_PATH}")
    
    # Load the model
    pipe = DiffusionPipeline.from_pretrained(
        MODEL_PATH,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    
    # Print GPU status after loading model
    print_gpu_status("GPU Status After Loading Model")
    
    # Enable memory efficient attention
    if hasattr(pipe, 'enable_memory_efficient_attention'):
        pipe.enable_memory_efficient_attention()
        print("\nEnabled memory efficient attention")
    
    # Save pipe to pickle file
    with open(PIPE_PATH, 'wb') as f:
        pickle.dump(pipe, f)
    
    print(f"\nPipe saved to: {PIPE_PATH}")
    
    # Final GPU status
    print_gpu_status("Final GPU Status")
    
    return pipe

if __name__ == "__main__":
    try:
        print("Starting main-2.py execution...")
        pipe = load_model()
        print("\nPart 2 completed successfully!")
    except Exception as e:
        print(f"\nError in Part 2: {e}")
        raise