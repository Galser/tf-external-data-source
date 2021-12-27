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

