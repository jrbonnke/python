import boto3

# s3 = boto3.resource('s3')

# for bucket in s3.buckets.all():
#     print(bucket.name)

# with open('boto-file.txt','rb') as data:
#     s3.Bucket('testmynewbucket-jrbonnke').put_object(key='test-boto.txt' , body = data)

####################################


sqs = boto3.resource('sqs', region_name='us-east-1') # fetching the resource of aws sqs


#creating a new queue
queue = sqs.create_queue(
    QueueName='test',
    Attributes={'DelaySeconds': '5'}
)

print(queue.url)
print(queue.attributes.get('DelaySeconds'))

#getting all queue detail
for queue_item in sqs.queues.all():
    print(queue_item)

#fetching the details of que test
queue_1 = sqs.get_queue_by_name(
    QueueName='test'
    )

# sending the message to the test queue
response = queue_1.send_message(
    MessageBody = 'new-world of python'
    )

#get  the message Id
print(response.get('MessageId'))
print(response.get('MD5OfMessageBody'))

