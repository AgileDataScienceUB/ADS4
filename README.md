# ADS4

## Projecte dependencies:

* Docker
* Updated web browser

# Use instructions

* Build docker file
    * docker build . -t agile_course_election

* Run docker file
    * docker run -d -it -v $(pwd):/home agile_course_election

* Get inside docker file

    * docker exec -it $agile_course_election_docker_id bash

* Upload dataset
  
    * python s3upload.py <file_name> <BUCKET_NAME> 
