package main

import (
    "fmt"
    "github.com/aws/aws-sdk-go/aws"
    "github.com/aws/aws-sdk-go/aws/session"
    "github.com/aws/aws-sdk-go/service/ec2"
    "github.com/aws/aws-sdk-go/service/ec2instanceconnect"
    "os"
    "io/ioutil"
    "os/user"
	"os/exec"
	"log"
)

type Instance struct {
    N int
    Id string
    Name string
    Ip string
    Az string
}
func main() {
    sess, err := session.NewSession(&aws.Config{
        Region: aws.String("us-east-1"),
    })

    // key location is much better now

    usr, u_err := user.Current()
    if u_err != nil {
        fmt.Println(u_err)
    }

    var fullPath string
    fullPath = usr.HomeDir + "/.ssh/id_rsa.pub"
    data, err := ioutil.ReadFile(fullPath)
    if err != nil {
        fmt.Println("Error: ", err)
    }
    //fmt.Println(string(data))

    svc := ec2.New(sess)
    result, err := svc.DescribeInstances(nil)
    if err != nil {
        fmt.Println("something blew up")
    }

    fmt.Println("EC2 Instances")

    instances := []Instance{}

    var instanceId int = 0
    for _, reservation := range result.Reservations {
        for _, instance := range reservation.Instances {
            //fmt.Println(*instance.InstanceId)
            for _, tag := range instance.Tags {
                if *tag.Key == "Name" {
                    //fmt.Println(*tag.Value,*instance.InstanceId,*instance.InstanceIp)
                    fmt.Println(instanceId, "\t", *tag.Value, *instance.InstanceId, *instance.PrivateIpAddress)
                    instances = append(instances, Instance {
                        N: instanceId,
                        Id: *instance.InstanceId,
                        Name: *tag.Value,
                        Ip: *instance.PrivateIpAddress,
                        Az: *instance.Placement.AvailabilityZone,
                    })
                }
            }
            instanceId++
        }
    }
    var choice int
    fmt.Println(">> ")
    _, er := fmt.Scan(&choice)
    if er != nil {
        fmt.Println("something blew up")
    }
    //var shellCommand string
    //shellCommand = fmt.Sprintf("aws ec2-instance-connect send-ssh-public-key --instance-id %s --instance-os-user 'ec-user' --ssh-public-key %s --availability-zone %s", instances[choice].Id, keyLocation, instances[choice].Az) 
    //fmt.Println(shellCommand)

    serv := ec2instanceconnect.New(session.New())

    input := &ec2instanceconnect.SendSSHPublicKeyInput{
        AvailabilityZone: aws.String(instances[choice].Az),
        InstanceId: aws.String(instances[choice].Id),
        InstanceOSUser: aws.String("ec2_user"),
        SSHPublicKey: aws.String(string(data)),
    }
    res, erz := serv.SendSSHPublicKey(input)
    if erz != nil {
        fmt.Println(erz)
    } else {
		// SUCCESS
        fmt.Println(res)
		_ = res
		var sshTarget string
		sshTarget = "root@"+instances[choice].Ip
		fmt.Println(sshTarget)

		cmd := exec.Command("ssh", "-v", sshTarget)
		err := cmd.Run()
		log.Printf("command finished with error: %v", err)
    }
}

func exitErrorf(msg string, args ...interface{}) {
    fmt.Fprintf(os.Stderr, msg+"\n", args...)
    os.Exit(1)
}

