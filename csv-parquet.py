import boto3
import pandas as pd
import io

s3 = boto3.client('s3')
source_bucket = 'jrbonnke-bl'               #from where to take the file 
source_key = 'tips.csv'                     #file name
destination_bucket = 'jrbonnke'             #destination bucket
destination_key = 'converted.parquet'       #storeage file name 


csv_obj = s3.get_object(Bucket=source_bucket, Key=source_key)       #getting the file from bucket
csv_content = csv_obj['Body'].read().decode('utf-8')               #get raw byte data and convert byte to string
df = pd.read_csv(io.StringIO(csv_content))                          #convert to string into panda's project


parquet_buffer = io.BytesIO()                                      #creating the buffer for storing and process the data to convert
df.to_parquet(parquet_buffer, engine='pyarrow', index=False)       #Convert the DataFrame to a Parquet file inside the buffer


s3.put_object(Bucket=destination_bucket, Key=destination_key, Body=parquet_buffer.getvalue()) #upload the file

print("CSV converted to Parquet and uploaded successfully.")
