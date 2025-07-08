from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import pandas as pd
import io


def authenticate(service_account_file):
	scopes = ["https://www.googleapis.com/auth/drive"]
	creds = service_account.Credentials.from_service_account_file(service_account_file, scopes=scopes)
	return creds

def upload_file(file_path, file_name, parent_folder_id=[]):
	creds = authenticate("baby-names.json")
	upload_service = build("drive", "v3", credentials=creds)
	
	## parent_folder_id = "1E1QDksgUQ39xvq_v9T2uohPlEvN9fP2D"
	file_metadata ={
		"name": file_name,
		"parents": [parent_folder_id]
	}
	
	file = upload_service.files().create(
			body=file_metadata,
			media_body=file_path
	).execute()
	
	## print("Upload is done 100%%")  ## For debugging

def update_file(file_path, file_id, file_name):
	creds = authenticate("baby-names.json")
	update_service = build("drive", "v3", credentials=creds)
	
	media_body = MediaFileUpload(file_path, resumable=True)
	updated_metadata = {'name': file_name}

	try:
		updated_file = update_service.files().update(
						fileId=file_id,
						body=updated_metadata,
						media_body=media_body
					   ).execute()
		## print("File Updated Successfully")  ## For debugging
	except Exception as e:
		print(f"An error occurred: {e}")
	
def download_file(file_path, file_id):
	creds = authenticate("baby-names.json")
	download_service = build("drive", "v3", credentials=creds)
	# file_id = parent_folder_id
	
	request = download_service.files().get_media(fileId=file_id)
	
	file = io.FileIO(file_path, "wb")  ## Download file in hard-disk
	downloader = MediaIoBaseDownload(file, request)
	done =False
	while not done:
		status, done = downloader.next_chunk()
		## print("Download {0}%%".format(int(status.progress()*100)))  ## For debugging
	
	data = pd.read_excel(file_path)
	return data