# Docker Containerisation Task
1. Build a Docker image of your Python plane project with a Dockerfile
2. Create a Webhook on Docker Hub to send a notification to Shahrukh's email and yourself once the new image is pushed to your Docker Hub
3. Push it to Docker Hub
4. Share your Docker Hub image name and *this* repository
5. Create a video for this task with a demo

## Containerising the Plane Project
It's highly recommended to do all the containerisation steps manually first, to ensure it's actually working.

### Modify the Dockerfile
* In this task, we'll containerise a Python Plane Project and the original repository can be [found here](https://github.com/conjectures/eng84-airport-project)
* Clone the Plane Project repository
* Create a `Dockerfile` in the same directory with the following contents:
  ```
  # Using Django official image
  FROM python

  # Optional, but a good practice
  LABEL MAINTAINER = kingbigw

  # Copying the project from our OS to the specified location (in container) 
  COPY eng84-airport-project /usr/src/app

  # Expose required port for the base image
  EXPOSE 8000

  # Install the requirements
  WORKDIR /usr/src/app
  RUN python -m pip install -r requirements.txt
  WORKDIR /usr/src/app/app

  # Make migrations, then run the application (Django runs on port 8000)
  RUN python manage.py makemigrations
  RUN python manage.py migrate
  CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### Run the Plane Project
* `docker build -t kingbigw/eng84_plane_project_django .` - build the image from the Dockerfile
* `docker run -d -p 977:8000 kingbigw/eng84_plane_project_django` - run the project. Go on `localhost:977`, on your browser.

### Making q Webhook with Google App Script
* On Google Drive, go on `New` > `More` > `Google Apps Script`
* Copy and paste the following code:
  ```
  function doPost(request) {
    // get string value of POST data
    var postJSON = request.postData.getDataAsString();
    var payload = JSON.parse(postJSON);
    var tag = payload.push_data.tag; // docker version
    var reponame = payload.repository.repo_name;
    var dockerimagename = payload.repository.name;

    if (typeof request !== 'undefined')
  
    // Send an email to me
    MailApp.sendEmail({
      to: "name@example-email.com",
      subject: reponame + " on DockerHub has been updated",
      htmlBody: "Hi William,<br /><br />"+
                "The repository has been updated version " + tag + ".<br /><br />" +
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

### On Docker Webhooks
* Give it a suitable name
* Paste the Web app URL
* Now, commit and push to your repository (no changes need to be made), then you'll recieve an email

## Additional Notes
### Run Python Image
* `alias docker="winpty docker"`
* `docker run -dit python`

