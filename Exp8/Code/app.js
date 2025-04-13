var app = angular.module('myApp', ['ngRoute']);

// Configure Routes
app.config(function($routeProvider) {
  $routeProvider
    .when('/binding', {
      templateUrl: 'templates/binding.html',
      controller: 'BindingController'
    })
    .when('/login', {
      templateUrl: 'templates/login.html',
      controller: 'LoginController'
    })
    .when('/book-search', {
      templateUrl: 'templates/book-search.html',
      controller: 'BookController'
    })
    .otherwise({
      redirectTo: '/binding'
    });
});

// Controllers
app.controller('BindingController', function($scope) {
  $scope.message = "This is One-Way Data Binding!";
  $scope.name = "John";
});

app.controller('LoginController', function($scope) {
  $scope.username = '';
  $scope.password = '';
  $scope.message = '';

  $scope.login = function() {
    if ($scope.username === 'Chirag' && $scope.password === '1234') {
      $scope.message = 'Login Successful!';
    } else {
      $scope.message = 'Invalid Credentials!';
    }
  };
});

app.controller('BookController', function($scope) {
  $scope.books = [
    { title: 'Book A', author: 'Author 1', genre: 'Fiction' },
    { title: 'Book B', author: 'Author 2', genre: 'Non-fiction' },
    { title: 'Book C', author: 'Author 3', genre: 'Science' }
  ];
  $scope.search = '';
});
