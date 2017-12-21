import os
import pickle

# This function should upload the given file to S3, saving it
# with the given filename
# In this case the function is simply saving the file locally
def upload_file(file, filename):
    file.save(filename)

# This function should upload the given object to S3, saving it
# with the given objectname
# In this case the function is simply saving the object locally
def upload_object(object, objectname):
    file = open(objectname, 'w')
    pickle.dump(object, file)

# This function should download an object with the given objectname
# from S3 and return it
# In this case, the function is simply reading the object from
# the filesystem, where it's saved
def download_object(objectname):
    file = open(objectname, 'r')
    return pickle.load(file)

# This function should check whether an object with the given
# objectname exists or not.
# In this case, the function simply checks whether the file exists
# in the filesystem
def object_exists(objectname):
    return os.path.isfile(objectname)
