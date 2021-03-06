# Creating-and-Deploying-an-Image-Object-Detection-Web-Service-within-a-Containerised-Environment
Image Object Detection Web Service within a Containerised Environment. Here Yolo and OpenCV is used to process images and detect objects. This project has Five parts.
* Creating a web service: A RESTful API was developed that allows clients to upload images to the server. Flask was used to create web service. Yolo and OpenCV was used to detect objects. Server returned objects in JSON format. As this project was done in Necture cloud, the resouces were limited. So, I used yolov3-tiny. I downloaded yolov3-tiny from URL: https://pjreddie.com/media/files/yolov3-tiny.weights.
* Dockerfile: Docker images were created by Docker by using the instructions given in Dockerfile.
* Kubernetes Cluster: As Necture cloud only allows 2 VCPUs, I've used KIND(Kubernetes in Docker). Kind uses Docker to set up and initialise a Kube cluster. A VM is created that uses Nectar Ubuntu 18.04 with Docker as its boot image. Kind's quick start is available here : URL: https://kind.sigs.k8s.io/docs/user/quick-start.
* Kubernetes Service: Kubernetes Service and deployment configurations in YML file was created that will create and deploy required pods in the cluster.
* Experiment: At last the performance was measured by changing the number of pods and threads.

## Environment: Flask, Python 3.7.1, Ubuntu 18.04, Necture Cloud.
