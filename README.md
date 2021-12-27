# tf-external-data-source
Terraform external data source testing repo

Repository dedicated to a small test of the Terraform External Data Source. 

# Intro

The external data source allows an external program to be called from Terraform during state refresh implementing a specific protocol (JSON communication + an error exit in the case of no-success)


# TF Code

Simple code to test our external data source : 

```Terraform
# External data source example
#
variable "animal" {
  # NO DEFAULT value on purpose, for the demo
}

data "external" "animal-getter" {
  program = ["python", "${path.module}/cat-extractor.py"]

  query = {
    # find all animals with the required tag
    tag = var.animal
  }
}

resource "null_resource" "animal-echo" {
  triggers = {
    always_run = timestamp()
  }
  provisioner "local-exec" {
    command = "echo ${data.external.animal-getter.result.name}"
  }
}
```

# External program (e.g. Data Source) code

Simple programm in Python3 that is using built-in data , but could be extended to rad that from some source, not avaible normally for Terraform.

This expect to read JSON from `STDIN` and produce a resulting response as valids JSON map to `STDOUT`.
In case of the fail - it should error and produce **one-line error**

As of now - JSON arrays in response are not supported ( 27/12/2021 )


```Python
#!/usr/bin/python3
# Animal extractor
import sys
import json

data = {}
data['animals'] = []
data['animals'].append({
    'tag':'cat',
    'name':'Tom'
    })
data['animals'].append({
    'tag':'dog',
    'name':'Pluto'
    })
data['animals'].append({
    'tag':'vermin',
    'name':'Jeez'
    })


result={}

try:
    arguments = json.load(sys.stdin)
except:
    sys.exit('Error reading input arguments')

if 'tag' in arguments:
    try:
        result = json.dumps(next(filter(lambda animal: animal['tag']==arguments['tag'], data['animals'])))
    except:
        sys.exit('Tax extraction from data failed, perhaps there is no such tag : "'+arguments['tag']+'"')
    print(result)
else:
    sys.exit('Error, at least some "tag" of animal is expected like - cat, dog, vermin')
```

# Test runs

Let's get a "dog" from our data : 

```Terraform
terraform apply --auto-approve -var="animal=dog"
null_resource.animal-echo: Refreshing state... [id=1442566978067270438]

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated
with the following symbols:
-/+ destroy and then create replacement

Terraform will perform the following actions:

  # null_resource.animal-echo must be replaced
-/+ resource "null_resource" "animal-echo" {
      ~ id       = "1442566978067270438" -> (known after apply)
      + triggers = (known after apply) # forces replacement
    }

Plan: 1 to add, 0 to change, 1 to destroy.
null_resource.animal-echo: Destroying... [id=1442566978067270438]
null_resource.animal-echo: Destruction complete after 0s
null_resource.animal-echo: Creating...
null_resource.animal-echo: Provisioning with 'local-exec'...
null_resource.animal-echo (local-exec): Executing: ["/bin/sh" "-c" "echo Pluto"]
null_resource.animal-echo (local-exec): Pluto
null_resource.animal-echo: Creation complete after 0s [id=7049043146374803735]

Apply complete! Resources: 1 added, 0 changed, 1 destroyed.
```

Let's now try to get a "cat" from our data : 

```Terraform
terraform apply --auto-approve -var="animal=cat"
null_resource.animal-echo: Refreshing state... [id=7049043146374803735]

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated
with the following symbols:
-/+ destroy and then create replacement

Terraform will perform the following actions:

  # null_resource.animal-echo must be replaced
-/+ resource "null_resource" "animal-echo" {
      ~ id       = "7049043146374803735" -> (known after apply)
      ~ triggers = {
          - "always_run" = "2021-12-27T16:00:12Z"
        } -> (known after apply) # forces replacement
    }

Plan: 1 to add, 0 to change, 1 to destroy.
null_resource.animal-echo: Destroying... [id=7049043146374803735]
null_resource.animal-echo: Destruction complete after 0s
null_resource.animal-echo: Creating...
null_resource.animal-echo: Provisioning with 'local-exec'...
null_resource.animal-echo (local-exec): Executing: ["/bin/sh" "-c" "echo Tom"]
null_resource.animal-echo (local-exec): Tom
null_resource.animal-echo: Creation complete after 0s [id=2656677041203394027]

Apply complete! Resources: 1 added, 0 changed, 1 destroyed.
```

Seems to be valid, we goit in return cat Tom, rather traditional name for a feline character


How about if we requesat some gibberish ? What will error look like? 

```Terraform
terraform apply --auto-approve -var="animal=sd"
╷
│ Error: failed to execute "python": Tax extraction from data failed, perhaps there is no such tag : "sd"
│
│
│   with data.external.animal-getter,
│   on main.tf line 7, in data "external" "animal-getter":
│    7: data "external" "animal-getter" {
│
╵
```




# TODO

- [x] make basic code
- [x] test it
- [ ] update readme
