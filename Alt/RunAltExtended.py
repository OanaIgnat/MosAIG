# import os
# import pandas as pd
# import main3  # Your image generation module
# import main2  # Adding main2 for model loading
# import importlib
# from pathlib import Path
# import zipfile
# import logging

# # Set up logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler('image_generation.log'),
#         logging.StreamHandler()
#     ]
# )

# class ImageGenerator:
#     def __init__(self, excel_path, output_dir="output_images"):
#         """
#         Initialize the image generator with paths and parameters
        
#         Args:
#             excel_path (str): Path to the Excel file
#             output_dir (str): Directory to save generated images
#         """
#         self.excel_path = excel_path
#         self.output_dir = output_dir
#         self.params = {
#             "width": 768,
#             "height": 768,
#             "seed": 12000,
#             "guidance_scale": 9.5,
#             "num_inference_steps": 110
#         }
        
#         # Create output directory if it doesn't exist
#         os.makedirs(self.output_dir, exist_ok=True)
        
#         # Initialize the model once at startup
#         logging.info("Loading model into GPU memory...")
#         self.initialize_model()
        
#     def initialize_model(self):
#         """
#         Load the model into GPU memory once at initialization
#         """
#         try:
#             # Initialize main2 module and load model
#             main2 = importlib.import_module("main2")
#             main2.load_model()
#             logging.info("Model loaded successfully")
#         except Exception as e:
#             logging.error(f"Error loading model: {str(e)}")
#             raise
        
#     def read_excel(self):
#         """
#         Read the Excel file and validate required columns
        
#         Returns:
#             pandas.DataFrame: DataFrame containing prompts and image names
#         """
#         try:
#             df = pd.read_excel(self.excel_path)
            
#             # Validate required columns
#             required_columns = ['Prompt', 'Image name']
#             if not all(col in df.columns for col in required_columns):
#                 missing = [col for col in required_columns if col not in df.columns]
#                 raise ValueError(f"Missing required columns: {missing}")
            
#             # Remove rows with missing values
#             df_clean = df.dropna(subset=required_columns)
            
#             if df_clean.empty:
#                 raise ValueError("No valid data found after removing rows with missing values")
                
#             return df_clean
            
#         except Exception as e:
#             logging.error(f"Error reading Excel file: {str(e)}")
#             raise
    
#     def generate_single_image(self, prompt, filename):
#         """
#         Generate a single image using the provided prompt and filename
        
#         Args:
#             prompt (str): Text prompt for image generation
#             filename (str): Output filename for the image
#         """
#         try:
#             # Clean filename to be safe for filesystem
#             clean_filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_')).rstrip()
            
#             main3.generate_single_image(
#                 prompt=prompt,
#                 seed=self.params["seed"],
#                 width=self.params["width"],
#                 height=self.params["height"],
#                 num_inference_steps=self.params["num_inference_steps"],
#                 guidance_scale=self.params["guidance_scale"],
#                 output_dir=self.output_dir,
#                 filename=clean_filename
#             )
#             logging.info(f"Successfully generated image: {clean_filename}")
            
#         except Exception as e:
#             logging.error(f"Error generating image for prompt '{prompt}': {str(e)}")
#             raise
    
#     def create_zip(self):
#         """
#         Create a ZIP file of all generated images
#         """
#         try:
#             zip_path = os.path.join(os.path.dirname(self.output_dir), 'generated_images.zip')
#             with zipfile.ZipFile(zip_path, 'w') as zipf:
#                 for file in os.listdir(self.output_dir):
#                     file_path = os.path.join(self.output_dir, file)
#                     zipf.write(file_path, os.path.basename(file_path))
#             logging.info(f"Created ZIP file at: {zip_path}")
            
#         except Exception as e:
#             logging.error(f"Error creating ZIP file: {str(e)}")
#             raise

#     def process_all_images(self):
#         """
#         Process all rows in the Excel file and generate images
#         """
#         try:
#             df = self.read_excel()
#             total_rows = len(df)
            
#             logging.info(f"Starting batch processing of {total_rows} images")
            
#             for index, row in df.iterrows():
#                 try:
#                     logging.info(f"Processing {index + 1}/{total_rows}: {row['Image name']}")
#                     self.generate_single_image(row['Prompt'], row['Image name'])
#                 except Exception as e:
#                     logging.error(f"Error processing row {index + 1}: {str(e)}")
#                     continue
            
#             self.create_zip()
#             logging.info("Batch processing completed")
            
#         except Exception as e:
#             logging.error(f"Error in batch processing: {str(e)}")
#             raise

# def main():
#     """
#     Main function to run the image generation process
#     """
#     try:
#         # Configuration
#         excel_path = "Alt-Multi-V1-Prompts.xlsx"  # Change this to your Excel file path
#         output_dir = "output_images"
        
#         # Initialize and run
#         generator = ImageGenerator(excel_path, output_dir)
#         generator.process_all_images()
        
#     except Exception as e:
#         logging.error(f"Main process error: {str(e)}")
#         raise

# if __name__ == "__main__":
#     main()


import os
import pandas as pd
import main3
import main2
import importlib
from pathlib import Path
import zipfile
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('image_generation.log'),
        logging.StreamHandler()
    ]
)

class ImageGenerator:
    def __init__(self, excel_path, output_dir="output_images", start_number=None):
        """
        Initialize the image generator with paths and parameters
        
        Args:
            excel_path (str): Path to the Excel file
            output_dir (str): Directory to save generated images
            start_number (int): Entry number to start processing from
        """
        self.excel_path = excel_path
        self.output_dir = output_dir
        self.start_number = start_number
        self.params = {
            "width": 768,
            "height": 768,
            "seed": 12000,
            "guidance_scale": 9.5,
            "num_inference_steps": 110
        }
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialize the model once at startup
        logging.info("Loading model into GPU memory...")
        self.initialize_model()
        
    def initialize_model(self):
        """
        Load the model into GPU memory once at initialization
        """
        try:
            # Initialize main2 module and load model
            main2 = importlib.import_module("main2")
            main2.load_model()
            logging.info("Model loaded successfully")
        except Exception as e:
            logging.error(f"Error loading model: {str(e)}")
            raise
        
    def read_excel(self):
        """
        Read the Excel file and validate required columns
        
        Returns:
            pandas.DataFrame: DataFrame containing prompts and image names
        """
        try:
            df = pd.read_excel(self.excel_path)
            
            # Validate required columns
            required_columns = ['Prompt', 'Image name']
            if not all(col in df.columns for col in required_columns):
                missing = [col for col in required_columns if col not in df.columns]
                raise ValueError(f"Missing required columns: {missing}")
            
            # Remove rows with missing values
            df_clean = df.dropna(subset=required_columns)
            
            if df_clean.empty:
                raise ValueError("No valid data found after removing rows with missing values")
            
            # If start_number is specified, filter rows
            if self.start_number is not None:
                # Filter rows where Image name contains the number equal to or greater than start_number
                df_clean = df_clean[df_clean['Image name'].str.extract('(\d+)', expand=False).astype(float) >= self.start_number]
                if df_clean.empty:
                    raise ValueError(f"No entries found with image number {self.start_number} or higher")
                
            return df_clean
            
        except Exception as e:
            logging.error(f"Error reading Excel file: {str(e)}")
            raise
    
    def generate_single_image(self, prompt, filename):
        """
        Generate a single image using the provided prompt and filename
        
        Args:
            prompt (str): Text prompt for image generation
            filename (str): Output filename for the image
        """
        try:
            # Clean filename to be safe for filesystem
            clean_filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_')).rstrip()
            
            main3.generate_single_image(
                prompt=prompt,
                seed=self.params["seed"],
                width=self.params["width"],
                height=self.params["height"],
                num_inference_steps=self.params["num_inference_steps"],
                guidance_scale=self.params["guidance_scale"],
                output_dir=self.output_dir,
                filename=clean_filename
            )
            logging.info(f"Successfully generated image: {clean_filename}")
            
        except Exception as e:
            logging.error(f"Error generating image for prompt '{prompt}': {str(e)}")
            raise
    
    def create_zip(self):
        """
        Create a ZIP file of all generated images
        """
        try:
            zip_path = os.path.join(os.path.dirname(self.output_dir), 'generated_images.zip')
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for file in os.listdir(self.output_dir):
                    file_path = os.path.join(self.output_dir, file)
                    zipf.write(file_path, os.path.basename(file_path))
            logging.info(f"Created ZIP file at: {zip_path}")
            
        except Exception as e:
            logging.error(f"Error creating ZIP file: {str(e)}")
            raise

    def process_all_images(self):
        """
        Process all rows in the Excel file and generate images
        """
        try:
            df = self.read_excel()
            total_rows = len(df)
            
            logging.info(f"Starting batch processing of {total_rows} images")
            
            for index, row in df.iterrows():
                try:
                    logging.info(f"Processing {index + 1}/{total_rows}: {row['Image name']}")
                    self.generate_single_image(row['Prompt'], row['Image name'])
                except Exception as e:
                    logging.error(f"Error processing row {index + 1}: {str(e)}")
                    continue
            
            self.create_zip()
            logging.info("Batch processing completed")
            
        except Exception as e:
            logging.error(f"Error in batch processing: {str(e)}")
            raise

def main():
    """
    Main function to run the image generation process
    """
    try:
        # Configuration
        excel_path = "Alt-Multi-V2-Prompts.xlsx"
        output_dir = "Alt_MV2_output_images"
        
        # Get starting entry number from user
        while True:
            try:
                user_input = input("\nEnter the entry number to start from (press Enter to start from beginning): ").strip()
                if user_input == "":
                    start_number = None
                    break
                start_number = int(user_input)
                if start_number < 0:
                    print("Please enter a positive number")
                    continue
                break
            except ValueError:
                print("Please enter a valid number")
        
        # Initialize and run
        generator = ImageGenerator(excel_path, output_dir, start_number)
        generator.process_all_images()
        
    except Exception as e:
        logging.error(f"Main process error: {str(e)}")
        raise

if __name__ == "__main__":
    main()