# Accessing the AWS EC2 Instance with SSH

Download the `AMODStudents.pem` file

NOTE: __do not share this `.pem` file, it is a private key file and having it compromised would be very bad__

## For Linux/macOS:

In a terminal:

```
ssh -i /path/to/AMODStudent.pem student@ec2-13-58-90-43.us-east-2.compute.amazonaws.com
```

Then, you can query mongo by typing the following into the terminal:
```
> mongo
> use twitter
> db.tweet.stats()
```

To exit the mongo console, type `exit`

When you're done with ssh, type `exit`


## For Windows:

You can refer to the guide here: [https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/putty.html](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/putty.html) or follow the steps below.

- Download [Putty](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html)
- Convert the `AMODStudent.pem` file to `.ppk` format by:
  - Launching PuTTYgen (All Programs -> PuTTY -> PuTTYgen)
  - Select _RSA_ under __Type of key to generate__
  - Load the `AMODStudent.pem` file (be sure to select _All Files_ for this)
  - Choose __Save private key__ (you don't need to add a password)
  - Save the file as `AMODStudent.ppk`
- Start a PuTTY session:
  - Enter `student@ec2-13-58-90-43.us-east-2.compute.amazonaws.com` into __Host Name__
  - Enter `22` into __Port__
  - Make sure __SSH__ is selected as the _Connection Type_
  - In the side pane, select: __Connection -> SSH -> Auth__
  - Select your `AMODStudent.ppk` with the __Browse__ button
  - You're ready, click the __Open__ button and await connection to the EC2 instance

Then, you can query mongo by typing the following into the terminal:
```
> mongo
> use twitter
> db.tweet.stats()
```

To exit the mongo console, type `exit`

When you're done with ssh, type `exit`
