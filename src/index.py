def handler(event, context):
    print("Hello from Terraform Managed Lambda!")
    return {
        'statusCode': 200,
        'body': 'Success'
    }

def handler_two(event, context):
    print("Hello from Terraform Managed Lambda 2!")
    return {
        'statusCode': 200,
        'body': 'Success'
    }