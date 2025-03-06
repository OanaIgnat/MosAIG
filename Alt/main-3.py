import torch
import os
import time
import pickle

# Define the constant negative prompt
NEGATIVE_PROMPT = "deformed face, blurry, bad anatomy, disfigured, poorly drawn face, mutation, mutated, extra limb, ugly, poorly drawn hands, missing limb, floating limbs, disconnected limbs, malformed hands, blur, out of focus, long neck, distorted, body out of frame, bad composition, duplicate, multiple faces, animation, animated, blurry background"

def generate_single_image(
    prompt,
    seed,
    width,
    height,
    num_inference_steps,
    guidance_scale,
    output_dir,
    filename="temp"
):
    """
    Generate a single image based on the provided parameters.
    All parameters come from the web interface.
    """
    # Load pipe from pickle
    PIPE_PATH = "/WAVE/scratch2/oignat_lab/ParthBhaleraoWork/pipe.pkl"
    if not os.path.exists(PIPE_PATH):
        raise RuntimeError(f"Pipe not found at {PIPE_PATH}. Please load the model first.")
    
    with open(PIPE_PATH, 'rb') as f:
        pipe = pickle.load(f)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Set up generator with seed
    generator = torch.Generator("cuda").manual_seed(seed)
    
    # Generate image with user parameters
    start_time = time.time()
    with torch.inference_mode():
        image = pipe(
            prompt=prompt,
            negative_prompt=NEGATIVE_PROMPT,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            generator=generator,
            width=width,
            height=height
        ).images[0]
    end_time = time.time()
    
    # Save image with provided filename
    output_path = os.path.join(output_dir, f"{filename}.png")
    image.save(output_path)
    
    print(f"Image generated in {end_time - start_time:.2f} seconds")
    print(f"Saved to: {output_path}")
    
    return output_path

if __name__ == "__main__":
    # This section is just for testing
    test_params = {
        "prompt": "Test prompt",
        "seed": 1337,
        "width": 512,
        "height": 512,
        "num_inference_steps": 50,
        "guidance_scale": 7.5,
        "output_dir": "test_output",
        "filename": "test"
    }
    
    try:
        output_path = generate_single_image(**test_params)
        print(f"Test successful: {output_path}")
    except Exception as e:
        print(f"Test failed: {e}")