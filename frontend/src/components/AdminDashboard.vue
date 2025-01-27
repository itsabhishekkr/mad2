<template>
    <div class="admin-dashboard">
      <h1>Admin Dashboard</h1>
      <div class="buttons">
        <router-link to="/admin/customers" class="btn btn-primary">Customer Management</router-link>
        <router-link to="/admin/professionals" class="btn btn-primary">Professional Management</router-link>
        <router-link to="/admin/services" class="btn btn-primary">Service Management</router-link>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'AdminDashboard'
  }
  </script>
  
  <style scoped>
  .admin-dashboard {
    text-align: center;
    padding: 50px;
  }
  
  h1 {
    font-size: 2.5em;
    margin-bottom: 20px;
  }
  
  .buttons {
    display: flex;
    justify-content: center;
    gap: 20px;
  }
  
  .btn {
    display: inline-block;
    padding: 10px 20px;
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
  </style>