import boto3

def get_user_input():
    print("=== EC2 Instance Configuration ===")
    ami_id = input("Enter AMI ID (e.g., ami-0abcdef1234567890): ").strip()
    instance_type = input("Enter Instance Type (e.g., t2.micro): ").strip()
    key_name = input("Enter Key Pair Name: ").strip()
    security_group_id = input("Enter Security Group ID (e.g., sg-0123456789abcdef): ").strip()
    subnet_id = input("Enter Subnet ID (optional, press Enter to skip): ").strip()
    return ami_id, instance_type, key_name, security_group_id, subnet_id or None

def launch_ec2_instance(ami_id, instance_type, key_name, security_group_id, subnet_id=None):
    ec2 = boto3.resource('ec2')

    print("\nLaunching EC2 instance...")
    instance_params = {
        'ImageId': ami_id,
        'InstanceType': instance_type,
        'KeyName': key_name,
        'SecurityGroupIds': [security_group_id],
        'MinCount': 1,
        'MaxCount': 1
    }

    if subnet_id:
        instance_params['SubnetId'] = subnet_id

    instances = ec2.create_instances(**instance_params)
    instance = instances[0]

    print(f"Waiting for instance {instance.id} to be running...")
    instance.wait_until_running()
    instance.reload()
    print(f"\n✅ EC2 Instance launched successfully!")
    print(f"Instance ID: {instance.id}")
    print(f"Public DNS: {instance.public_dns_name}")
    print(f"State: {instance.state['Name']}")

if __name__ == "__main__":
    ami_id, instance_type, key_name, security_group_id, subnet_id = get_user_input()
    launch_ec2_instance(ami_id, instance_type, key_name, security_group_id, subnet_id)
