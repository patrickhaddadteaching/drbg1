## How to launch the exercise ?
* We can execute this exercise on [Colab](https://colab.research.google.com/github/patrickhaddadteaching/drbg1/blob/main/drbg1_binder.ipynb)
    * [Click here](https://colab.research.google.com/github/patrickhaddadteaching/drbg1/blob/main/drbg1_binder.ipynb)
    * Then press Ctrl+F9 or click on Runtime/Run All
* We can also execute this exercise on Binder
    * Click or scan the QR-code <a href="https://mybinder.org/v2/gh/patrickhaddadteaching/drbg1/main?urlpath=voila%2Frender%2Fdrbg1_binder.ipynb"><img src="qr-code-drbg1.png" style="width:100px;height:100px;"></a>
* The exercise is a jupyter notebook compatible with voila.
The following library is required:
    * numpy
  
## Examples of procedures to execute the exercise with different systems.
1. Windows
    * First of all, Let clone this repositorie
    ```
     git clone https://github.com/patrickhaddadteaching/drbg1
    ```
    * [Download and install the latest Miniconda](https://docs.conda.io/en/latest/miniconda.html#latest-miniconda-installer-links).
    * Open the Anaconda Powershell Prompt associated to Miniconda3 and type the following commands to install  to install all the dependencies required by this exercise.
     ```
        conda install jupyter
        conda install numpy
        conda install -c conda-forge voila    
    ```
    * Now, you can either launch the notebook by executing the folowing command in the directory where you cloned this repositorie.
    ```
    jupyter-notebook.exe .\drbg1_binder.ipynb
    
    ```
    
    * Or, you can directly launch it with voila  by executing the folowing command in the directory where you cloned this repositorie.
    ```
    voila.exe .\drbg1_binder.ipynb
    ```
2. Linux
3. Mac OS X
