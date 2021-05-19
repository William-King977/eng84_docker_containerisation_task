# Docker Containerisation Task
1. Build a Docker image of your Python plane project with a Dockerfile
2. Create a webhook on Docker Hub to send a notification to Shahrukh's email and yourself once the new image is pushed to your Docker Hub
3. Push it to Docker Hub
4. Share your Docker Hub image name and *this* repository
5. Create a video for this task with a demo

## Containerising the Plane Project
It's highly recommended to do all the containerisation steps manually first, to ensure that it's actually working. If you run into any problems with running the Python image or Plane Project, see **Additional Notes**.

### Step 1: Modify the Dockerfile
* In this task, we'll containerise a [Python Plane Project](https://github.com/conjectures/eng84-airport-project)
* Clone the Plane Project repository
* Create a `Dockerfile` in the same directory with the following contents:
  ```
  # Using Python official image
  FROM python:3.7

  # Optional, but a good practice
  LABEL MAINTAINER = kingbigw

  # Copying the project from our OS to the specified location (in container) 
  COPY eng84-airport-project /usr/src/app

  # Expose required port for the plane project (Django runs on port 8000)
  EXPOSE 8000

  # Install the requirements
  WORKDIR /usr/src/app
  RUN python -m pip install -r requirements.txt

  # Make migrations, then run the application
  WORKDIR /usr/src/app/app
  RUN python manage.py makemigrations
  RUN python manage.py migrate
  CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
  ```

### Step 2: Run the Plane Project
* `docker build -t kingbigw/eng84_plane_project_django .` - build the image from the Dockerfile
* `docker run -d -p 977:8000 kingbigw/eng84_plane_project_django` - run the project. On your browser, go on `localhost:977` to see the application running.

### Step 3: Commit and Push your Image to Docker Hub
* `docker commit container_id kingbigw/eng84_plane_project_django` - changes it locally
* `docker push kingbigw/eng84_plane_project_django:version_tag` - push it to Docker Hub

### Step 4: Creating a Webhook with Google App Script
* On Google Drive, go on `New` > `More` > `Google Apps Script`
* Copy and paste the following code, and change where applicable:
  ```
  function doPost(request) {
    // Gets the string value of the POST data
    var postJSON = request.postData.getDataAsString();
    var payload = JSON.parse(postJSON);

    var tag = payload.push_data.tag; // image version
    var reponame = payload.repository.repo_name;
    var dockerimagename = payload.repository.name;

    if (typeof request !== 'undefined')
  
    // Send an email to me
    MailApp.sendEmail({
      to: "name@example-email.com",
      subject: reponame + " on DockerHub Has Been Updated",
      htmlBody: "Hi William,<br /><br />" +
                "The repository has been updated to version " + tag + ".<br /><br />" +
                "Thanks,<br />" +
                "William"
    })
  }
  ```
* Once you have finished, click `Deploy` and set the follow configurations:
  * Deploy as a `Web app`
  * Execute as yourself 
  * Allow access to `Anyone`
* Copy the Web app URL

### Step 5: Create a Docker Webhook
* Select the repository you want to attach the webhook to
* Select `Webhooks`
* Give it a suitable name
* Paste the Web app URL
* Now, commit and push to your Docker repository (no changes need to be made), then you'll receive an email

## Additional Notes
**To run a Python Image:**
* `alias docker="winpty docker"`
* `docker run -dit python`

**Execute these commands to run the project on the container's port:**
* `cd eng84-plane-project`
* `python -m pip install -r requirements.txt`
* `cd app`
* `python manage.py makemigrations`
* `python manage.py migrate`
* `python manage.py runserver 0.0.0.0:8000`

