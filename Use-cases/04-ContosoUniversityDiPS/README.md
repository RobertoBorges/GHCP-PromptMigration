# Contoso University with DiPS
## A web application with a C# backend build with DiPS.

<a href="http://pedro-ramirez-suarez.github.io/DiPS/" target="_blank">DiPS</a> is a Distributed Publish Subscribe service, built with C# and clients for C#, Ruby and Javascript.

The application is a demonstration of how to build a web application that has a console application as backend and communicates with it through DiPS, the web appliction is built only with html, css and javascript.

## Running the application.
The first time you run the application the database structure will be created, you need to create the database and modify the console application  app.config file accordingly.

Run the website without debugging(ctrl+F5).

## Points of interest
The backend uses the <a href="http://www.nuget.org/packages/DiPSBackEndApplication/" target="_blank">DiPSBackEndApplication</a> nuget package, this package contains functionality that facilitates the creation of the service that acts as the backend, like registration of the controllers and it's methods, it also uses the <a href="http://www.nuget.org/packages/Needletail.DataAccess/" target="_blank">Needletail</a> micro orm and the  <a href="http://www.nuget.org/packages/Needletail.DataAccess.Migrations/" target="_blank">Needletail Migrations</a> packages for the data base access and initialization.

## Original idea.
The original contoso university application is a sample app and tutorial from Microsoft, the tutorial is located <a href="https://www.asp.net/mvc/overview/getting-started/getting-started-with-ef-using-mvc/creating-an-entity-framework-data-model-for-an-asp-net-mvc-application" target="_blank">here</a>

## Things to improve
The application needs some improvement handling a high number of  concurrent users, it handles the load pretty well, but some times some browsers may react to events that are intended to be for other user, this is not hard to fix, but right now I am not sure about the best way to handle some scenarios.




