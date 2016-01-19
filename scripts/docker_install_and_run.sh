#!/bin/bash
sudo apt-get update
sudo apt-get install -y docker.io
sudo docker pull javiergarridomellado/dai:dai
sudo docker run -t -i javiergarridomellado/dai:dai /bin/bash
