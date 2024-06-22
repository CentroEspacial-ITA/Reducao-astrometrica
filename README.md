# Astrometric Reduction

Welcome to the Astrometric Reduction project, an initiative by the ITA Space Center. This project encompasses the entire process from practical satellite trajectory observation to computer vision and the corresponding calculations for determining the trajectories of photographed satellites.

## How to Use the Code

### Programar_Observacao.py

This script is straightforward to run. Common errors are typically related to missing Python modules or the version of Selenium being used.

**Output:** The script generates a `.zip` file containing an Excel spreadsheet (`observacoes.xlsx`) with the scheduled observations and photos of the estimated trajectory of each chosen satellite from Heavens Above. The `.zip` file is saved in the same directory as the script.

### astrometric_reduction.ipynb

This Jupyter notebook allows you to go step by step, understanding each process as it unfolds.

**Steps to Use:**
1. Change the path to your image file (or name your image as specified in the code).
2. Run each cell sequentially, following the development of the functions.

**Output:** After running all cells, you will have the desired coordinates (RA and Dec) for input into the `gauss_method.ipynb` notebook.

### gauss_method.ipynb

Once you have updated the input coordinates and observation times in the code, simply run it. At the end, you will obtain the orbital elements of the corresponding satellite's orbit.

---
Feel free to contribute, raise issues, or suggest improvements. Happy coding!
