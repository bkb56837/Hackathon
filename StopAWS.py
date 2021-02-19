import boto3
import time


def stop_model(model_arn):
    client = boto3.client('rekognition')

    print('Stopping model:' + model_arn)

    # Stop the model
    try:
        response = client.stop_project_version(ProjectVersionArn=model_arn)
        status = response['Status']
        print('Status: ' + status)
    except Exception as e:
        print(e)

    print('Done...')


def main():
    model_arn = 'arn:aws:rekognition:us-east-1:403295037370:project/PTC-Hackathon/version/PTC-Hackathon.2021-02-13T14.18.02/1613243883102'
    stop_model(model_arn)


if __name__ == "__main__":
    main()