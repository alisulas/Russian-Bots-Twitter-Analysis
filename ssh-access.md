# Accessing our AWS EC2 Instance with SSH

Download the `AMODStudents.pem` file

NOTE: __do not share this `.pem` file, it is a private key file and having it compromised would be very bad__

In a terminal:

```
ssh -i /path/to/AMODStudent.pem student@ec2-13-58-90-43.us-east-2.compute.amazonaws.com
```

Then, enter `mongo` and `use twitter` to perform some queries such as: `db.tweet.stats()`
