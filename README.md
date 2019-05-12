# EDecor
Important folders.
The virtual environment folder is named as project<br>
The Django Project site is first_site<br>
The main index.html is in myapp folder named votings <br>
For this website, folders containing js and css have been kept in the static folder in votings and other app folders, which is user for bootstrap.

### Installing python3 <br>
sudo apt-get update <br>
sudo apt-get upgrade python3 <br>

### Making python3 default  <br>
python --version <br>
sudo su <br>
update-alternatives --install /usr/bin/python python /usr/bin/python3 1 <br>
python --version <br>

### Get virtual env with python 3.6 <br>
virtualenv project -p python #when python has been set to python3.6 <br>
virtualenv project -p python3 <br>

### Get virtualenvWrapper too <br>

### Tensorflow related installtions and other <br>
workon project  <br>
pip install numpy pandas sklearn keras tensorflow matplotlib Pillow  <br>
sudo apt-get install python3-tk  <br>
pip install Django <br>
Download object detection from https://github.com/tensorflow/models/tree/master/research<br>
Copy paste object Detection package to site-packages in virtualenv <br>
Keep FrontEnd/codes/SSD... in same directory as first_site  <br>

### Installing opencv
sudo apt-get install python-opencv <br>
### If above does not work then --------->>
git clone https://github.com/opencv/opencv.git

### Necessary django installations <br>
pip install --upgrade django-crispy-forms <br>
pip install mysqlclient <br>

### Setup django as user in mysql with django as password. 

### Setup anaconda
sha256sum Anaconda3-2018.12-Linux-x86_64.sh //download the latest .sh file <br>
bash <output of previous command> <br>

conda install -c conda-forge opencv <br>//done with all environments deactivated<br>
conda config --set auto_activate_base false<br> //set default base to false<br>

### May be useful later
tensorboard<br>
tensorboard-1.13.1.dist-info<br>
tensorflow<br>
tensorflow-1.13.1.dist-info<br>
tensorflow_estimator<br>
tensorflow_estimator-1.13.0.dist-info<br>
