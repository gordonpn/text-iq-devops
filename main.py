# attempt at retrieving running ec2 instances and their launch times to calculate cost.
# tough without having data to work with. (untested)
import datetime
import boto3
import awspricing


def get_running_instances():
    ec2 = boto3.resource("ec2")
    # only looking for running instances
    instances = ec2.instances.filter(
        Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
    )

    instance_dict = {}

    for instance in instances:
        launch_time_datetime = datetime.datetime.strptime(
            instance.launch_time, "%Y-%m-%dT%H:%M:%S"
        )
        # getting a datetime object of the difference of time between now and launch time
        instance_dict[instance.id] = {
            "type": instance.instance_type,
            "launch_time_delta": datetime.datetime.utcnow() - launch_time_datetime,
        }

    return instance_dict


def get_cost(instance_dict):
    pricing_dict = {}
    ec2_offer = awspricing.offer("AmazonEC2")

    for instance in instance_dict:
        instance_type = instance_dict[instance]["type"]

        # assuming that all ec2 instances are running linux and are located in the west of the US
        pricing_dict[instance_type] = ec2_offer.ondemand_hourly(
            instance_type, operating_system="Linux", region="us-west-1"
        )

    return pricing_dict


def calculate_total_cost(instance_dict, pricing_dict):
    # creating a new dictionary because modifying a dictionary while iterating it might not be good idea
    total_cost = {}

    for instance in instance_dict:
        instance_type = instance_dict[instance]["type"]
        # add 1 hour because if the hour has already started, then aws should charge for it
        hours = instance_dict[instance]["launch_time_delta"].hour + 1
        cost = hours * pricing_dict[instance_type]
        total_cost[instance] = {"type": instance_type, "cost": cost}

    return total_cost


if __name__ == "__main__":
    running_instances = get_running_instances()
    prices = get_cost(running_instances)
    print(calculate_total_cost(running_instances, prices))
