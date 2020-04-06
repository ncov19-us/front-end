### <img src="assets/images/covid19-logo.png" width="45px" height="45px">[COVID-19 US Dashboard](https://ncov19.us/)

# Project Overview

### 1️⃣ About this app
Visualizing COVID19 pandemic in the U.S. by states and by the whole country, with newsfeeds from major news channels and twitter feeds from public officials and institutions. The app can be [found here](https://ncov19.us/).

---

### 2️⃣ Key Features

- drive-thru testing center locations
- testing counts
- confirmed cases
- fatality counts 
- twitter feeds
- news feeds

---

### 3️⃣ Data Sources

- For US and International: [Johns Hopkins CSSE](https://github.com/CSSEGISandData/COVID-19)
- For US States: [New York Times](https://github.com/nytimes/covid-19-data)
- For County comes from State & Local Govs. County Sites
- For Tested Data: [COVIDTRACKING](https://covidtracking.com/api/)
- Drive-Thru COVID-19 Testing Centers, hand labelled from News Articles
- Twitter API
- News API
- Google News API

---

## 4️⃣ Contributors

| [Harsh Desai](https://github.com/hurshd0)     | [Elizabeth Ter Sahakyan](https://github.com/elizabethts) | [Han Lee](https://github.com/leehanchung) |[Anisha Sunkerneni](https://github.com/ars394) | [Michael Chrupcala](https://github.com/mchrupcala) | [Daniel Firpo](https://github.com/Turtled) |
| :--------------------: | :--------------------: | :--------------------: | :--------------------: | :--------------------: | :--------------------: | 
| <img src="https://avatars2.githubusercontent.com/u/16807421?s=400&u=844b3a27a223f7e3e2b3318e6a917d3641f93d6a&v=4" width = "200" /> | <img src="https://avatars1.githubusercontent.com/u/30808123?s=400&u=7757b1986b1e1713f378b402cb4e0a43b33ed451&v=4" width = "200" /> | <img src="https://avatars2.githubusercontent.com/u/4794839?s=400&u=1b4ce1a3a102b472ceaeae0f7f5b45df39f80322&v=4" width = "200" /> | <img src="https://media-exp1.licdn.com/dms/image/C5603AQGNbwDHi380iw/profile-displayphoto-shrink_200_200/0?e=1590624000&v=beta&t=EADYs8ZsWrS495ZsoIXd3X-7h8JYydf8RLPwMzIQbT4" width = "200" /> | <img src="https://avatars2.githubusercontent.com/u/52679312?s=400&u=9867ceebb039cd6d281940d5afb7a080e45e7385&v=4" width = "200" /> | <img src="https://avatars1.githubusercontent.com/u/17069338?s=460&u=cffb3688f1e8ad08518b791de36467775c8d92f3&v=4" width = "200" /> | 
| Data Scientist | Data Scientist | Machine Learning Engineer | Web Developer |  Web Developer |  Web Developer |
| [<img src="https://github.com/favicon.ico" width="20"> ](https://github.com/hurshd0) [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="20"> ](https://www.linkedin.com/in/hurshd/)                   |[<img src="https://github.com/favicon.ico" width="20"> ](https://github.com/elizabethts) [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="20"> ](https://www.linkedin.com/in/elizabethts/)    |[<img src="https://github.com/favicon.ico" width="20"> ](https://github.com/leehanchung) [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="20"> ](https://www.linkedin.com/in/hanchunglee/)    |[<img src="https://github.com/favicon.ico" width="20"> ](https://github.com/ars394) [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="20"> ](https://www.linkedin.com/in/anishasunkerneni/) | [<img src="https://github.com/favicon.ico" width="20"> ](https://github.com/mchrupcala) [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="20"> ](https://www.linkedin.com/in/michaelchrupcala/) | [<img src="https://github.com/favicon.ico" width="20"> ](https://github.com/Turtled) [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="20"> ](https://www.linkedin.com/in/daniel-firpo/)     

---

## 5️⃣ Tech Stack

### Front end built using:

- **Plotly Dash** for its interactive and easy to create dashboard 
```
NOTE:
Dash uses React under the hood to render the user interface you see when you load a web page created with Dash. Because React allows you to write your user interface in encapsulated components that manage their own state, it is easy to split up parts of code for Dash too. At the end of this tutorial, you will see that Dash components and React components map one to one!

For now, the important thing to know is that Dash components are mostly simple wrappers around existing React components. This means the entire React ecosystem is potentially usable in a Dash application!
```

- **Flask** is lightweight framework that is integrated with Plotly Dash

👉 [Plotly Dash Tutorial](https://dash.plotly.com/layout)

#### Back end built using:

- [FAST API](https://fastapi.tiangolo.com/)

---

# 6️⃣ Environment Variables

    *  MAPBOX_ACCESS_TOKEN - this is Mapbox API Token from Mapbox.com
    *  MAPBOX_STYLE - created using Mapbox Studio

---

# 7️⃣ Contributing

When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository before making a change.

Please note we have a [code of conduct](./CODE_OF_CONDUCT.md). Please follow it in all your interactions with the project.

## Issue/Bug Request
   
 **If you are having an issue with the existing project code, please submit a bug report under the following guidelines:**
 - Check first to see if your issue has already been reported.
 - Check to see if the issue has recently been fixed by attempting to reproduce the issue using the latest master branch in the repository.
 - Create a live example of the problem.
 - Submit a detailed bug report including your environment & browser, steps to reproduce the issue, actual and expected outcomes,  where you believe the issue is originating from, and any potential solutions you have considered.

### Feature Requests

We would love to hear from you about new features which would improve this app and further the aims of our project. Please provide as much detail and information as possible to show us why you think your new feature should be implemented.

### Pull Requests

If you have developed a patch, bug fix, or new feature that would improve this app, please submit a pull request. It is best to communicate your ideas with the developers first before investing a great deal of time into a pull request to ensure that it will mesh smoothly with the project.

Remember that this project is licensed under the MIT license, and by submitting a pull request, you agree that your work will be, too.

#### Pull Request Guidelines

- Ensure any install or build dependencies are removed before the end of the layer when doing a build.
- Update the README.md with details of changes to the interface, including new plist variables, exposed ports, useful file locations and container parameters.
- Ensure that your code conforms to our existing code conventions and test coverage.
- Include the relevant issue number, if applicable.
- You may merge the Pull Request in once you have the sign-off of two other developers, or if you do not have permission to do that, you may request the second reviewer to merge it for you.

### Attribution

These contribution guidelines have been adapted from [this good-Contributing.md-template](https://gist.github.com/PurpleBooth/b24679402957c63ec426).
