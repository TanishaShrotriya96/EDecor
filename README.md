# EDecor
FrontEnd contains frontend and edecorsite <br>
frontend is the virtual environment folder<br>
edecorsite is the Django Project<br>
edecor is the myapp folder <br>
For this website, index.html from /edecor/templates has been edited and folders containing js and css have been kept in the static folder in edecorsite.

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
sudo apt-get install python-opencv <br>
### If above does not work then --------->>
git clone https://github.com/opencv/opencv.git

Copy paste object Detection package to site-packages in virtualenv <br>
Keep FrontEnd/codes/SSD... in same directory as first_site  <br>

### Necessary django installations <br>
pip install --upgrade django-crispy-forms <br>
pip install mysqlclient <br>

### Setup django as user in mysql with django as password. 
python

### Setup anaconda
sha256sum Anaconda3-2018.12-Linux-x86_64.sh //download the latest .sh file 
bash <output of previous command>

### Installing opencv
conda install -c conda-forge opencv #done with all environments deactivated
conda config --set auto_activate_base false #set default base to false

### May be useful later
tensorboard
tensorboard-1.13.1.dist-info
tensorflow
tensorflow-1.13.1.dist-info
tensorflow_estimator
tensorflow_estimator-1.13.0.dist-info
