import boto3


def start_model(project_arn, model_arn, version_name, min_inference_units):
    client = boto3.client('rekognition')

    try:
        # Start the model
        print('Starting model: ' + model_arn)
        response = client.start_project_version(ProjectVersionArn=model_arn, MinInferenceUnits=min_inference_units)
        # Wait for the model to be in the running state
        project_version_running_waiter = client.get_waiter('project_version_running')
        project_version_running_waiter.wait(ProjectArn=project_arn, VersionNames=[version_name])

        # Get the running status
        describe_response = client.describe_project_versions(ProjectArn=project_arn,
                                                             VersionNames=[version_name])
        for model in describe_response['ProjectVersionDescriptions']:
            print("Status: " + model['Status'])
            print("Message: " + model['StatusMessage'])
    except Exception as e:
        print(e)

    print('Done...')


def main():
    project_arn = 'arn:aws:rekognition:us-east-1:403295037370:project/PTC-Hackathon/1612838559436'
    model_arn = 'arn:aws:rekognition:us-east-1:403295037370:project/PTC-Hackathon/version/PTC-Hackathon.2021-02-13T14.18.02/1613243883102'
    min_inference_units = 1
    version_name = 'PTC-Hackathon.2021-02-13T14.18.02'
    start_model(project_arn, model_arn, version_name, min_inference_units)


if __name__ == "__main__":
    main()