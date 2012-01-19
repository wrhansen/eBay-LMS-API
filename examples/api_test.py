'''
Test custom LMS API
'''

__author__ = 'Wesley Hansen'
__date__ = '12/19/2011 03:18:13 PM'


import lmslib
import sys
import pprint
import time
import uuid

###############################
#Create a new upload job
# of addItem calls with
# gzip compression
###############################
uuid = uuid.uuid4()

environment = lmslib.SANDBOX #The server environment to connect to
print '*' * 50
print "Creating new UploadJob\n"


create_job = lmslib.CreateUploadJob( environment )
create_job.buildRequest( 'ReviseItem', 'gzip', uuid )
#can save response to file if desired
response = create_job.sendRequest()
response, resp_struct = create_job.getResponse()

jobId = None			#The jobId used throughout the process
fileReferenceId = None	#The fileId for the file to be uploaded
downloadFileId = None		#Eventually a new fileId will be made( for downloading )
filename = 'AddItem.xml'	#The uploaded File


if response == 'Success':
	jobId = resp_struct.get( 'jobId', None )
	fileReferenceId = resp_struct.get( 'fileReferenceId', None )
	if not jobId or not fileReferenceId:
		print "createUploadJob Error: couldn't obtain jobId or fileReferenceId"
		sys.exit()
	else:
		print "createUploadJob Success!"
		pprint.pprint( resp_struct )
elif response == 'Failure':
	pprint.pprint( resp_struct )
	print 'createUploadJob Error[%s]: %s' % (resp_struct.get('errorId',None), resp_struct.get('message', None) )
	#sys.exit()
else:
	print "createUploadJob Error: Something really went wrong here"
	sys.exit()

print '*' * 50
print '\n'

time.sleep( 10 )#I've gotten better results waiting a few seconds in between each call
#Sometimes the call doesn't register on the eBay server fast enough and it throws an error

###################################
#upload the file to eBay
###################################
print '*' * 50
print "Uploading File\n"
upload_job = lmslib.UploadFile( environment )
upload_job.buildRequest( jobId, fileReferenceId, filename )

response = upload_job.sendRequest()

response, response_struct = upload_job.getResponse()


if response == 'Failure':
	print 'uploadFile Error[%s]: %s' % ( response_struct.get('errorId',None), response_struct.get('message', None ) )
	pprint.pprint( response_struct )
	sys.exit()
elif response == 'Success':
	print "uploadFile Success!"
	pprint.pprint( response_struct )
	print '\n'
else:
	print "uploadFile Error: Something really went wrong here"
	sys.exit()
	
print '*' * 50
print '\n'

time.sleep( 10 )

#####################################
#Start processing the file
#####################################
print '*' * 50
print "Starting job processing\n"
start_job = lmslib.StartUploadJob( environment )
start_job.buildRequest( jobId )

response = start_job.sendRequest()
response, response_dict = start_job.getResponse()

if response == 'Success':
	print "startUploadJob Success!"
	pprint.pprint( response_struct )
	print '\n'
elif response == 'Failure':
	print 'startUploadJob Error[%s]: %s' % (response_struct.get('errorId', None), response_struct.get('message', None  ))
	pprint.pprint( response_struct )
	sys.exit()
else:
	print "startUploadJob Error: Something really went wrong here"
	sys.exit()

print '*' * 50
print '\n'

time.sleep( 10 )


######################################
#Get Job status
######################################
print '*' * 50
print "Checking Job Status\n"
job_status = lmslib.GetJobStatus( environment )
job_status.buildRequest( jobId )


#Keep checking on status until completed
while True:
	response = job_status.sendRequest()
	response, resp_struct = job_status.getResponse()
	if response == 'Success':
		if resp_struct[0].get('jobStatus',None) == 'Completed':
			print "Job Finished! Woo hoo!"
			print resp_struct[0]
			print '\n'
			downloadFileId = resp_struct[0].get( 'fileReferenceId', None )
			break
		else:
			print "Job is %s complete, trying again in 10 seconds" % resp_struct[0].get('percentComplete', None )
			print resp_struct
			print '\n'
	#Check again in 10 seconds
	time.sleep( 10 )
	
			
print '*' * 50
print '\n'

###########################################
#downloadFile --The responses
###########################################
print '*' * 50
print "Downloading Responses\n"


download_file = lmslib.DownloadFile( environment )
download_file.buildRequest( jobId, downloadFileId )

response = download_file.sendRequest()

response, resp_struc = 	download_file.getResponse()

if response == 'Success':
	print "Successfully downloaded response!"
	print resp_struc
	print '\n'
elif response == "Failure":
	print "Failure! downloadFile failed"
	print resp_struc

print '*' * 50
	
sys.exit()





	

