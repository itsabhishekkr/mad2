<template>
    <div class="home">
      <h1>Welcome to Household Services</h1>
      <p>Your one-stop solution for all household services.</p>
      <router-link to="/login" class="btn btn-primary">Login</router-link>
      <!-- <router-link to="/signup" class="btn btn-secondary">Sign Up</router-link> -->
    </div>
  </template>
  
  <script>
  export default {
    name: 'HomePage'
  }
  </script>
  
  <style scoped>
  .home {
    text-align: center;
    padding: 50px;
  }
  
  h1 {
    font-size: 2.5em;
    margin-bottom: 20px;
  }
  
  p {
    font-size: 1.2em;
    margin-bottom: 40px;
  }
  
  .btn {
    display: inline-block;
    padding: 10px 20px;
    margin: 10px;
    font-size: 1em;
    text-decoration: none;
    border-radius: 5px;
    transition: background-color 0.3s ease;
  }
  
  .btn-primary {
    background-color: #007bff;
    color: white;
  }
  
  .btn-primary:hover {
    background-color: #0056b3;
  }
  
  .btn-secondary {
    background-color: #6c757d;
    color: white;
  }
  
  .btn-secondary:hover {
    background-color: #5a6268;
  }
  </style>