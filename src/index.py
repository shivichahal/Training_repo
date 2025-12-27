def handler_one(event, context):
    print("Hello from Terraform Managed Lambda!")
    return {
        'statusCode': 200,
        'body': 'Success'
    }
