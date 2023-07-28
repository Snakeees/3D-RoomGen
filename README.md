# 3D-RoomGen
## Setup
To set up the 3D-RoomGen project, follow these steps:

1. Clone the repository:
```bash
git clone https://github.com/Snakees/3D-RoomGen.git
```
2. Navigate to the project directory:
```bash
cd 3D-RoomGen
```
3. Install the required dependencies using Miniconda and pip:
```bash
conda env create -f environment.yml
conda activate 3D-RoomGen
```
4. Download the 3D-FUTURE model dataset from https://tianchi.aliyun.com/dataset/98063

5. Create another folder containing just the images of the models:
```python
models_dir = "Your Models Dir"
model_images_dir = "Your Model Images Dir"
for i, model in enumerate(model for model in os.listdir(models_dir) if os.path.isdir(model)):
    input_image_path = os.path.join(models_dir,model+"/image.jpg")
    output_image_path = os.path.join(model_images_dir, model+".jpg")
    shutil.copy(input_image_path,output_image_path)
    print(i+1)
```
7. Edit the constants.py file: Add models dir, model images dir and your OpenAI api key

8. Run Either the main file or the main-random file:
```bash
python main.py
```
OR
```bash
python main-random.py
```
