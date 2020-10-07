import requests
import boto3
import xml.etree.ElementTree as ET


def get_cost_and_usage():
    ce_client = boto3.client("ce")
    pricing_client = boto3.client("pricing")

    response = ce_client.get_cost_and_usage(
        TimePeriod={"Start": "string", "End": "string"},
        Granularity="MONTHLY",
        Metrics=["UsageQuantity"],
        NextPageToken="string",
    )


def get_xml():
    res = requests.get(
        "https://ec2.amazonaws.com/?Action=DescribeInstances&MaxResults=10&AUTHPARAMS"
    )
    return res.text


def parse_xml(xml_response):
    ec2_instanceIds = []
    ec2_instanceTypes = []

    tree = ET.parse(xml_response)
    root = tree.getroot()

    for item in root.findall("./reservationSet/item/instancesSet/item"):
        for node in item.getiterator():
            if node.tag == "instanceId":
                ec2_instanceIds.append(node.text)
            elif node.tag == "instanceType":
                ec2_instanceTypes.append(node.text)

    return ec2_instanceIds, ec2_instanceTypes


def calculate(ec2_instanceIds, ec2_instanceTypes):
    for index, item in enumerate(ec2_instanceTypes):
        if item == "a1.medium":
            # get hours instance has been running for beforehand
            cost = 0.0255 * hours

        # etc


if __name__ == "__main__":
    xml_response = get_xml()
    ec2_instanceIds, ec2_instanceTypes = parse_xml(xml_response)
    calculate(ec2_instanceIds, ec2_instanceTypes)
