# yet-another-lb-app
This repo can be used to spin up 3 boxes, two of which run a python script that replies to http `GET` requests with the `hostname` of the host it's running on. They're load balanced by an `nginx` box, which exposes port `65080` on the host machine.

| Hostname | Role | IP            |
| -------- |:----:|:-------------:|
| lb       | lb   |192.168.50.253 |
| app-1    | app  |192.168.50.10  |
| app-2    | app  |192.168.50.11  |


# How it works
There's a `Vagrantfile` which configures the 3 boxes, creates an extra network interface for internal (within `vagrant`) use and provisions everything using `ansible`.
The "app" is a simple `python` script started by ansible in the background (the good old but hacky `nohup .. &`)
The `nginx` config is a template which gets the `upstreams` as variables.

# Create all the VMs

## Requirements
* [git](https://git-scm.com/downloads)
* [vagrant](https://www.vagrantup.com/downloads.html)
* [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
* curl *(optional, used for testing the round robin load balancing)*


## Clone the repo and run the app
Open a command promt and type the following:
```bash
$ git clone https://github.com/ciprianc/yet-another-lb-app.git
$ cd yet-another-lb-app
$ vagrant up
```

After it's finished you can run a `vagrant status` and see 3 new `VMs` created.
Note: you have to make sure you didn't have anything running on port `65080` before, otherwise vagrant will fail.


## Test
Running the command below in your shell will cause 10 requests to be fired to the load balancer. You should see the output switching between two values with every run.
```bash
$ for i in {1..10}; do curl http://localhost:65080/; echo ; done
```

You should see output similar to the one below:
```html
<html><body>Hi there, I'm served from app-1.</body></html>
<html><body>Hi there, I'm served from app-2.</body></html>
<html><body>Hi there, I'm served from app-1.</body></html>
<html><body>Hi there, I'm served from app-2.</body></html>
<html><body>Hi there, I'm served from app-1.</body></html>
<html><body>Hi there, I'm served from app-2.</body></html>
<html><body>Hi there, I'm served from app-1.</body></html>
<html><body>Hi there, I'm served from app-2.</body></html>
<html><body>Hi there, I'm served from app-1.</body></html>
<html><body>Hi there, I'm served from app-2.</body></html>
```

## Cleanup
In order to remove all the `VMs` just run the following in the repo's top level:
```bash
$ vagrant destroy
```

*Note: you'll have confirm the destruction by pressing `y`*
