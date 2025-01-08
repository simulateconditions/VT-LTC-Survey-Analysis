1. INSTALL CONDA - no automatic base shell. https://docs.anaconda.com/free/anaconda/install/linux/
2. ACTIVATE BASE (source /anaconda3/bin/activate) 
3. CREATE new ENV (conda create -n gkloud_env python=3.9)
4. ACTIVATE new ENV (conda activate gkloud_env)
5. Install gcloud (conda install -c conda-forge google-cloud-sdk)
5.5. pip install requests==2.32.1
6. gcloud init
(7.) May need, gcloud auth application-default login, with your-email@gmail.com which I have provided with access to the project)
7. Create and enable service account using $ ./service_account_setup.sh (needs service account name and project name, not tested, and run $ chmod +x service_account_setup.sh before)
8. run python BBVT_secret.py to access the BBVT secret through google secret manager - a placeholder for the future GUI

out of dateS
