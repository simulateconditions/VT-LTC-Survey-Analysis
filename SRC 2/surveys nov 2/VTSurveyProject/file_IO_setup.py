import os


def setup_file_system():
    location = os.listdir()
    if 'Survey Statements' not in location: 
        os.mkdir('Survey Statements')
        os.mkdir(os.path.join('Survey Statements','ALR'))
        os.mkdir(os.path.join('Survey Statements','RCH'))
        os.mkdir(os.path.join('Survey Statements','SNF'))
        
        os.mkdir(os.path.join('Survey Statements','ALR','PageLinks'))
        os.mkdir(os.path.join('Survey Statements','RCH','PageLinks'))
        os.mkdir(os.path.join('Survey Statements','SNF','PageLinks'))
        
        os.mkdir(os.path.join('Survey Statements','ALR','PDF'))
        os.mkdir(os.path.join('Survey Statements','RCH','PDF'))
        os.mkdir(os.path.join('Survey Statements','SNF','PDF'))
        
        os.mkdir(os.path.join('Survey Statements','ALR','txt1'))
        os.mkdir(os.path.join('Survey Statements','RCH','txt1'))
        os.mkdir(os.path.join('Survey Statements','SNF','txt1'))

        os.mkdir(os.path.join('Survey Statements','ALR','txt2'))
        os.mkdir(os.path.join('Survey Statements','RCH','txt2'))
        os.mkdir(os.path.join('Survey Statements','SNF','txt2'))

        os.mkdir(os.path.join('Survey Statements','ALR','txt2','crop_images'))
        os.mkdir(os.path.join('Survey Statements','RCH','txt2','crop_images'))
        os.mkdir(os.path.join('Survey Statements','SNF','txt2','crop_images'))

        os.mkdir(os.path.join('Survey Statements','ALR','txt3'))
        os.mkdir(os.path.join('Survey Statements','RCH','txt3'))
        os.mkdir(os.path.join('Survey Statements','SNF','txt3'))



