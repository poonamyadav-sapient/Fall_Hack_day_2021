# Fall_Hack_day_2021
 
 #**Installation steps:**
 
 Create a virtual environment by using command pipenv shell.
 Run the command `pipenv install` to install all the packages.
 
 **#Credentials require for accessing ereceipt html page:**
Create a creds.env file in the same directory and add the following credentials in it-
`username=` SSO username
`password=` SSO password
`ACCESS_KEY_ID=` AWS access key id
`SECRET_ACCESS_KEY=` ASW access secret key

**Follow step to use this repository:**

**Step:1** To create preprocess dataset run below command on terminal by adding the required arguments:
`python createDataset.py --banner_key={banner_name} --start_date={start_date} --limit={receipt_limit}`

**Step:2** To create and train the dataset run below command:
` python createNERdata.py `
 Note: mention the path for storing traindata in this script at line:db.to_disk("path to store train data or validation data")
 
 **Step:3** To create NER model run the below command:
 `python -m spacy init fill-config base_config.cfg config.cfg`
` python -m spacy train config.cfg --output ./output --paths.train ./data/training_data/train.spacy --paths.dev ./data/validation_data/train.spacy`
 
 **Step:4** To use the trained model run the below command:
 `python load_NERMODEL.py` 
 
