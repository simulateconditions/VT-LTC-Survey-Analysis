import os

documents = os.listdir('Documents')
if 'Survey Statements' not in documents: 
	os.mkdir(os.path.join('Documents','Survey Statements'))
	os.mkdir(os.path.join('Documents','Survey Statements','ALR'))
	os.mkdir(os.path.join('Documents','Survey Statements','RCH'))
	os.mkdir(os.path.join('Documents','Survey Statements','SNF'))

	os.mkdir(os.path.join('Documents','Survey Statements','ALR','PDF'))
	os.mkdir(os.path.join('Documents','Survey Statements','RCH','PDF'))
	os.mkdir(os.path.join('Documents','Survey Statements','SNF','PDF'))

	os.mkdir(os.path.join('Documents','Survey Statements','ALR','txt1'))
	os.mkdir(os.path.join('Documents','Survey Statements','RCH','txt1'))
	os.mkdir(os.path.join('Documents','Survey Statements','SNF','txt1'))

	os.mkdir(os.path.join('Documents','Survey Statements','ALR','txt2'))
	os.mkdir(os.path.join('Documents','Survey Statements','RCH','txt2'))
	os.mkdir(os.path.join('Documents','Survey Statements','SNF','txt2'))

	os.mkdir(os.path.join('Documents','Survey Statements','ALR','txt2','crop_images'))
	os.mkdir(os.path.join('Documents','Survey Statements','RCH','txt2','crop_images'))
	os.mkdir(os.path.join('Documents','Survey Statements','SNF','txt2','crop_images'))

	os.mkdir(os.path.join('Documents','Survey Statements','ALR','txt3'))
	os.mkdir(os.path.join('Documents','Survey Statements','RCH','txt3'))
	os.mkdir(os.path.join('Documents','Survey Statements','SNF','txt3'))



