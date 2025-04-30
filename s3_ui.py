import streamlit as st
import boto3
from botocore.exceptions import ClientError
import os

REGIONS = ['us-east-1', 'us-east-2', 'us-west-2', 'ap-south-1', 'ap-southeast-1']

# Select region
st.sidebar.title("AWS Region")
region = st.sidebar.selectbox("Choose a region", REGIONS)

# AWS Client
@st.cache_resource
def get_s3_client(region):
    return boto3.client('s3', region_name=region)

s3 = get_s3_client(region)

# Create Bucket
st.header("🪣 S3 Bucket Manager")

if st.button("List Buckets"):
    try:
        buckets = s3.list_buckets().get("Buckets", [])
        if not buckets:
            st.info("No buckets found.")
        else:
            for bucket in buckets:
                st.success(f"{bucket['Name']} (Created: {bucket['CreationDate']})")
    except ClientError as e:
        st.error(e)

st.subheader("Create a Bucket")
bucket_name = st.text_input("Bucket Name")

if st.button("Create Bucket"):
    try:
        if region == 'us-east-1':
            s3.create_bucket(Bucket=bucket_name)
        else:
            s3.create_bucket(Bucket=bucket_name,
                             CreateBucketConfiguration={'LocationConstraint': region})
        st.success(f"Bucket {bucket_name} created.")
    except ClientError as e:
        st.error(e)

st.subheader("Bucket Details")
bucket_detail_name = st.text_input("Enter bucket name for details")

if st.button("Get Bucket Details"):
    try:
        location = s3.get_bucket_location(Bucket=bucket_detail_name)
        versioning = s3.get_bucket_versioning(Bucket=bucket_detail_name).get('Status', 'Not Enabled')
        st.write(f"📍 Region: {location.get('LocationConstraint') or 'us-east-1'}")
        st.write(f"🔁 Versioning: {versioning}")

        st.write("📄 Objects in Bucket:")
        objects = s3.list_objects_v2(Bucket=bucket_detail_name)
        if 'Contents' in objects:
            for obj in objects['Contents']:
                st.markdown(f"- {obj['Key']}")
        else:
            st.info("No objects in bucket.")
    except ClientError as e:
        st.error(e)

# Enable versioning
if st.button("Enable Versioning"):
    try:
        s3.put_bucket_versioning(
            Bucket=bucket_detail_name,
            VersioningConfiguration={'Status': 'Enabled'}
        )
        st.success("Versioning enabled.")
    except ClientError as e:
        st.error(e)

# Upload file
st.subheader("Upload a File")
upload_bucket = st.text_input("Bucket name to upload to")
uploaded_file = st.file_uploader("Choose a file")

if uploaded_file and st.button("Upload File"):
    try:
        s3.upload_fileobj(uploaded_file, upload_bucket, uploaded_file.name)
        st.success(f"{uploaded_file.name} uploaded to {upload_bucket}")
    except ClientError as e:
        st.error(e)

# Delete bucket
st.subheader("Delete Bucket")
delete_bucket = st.text_input("Bucket name to delete")

if st.button("Delete Bucket"):
    try:
        # Delete objects first
        objs = s3.list_objects_v2(Bucket=delete_bucket)
        if 'Contents' in objs:
            for obj in objs['Contents']:
                s3.delete_object(Bucket=delete_bucket, Key=obj['Key'])

        s3.delete_bucket(Bucket=delete_bucket)
        st.success(f"Bucket {delete_bucket} deleted.")
    except ClientError as e:
        st.error(e)
