package main

import (
	"fmt"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/ec2"
	"os"
)

func main() {
	sess, err := session.NewSession(&aws.Config{
		Region: aws.String("us-east-1"),
	})
	svc := ec2.New(sess)
	result, err := svc.DescribeInstances(nil)
	if err != nil {
		fmt.Println("something blew up")
	}
	//fmt.Println("EC2 Instances")
	for _, reservation := range result.Reservations {
		for _, instance := range reservation.Instances {
			//fmt.Println(*instance.InstanceId)
			for _, tag := range instance.Tags {
				if *tag.Key == "Name" {
					fmt.Println(*tag.Value,*instance.InstanceId,*instance.InstanceIp)
				}
			}
		}
	}
}

func exitErrorf(msg string, args ...interface{}) {
	fmt.Fprintf(os.Stderr, msg+"\n", args...)
	os.Exit(1)
}
